import copy

import torch
import torch.nn as nn
# from transformers import BartForConditionalGeneration
from .prefix_gen_bart import PrefixGenBartForConditionalGeneration
from transformers.models.bart.modeling_bart import shift_tokens_right
from transformers import T5ForConditionalGeneration, T5Tokenizer
from transformers import BartForConditionalGeneration, AutoConfig, AutoModel
from utils import hungarian_matcher, get_best_span, get_best_span_simple
from torch.nn import NLLLoss
from transformers.modeling_outputs import Seq2SeqLMOutput
import ipdb

# 主要实现forward方法。
# 注意这个model才定义了数据逻辑处理的forward。这个model之前的父类都是BART的重写
# 继承了PrefixGenBartForConditionalGeneration，但是重写了forward函数，把PrefixGenBartForConditionalGeneration的forward覆盖了。
# 注意！重写的forward方法必须与父类的forward保持输入输出的一致性
# 下面方法的self.model是在PrefixGenBartForConditionalGeneration定义的self.model = PrefixGenBartModel(config)
# 所以在CopyBartWithReg的forward调用的self.model(kwargs)直接就跳转到了PrefixGenBartModel的forward
class CopyBartWithReg(PrefixGenBartForConditionalGeneration):
    def __init__(self, config):
        super().__init__(config)
        # If extra model/module, we need to initialize the module here.
        self.linear_copy = nn.Linear(self.config.d_model, 1)

        # paie
        self.w_prompt_start = nn.Parameter(torch.rand(config.d_model, ))
        self.w_prompt_end = nn.Parameter(torch.rand(config.d_model, ))
        self.model._init_weights(self.w_prompt_start)
        self.model._init_weights(self.w_prompt_end)
        self.loss_fct = nn.CrossEntropyLoss(reduction='sum')

    def forward(
            self,
            input_ids=None,
            prefix=None,
            attention_mask=None,
            decoder_input_ids=None,
            decoder_attention_mask=None,
            arg_joint_prompts=None,  # Tag: Changed，
            target_info=None,  # Tag: Changed，
            old_tok_to_new_tok_indexs=None,  # Tag: Changed，
            arg_list=None,  # Tag: Changed，
            head_mask=None,
            decoder_head_mask=None,
            cross_attn_head_mask=None,
            encoder_outputs=None,
            past_key_values=None,
            inputs_embeds=None,
            decoder_inputs_embeds=None,
            labels=None,
            use_cache=None,
            output_attentions=None,
            output_hidden_states=None,
            return_dict=None,
    ):

        prefix_enc={}
        prefix_enc['encoder_prefix'] = prefix['encoder_prefix']
        prefix_enc['local_prefix'] = prefix['local_prefix']
        context_outputs = self.model(
            input_ids=input_ids,
            prefix=prefix_enc,   # 在不在这里加prefix？这里不加，之后doc编码就没得加了，或者说这里只加encoder的
            attention_mask=attention_mask,
            return_dict=True,
        )

        # context_outputs = self.model(
        #     input_ids=input_ids,
        #     prefix=prefix,   # encode_doc_with_all_prefix
        #     attention_mask=attention_mask,
        #     return_dict=True,
        # )
        decoder_context = context_outputs.encoder_last_hidden_state  # Sequence of hidden-states at the output of the last layer of the encoder of the model.
        context_outputs = context_outputs.last_hidden_state  # Sequence of hidden-states at the output of the last layer of the decoder of the model.

        decoder_prompt_outputs = self.model.decoder(
            input_ids=decoder_input_ids,
            cross_prefix=prefix['cross_prefix'] if self.config.use_cross_prefix else None,
            decoder_prefix=prefix['decoder_prefix'] if self.config.use_decoder_prefix else None,
            attention_mask=decoder_attention_mask,
            encoder_hidden_states=decoder_context,
            encoder_attention_mask=attention_mask,
        )

        decoder_prompt_outputs = decoder_prompt_outputs.last_hidden_state   #[bs, prompt_len, H]
        logit_lists = list()
        total_loss = 0.
        # 每次遍历一个batch中的一条数据
        # context_output：只有doc经过整个BART模型后的decoder的最后一层隐藏层的参数。
        # decoder_prompt_output：模板和doc经过decoder之后得到的输出
        # arg_joint_prompt：记录的是模板中出现的角色名在模板编码化后的start和end位置。
        # old_tok_to_new_tok_index：doc中各token对应在doc编码后数据的位置
        for i, (context_output, decoder_prompt_output, arg_joint_prompt, old_tok_to_new_tok_index) in \
                enumerate(zip(context_outputs, decoder_prompt_outputs, arg_joint_prompts, old_tok_to_new_tok_indexs)):

            batch_loss = list()
            cnt = 0
            output = dict()
            # 对当前事件预定义的每一个角色进行遍历，生成set of span selectors θk，并提取出预测出来的text，与真实论元进行loss计算
            for arg_role in arg_joint_prompt.keys():  # arg_rolr:'crime'
                """
                "arg_role": {"tok_s": , "tok_e": }
                """
                # prompt_slots：{'tok_s': [12], 'tok_e': [13]}。取出当前遍历的角色在模板编码化后的start和end
                prompt_slots = arg_joint_prompt[arg_role]

                start_logits_list = list()
                end_logits_list = list()
                # 这里就是生成多个特定于角色的跨度选择器θk，文中还说到：“一个角色可能会有多个槽（对应多个论元），相应的，就会产生多个角色特征和跨度选择器”。
                # 但是其实最多就两个，这里的所谓多个就是由模板中的类似于”Recipient ( and Recipient )“形式的占位符生成的。
                for (p_start, p_end) in zip(prompt_slots['tok_s'], prompt_slots['tok_e']):
                    prompt_query_sub = decoder_prompt_output[
                                       p_start:p_end]  # 取出最后预测结果[p_start:p_end]位置的输出，训练目的就是要让这个位置的结果是正确的论元
                    prompt_query_sub = torch.mean(prompt_query_sub, dim=0).unsqueeze(0)  # 得到角色特征
                    # 得到prompts中当前jueseslot的特定于角色的跨度选择器θk
                    start_query = (prompt_query_sub * self.w_prompt_start).unsqueeze(-1)  # [1, H, 1]
                    end_query = (prompt_query_sub * self.w_prompt_end).unsqueeze(-1)  # [1, H, 1]
                    # 实现论文中的公式3,torch.bmm:三维数据的乘法，需要两个tensor的第一维是相等的，然后第一个数组的第三维和第二个数组的第二维度要求一样，得到的就是第一维不变，剩下两维正常相乘。这里的context_output是(500,1024)然后经过unsqueeze(0)变成了(1,500,1024)。start_query是(1,1024,1)，乘出来就是(1,500,1)
                    # 这两句代码将context与θk相乘，获得context中的每一个token被选中称为论元的start/end的概率。
                    start_logits = torch.bmm(context_output.unsqueeze(0), start_query).squeeze()
                    end_logits = torch.bmm(context_output.unsqueeze(0), end_query).squeeze()

                    start_logits_list.append(start_logits)
                    end_logits_list.append(end_logits)

                output[arg_role] = [start_logits_list, end_logits_list]  # 记录每个角色预测出来的论元

                if self.training:
                    # calculate loss
                    # target_info记录的是角色对应论元在doc经过编码后的位置（包括重叠论元），target_info[i]取出来的是一个batch中的第i个中出现的所有角色对应的论元，target_info[i][arg_role]取出来的是arg_role角色对应的论元
                    target = target_info[i][arg_role]  # "target": {"text": ,"span_s": ,"span_e": }，取出label
                    predicted_spans = list()
                    for (start_logits, end_logits) in zip(start_logits_list, end_logits_list):
                        if self.config.matching_method_train == 'accurate':
                            predicted_spans.append(get_best_span(start_logits, end_logits, old_tok_to_new_tok_index,
                                                                 self.config.max_span_length))
                        elif self.config.matching_method_train == 'max':  # 实现了公式3（由跨度选择器得到span），但是论文中写的softmax，这里直接max，因为其实也没差，softmax之后也是取max
                            predicted_spans.append(get_best_span_simple(start_logits,
                                                                        end_logits))  # predicted_spans：[[tensor(9), tensor(9)]]
                        else:
                            raise AssertionError()

                    target_spans = [[s, e] for (s, e) in zip(target["span_s"], target["span_e"])]  # 这里是真正希望预测出来的值
                    if len(target_spans) < len(
                            predicted_spans):  # 这里是当预测出来有多的论元时，就在target上增加(0,0)表示没有论元,以此来让模型学习，以后多预测出来的span都预测成(0, 0)
                        # need to consider whether to make more
                        pad_len = len(predicted_spans) - len(target_spans)
                        target_spans = target_spans + [[0, 0]] * pad_len
                        target["span_s"] = target["span_s"] + [0] * pad_len
                        target["span_e"] = target["span_e"] + [0] * pad_len

                    if self.config.bipartite:  # 论文中的Bipartite Matching部分，为当前角色的多个论元预测最佳匹配。
                        idx_preds, idx_targets = hungarian_matcher(predicted_spans, target_spans)
                    else:  # 不会进入此代码块
                        idx_preds = list(range(len(predicted_spans)))
                        idx_targets = list(range(len(target_spans)))
                        if len(idx_targets) > len(idx_preds):
                            idx_targets = idx_targets[0:len(idx_preds)]
                        idx_preds = torch.as_tensor(idx_preds, dtype=torch.int64)
                        idx_targets = torch.as_tensor(idx_targets, dtype=torch.int64)

                    cnt += len(idx_preds)  # 预测出来的论元数，其实就是模板中出现的角色占位符数
                    start_loss = self.loss_fct(torch.stack(start_logits_list)[idx_preds],
                                               torch.LongTensor(target["span_s"]).to(self.config.device)[
                                                   idx_targets])  # 计算损失
                    end_loss = self.loss_fct(torch.stack(end_logits_list)[idx_preds],
                                             torch.LongTensor(target["span_e"]).to(self.config.device)[idx_targets])
                    batch_loss.append((start_loss + end_loss) / 2)  # 这里将两个损失融合，其实就是取平均值。最终的len(batch_loss)=事件预定义角色数

            logit_lists.append(output)  # 存放的是每个角色预测出来的论元
            if self.training:  # inside batch mean loss
                total_loss = total_loss + torch.sum(torch.stack(batch_loss)) / cnt

        if self.training:
            return total_loss / len(context_outputs), logit_lists  # 这里将损失/batch_size
        else:
            return [], logit_lists
