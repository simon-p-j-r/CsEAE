import os
import random
import re
import sys
sys.path.append("../")
import torch

from torch.utils.data import Dataset
from processors.processor_base import DSET_processor
from utils import EXTERNAL_TOKENS, _PREDEFINED_QUERY_TEMPLATE
import copy
import numpy as np



# 里面定义的方法全部在evaluate.py文件中的predict()方法调用
class InputFeatures(object):
    """A single set of features of data."""

    def __init__(self, example_id, feature_id, 
                event_type, event_trigger,
                enc_text, enc_input_ids, enc_mask_ids, 
                dec_prompt_text, dec_prompt_ids, dec_prompt_mask_ids,
                arg_quries, arg_joint_prompt, target_info,
                old_tok_to_new_tok_index = None, full_text = None, arg_list=None,
                local_attention_mask=None,
                co_prompt_ids=None, co_prompt_mask_ids=None
        ):

        self.example_id = example_id
        self.feature_id = feature_id
        self.event_type = event_type
        self.event_trigger = event_trigger
        
        self.enc_text = enc_text
        self.enc_input_ids = enc_input_ids
        self.enc_mask_ids = enc_mask_ids


        if arg_quries is not None:
            self.dec_arg_query_ids = [v[0] for k,v in arg_quries.items()]
            self.dec_arg_query_masks = [v[1] for k,v in arg_quries.items()]
            self.dec_arg_start_positions = [v[2] for k,v in arg_quries.items()]
            self.dec_arg_end_positions = [v[3] for k,v in arg_quries.items()]
            self.start_position_ids = [v['span_s'] for k,v in target_info.items()]
            self.end_position_ids = [v['span_e'] for k,v in target_info.items()]
        else:
            self.dec_arg_query_ids = None
            self.dec_arg_query_masks = None
        
        self.arg_joint_prompt = arg_joint_prompt
        
        self.target_info = target_info
        self.old_tok_to_new_tok_index = old_tok_to_new_tok_index

        self.full_text = full_text
        self.arg_list = arg_list

        self.dec_prompt_texts = dec_prompt_text
        self.dec_prompt_ids =dec_prompt_ids
        self.dec_prompt_mask_ids=dec_prompt_mask_ids

        self.local_attention_mask = local_attention_mask

        self.co_prompt_ids = co_prompt_ids
        self.co_prompt_mask_ids = co_prompt_mask_ids

    # 由evaluate.py文件中的predict()方法调用
    def init_pred(self):
        self.pred_dict_tok = dict()
        self.pred_dict_word = dict()

    # 由evaluate.py文件中的predict()方法调用
    def add_pred(self, role, span, dset_type):
        if role not in self.pred_dict_tok:
            self.pred_dict_tok[role] = list()
        if span not in self.pred_dict_tok[role]:
            self.pred_dict_tok[role].append(span)  # self.pred_dict_tok里面存储了这个feature的所有预测出来的相对于编码后的span，存储的span个数等于对应模板的占位符数，格式是“role”:[span]的字典。这样的方法调用也能说明为什么在predict里面可以是以span selector为单位，而不是以feature为单位了

            if span!=(0, 0):
                if role not in self.pred_dict_word:
                    self.pred_dict_word[role] = list()
                word_span = self.get_word_span(span, dset_type)  # convert token span to word span
                if word_span not in self.pred_dict_word[role]:
                    self.pred_dict_word[role].append(word_span)  # 存储这个feature预测出来的对应于编码前的原span

    # 由evaluate.py文件中的predict()方法调用，目的是获得论元在原doc的start和end。为此写了这么多方法，简直有病，原event类型的数据不就有吗，传进来的时候直接复制给gt_dict_word不行吗...
    def set_gt(self, model_type, dset_type):
        self.gt_dict_tok = dict()  # 存储论元在编码后的doc上的start和end
        if model_type == 'base':  # false
            for k,v in self.target_info.items():
                span_s = list(np.where(v["span_s"])[0])
                span_e = list(np.where(v["span_e"])[0])
                self.gt_dict_tok[k] = [(s,e) for (s,e) in zip(span_s, span_e)]
        elif "paie" or 'amr' in model_type:
            for k,v in self.target_info.items():  # self.target_info是每个features初始化的时候赋值的，里面存储的是角色对应论元在doc经过编码后的位置（包括重叠论元），其实也就是label
                self.gt_dict_tok[k] = [(s,e) for (s,e) in zip(v["span_s"], v["span_e"])]
        else:
            assert(0==1)

        self.gt_dict_word = dict()  # 存储论元在原doc上的start和end
        for role in self.gt_dict_tok:  # 处理事件中的所有角色，不管是不是有论元
            for span in self.gt_dict_tok[role]:  # 获得角色对应的论元（如果有的话）
                if span!=(0, 0):
                    if role not in self.gt_dict_word:
                        self.gt_dict_word[role] = list()
                    word_span = self.get_word_span(span, dset_type)
                    self.gt_dict_word[role].append(word_span)

    # 由下面的get_word_span方法调用，这里得到的其实就是编码后的token在原token上的映射，相当于反过来了。而且这里有@property修饰，所以这个方法是个常量
    @property
    def old_tok_index(self):
        new_tok_index_to_old_tok_index = dict()
        for old_tok_id, (new_tok_id_s, new_tok_id_e) in enumerate(self.old_tok_to_new_tok_index):
            for j in range(new_tok_id_s, new_tok_id_e):
                new_tok_index_to_old_tok_index[j] = old_tok_id 
        return new_tok_index_to_old_tok_index

    # 由上面的set_gt方法调用，目的是获得传进来的span对应在原doc的位置（传进来的span是相对于编码后的doc的）
    def get_word_span(self, span, dset_type):  # 传进来的是label（ground truth的start和end）和数据集名称
        """
        Given features with gt/pred token-spans, output gt/pred word-spans
        """
        if span==(0, 0):
            raise AssertionError()
        offset = 0 if dset_type=='ace_eeqa' else self.event_trigger[2]  # ace是句子级的，所以默认都是0
        span = list(span)
        span[0] = min(span[0], max(self.old_tok_index.keys()))  # 这里的start和end是相对于编码后的句子来说的，这里在控制start不能超过编码后句子的最大长度
        span[1] = max(span[1]-1, min(self.old_tok_index.keys()))  # 这里控制end不能低于编码后句子的最小长度（所谓最小长度其实一般就是1，因为0的位置被BART要求编码的特殊开始字段占了）

        while span[0] not in self.old_tok_index:  # 上面的代码控制了start不能超过编码后句子的最大长度，但是没有控制其不能低于编码后句子的最小长度，一旦低于了，这里就疯狂加
            span[0] += 1 
        span_s = self.old_tok_index[span[0]] + offset  # 这里将start从相对于编码后的句子改成相对于编码前的句子（也就是token的时候）
        while span[1] not in self.old_tok_index:  # 同理，一旦高于了，这里就疯狂减
            span[1] -= 1 
        span_e = self.old_tok_index[span[1]] + offset # 这里将end从相对于编码后的句子改成相对于编码前的句子
        while span_e < span_s:
            span_e += 1  # 控制end>start，这里有点儿戏---
        return (span_s, span_e)

        
    def __repr__(self):
        s = "" 
        s += "example_id: {}\n".format(self.example_id)
        s += "event_type: {}\n".format(self.event_type)
        s += "trigger_word: {}\n".format(self.event_trigger)
        s += "old_tok_to_new_tok_index: {}\n".format(self.old_tok_to_new_tok_index)
        
        s += "enc_input_ids: {}\n".format(self.enc_input_ids)
        s += "enc_mask_ids: {}\n".format(self.enc_mask_ids)
        s += "dec_prompt_ids: {}\n".format(self.dec_prompt_ids)
        s += "dec_prompt_mask_ids: {}\n".format(self.dec_prompt_mask_ids)
        return s

# 这个类主要就是重写了collate_fn方法，然后让MultiargProcessor来调用，MultiargProcessor会把这个coolate_fn传递给父类DSET_processor，然后传进Dataloader中
class ArgumentExtractionDataset(Dataset):
    def __init__(self, features):
        self.features = features
    
    def __len__(self):
        return len(self.features)

    # 在Dataset的__getitem__把一条一条的数据发出来以后，Dataloader会根据你定义的batch_size参数把这些东西组织起来（其实是一个batch_list）。然后再送给collate_fn组织成batch最后的样子，
    def __getitem__(self, idx):
        return self.features[idx]

    @staticmethod
    def collate_fn(batch):  # 一个batch里面有四个Features
        
        enc_input_ids = torch.tensor([f.enc_input_ids for f in batch])
        enc_mask_ids = torch.tensor([f.enc_mask_ids for f in batch])

        if batch[0].dec_prompt_ids is not None:
            dec_prompt_ids = torch.tensor([f.dec_prompt_ids for f in batch])
            dec_prompt_mask_ids = torch.tensor([f.dec_prompt_mask_ids for f in batch])
        else:
            dec_prompt_ids=None
            dec_prompt_mask_ids=None

        example_idx = [f.example_id for f in batch]  # 得到doc_id
        feature_idx = torch.tensor([f.feature_id for f in batch])  # 由feature_idx可以知道这些数据是打乱过的

        if batch[0].dec_arg_query_ids is not None:  # None
            dec_arg_query_ids = [torch.LongTensor(f.dec_arg_query_ids) for f in batch]
            dec_arg_query_mask_ids = [torch.LongTensor(f.dec_arg_query_masks) for f in batch]
            dec_arg_start_positions = [torch.LongTensor(f.dec_arg_start_positions) for f in batch]
            dec_arg_end_positions = [torch.LongTensor(f.dec_arg_end_positions) for f in batch]
            start_position_ids = [torch.FloatTensor(f.start_position_ids) for f in batch]
            end_position_ids = [torch.FloatTensor(f.end_position_ids) for f in batch]
        else:
            dec_arg_query_ids = None
            dec_arg_query_mask_ids = None
            dec_arg_start_positions = None
            dec_arg_end_positions = None
            start_position_ids = None
            end_position_ids = None

        target_info = [f.target_info for f in batch]  # 角色对应论元在doc经过编码后的位置
        old_tok_to_new_tok_index = [f.old_tok_to_new_tok_index for f in batch]
        arg_joint_prompt = [f.arg_joint_prompt for f in batch]
        arg_lists = [f.arg_list for f in batch]

        # mask
        local_attention_mask = torch.stack([f.local_attention_mask for f in batch])


        # co-occur
        co_input_ids = torch.tensor([f.co_prompt_ids for f in batch])
        co_prompt_mask_ids = torch.tensor([f.co_prompt_mask_ids for f in batch])

        return enc_input_ids, enc_mask_ids, \
                dec_arg_query_ids, dec_arg_query_mask_ids,\
                dec_prompt_ids, dec_prompt_mask_ids,\
                target_info, old_tok_to_new_tok_index, arg_joint_prompt, arg_lists, \
                example_idx, feature_idx, \
                local_attention_mask, \
                co_input_ids, co_prompt_mask_ids, \
                dec_arg_start_positions, dec_arg_end_positions, \
                start_position_ids, end_position_ids

# 注意看这个类是processor_base中DSET_processor的子类，所以说有一些self的参数和方法要特别注意
class MultiargProcessor(DSET_processor):
    def __init__(self, args, tokenizer):
        super().__init__(args, tokenizer)  # 初始化父类DSET_processor,DSET_processor初始化就是读了dset_meta中的两个对应数据集的文件
        self.set_dec_input()  # 根据使用model_type判断是否需要加上prompt，并设置一个标签
        # 这个类主要就是重写了collate_fn方法，然后让MultiargProcessor来调用，
        # MultiargProcessor会把这个coolate_fn传递给父类DSET_processor，然后传进Dataloader中
        self.collate_fn = ArgumentExtractionDataset.collate_fn
    
    # base是PAIEE的设置
    def set_dec_input(self):
        self.arg_query=False
        self.prompt_query=False
        if self.args.model_type == "base":
            self.arg_query = True
        elif "paie" or 'amr' in self.args.model_type:
            self.prompt_query = True
        else:
            raise NotImplementedError(f"Unexpected setting {self.args.model_type}")

        self.co_occur = True
    # 获得模板，然后将其转换为字典的数据格式
    # 返回一个模板prompt组成的字典，
    # 格式为 {事件类型:prompt}
    # eg:'artifactexitence.artifactfailure.mechanicalfailure':'prompt start, mechanicalartifact failed due to instrument at place ,end\n'
    @staticmethod
    def _read_prompt_group(prompt_path):
        with open(prompt_path) as f:
            lines = f.readlines()
        prompts = dict()
        for line in lines:
            if not line:
                continue
            # 这里是将所有模板做成了一个字典，格式为{事件类型:prompt}
            event_type, prompt = line.split(":")
            prompts[event_type] = prompt
        return prompts


    def create_dec_qury(self, arg, event_trigger):
        dec_text = _PREDEFINED_QUERY_TEMPLATE.format(arg=arg, trigger=event_trigger)
                
        dec = self.tokenizer(dec_text)
        dec_input_ids, dec_mask_ids = dec["input_ids"], dec["attention_mask"]

        while len(dec_input_ids) < self.args.max_dec_seq_length:
            dec_input_ids.append(self.tokenizer.pad_token_id)
            dec_mask_ids.append(self.args.pad_mask_token)

        matching_result = re.search(arg, dec_text)
        char_idx_s, char_idx_e = matching_result.span(); char_idx_e -= 1
        tok_prompt_s = dec.char_to_token(char_idx_s)
        tok_prompt_e = dec.char_to_token(char_idx_e) + 1

        return dec_input_ids, dec_mask_ids, tok_prompt_s, tok_prompt_e

    # 这个方法由processor_base.py文件中父类DSET_processor的generate_dataloader方法调用
    # 是重写的父类DSET_processor中的同名方法
    def convert_examples_to_features(self, examples, role_name_mapping=None):
        if self.prompt_query:
            prompts = self._read_prompt_group(self.args.prompt_path)  # prompts是由模板prompt组成的字典，格式为{事件类型:prompt} eg:'artifactexitence.artifactfailure.mechanicalfailure':'prompt start, mechanicalartifact failed due to instrument at place ,end\n'

        if os.environ.get("DEBUG", False): counter = [0, 0, 0]
        features = []

        for example_idx, example in enumerate(examples):
            example_id =example.doc_id
            sent = example.sent  # 这个是由窗口切割过的cut_text
            event_type = example.type
            event_args = example.args
            sentences = example.sentences

            trigger_start, trigger_end = example.trigger['start'], example.trigger['end']
            # NOTE: extend trigger full info in features,主要是增加了text字段：['injured', [62, 63], 0]
            event_trigger = [example.trigger['text'], [trigger_start, trigger_end], example.trigger['offset'], example.trigger['sent_idx']]
            event_args_name = [arg['role'] for arg in event_args]  # 存放当前事件中论元对应的角色
            if os.environ.get("DEBUG", False): counter[2] += len(event_args_name)

            if self.args.dataset_type in ['wikievent', 'rams']:
                event_types = []
                co_trigger = []
                for event in example.event_types:
                    event_types.append(event['event_type'])
                    co_trigger.append(event['trigger'])
            elif self.args.dataset_type in ['MLEE', 'ace_eeqa']:
                event_types = []
                co_trigger = []
                for event in example.event_types:
                    event_types.append(event['event_type'])
                    trigger = event['trigger']
                    trigger = tuple(trigger)
                    co_trigger.append(trigger)
                co_trigger = list(set(co_trigger))
                co_trigger = sorted(co_trigger)
            else:
                event_types=example.event_types

            if self.args.dataset_type in ['MLEE', 'ace_eeqa']:
                offset = 0
                marker_indice = list(range(len(co_trigger)))  # 这个制作索引的方法很有趣，这里是触发词的索引
                for i, trigger in enumerate(co_trigger):
                    t_start = trigger[0] + offset
                    t_end = trigger[1] + offset
                    if trigger[0] == trigger_start and trigger[1] == trigger_end:
                        sent = sent[:t_start] + ['<t--1>'] + sent[t_start: t_end] + ['</t--1>'] + sent[t_end:]
                    else:
                        sent = sent[:t_start] + ['<t-%d>' % marker_indice[i]] + sent[t_start: t_end] + [
                            '</t-%d>' % marker_indice[i]] + sent[t_end:]
                    offset += 2
            else:
                sent = sent[:trigger_start] + ['<t>'] + sent[trigger_start:trigger_end] + ['</t>'] + sent[trigger_end:]  # 这里是给触发词上特殊标记的
            enc_text = " ".join(sent)  # 将sentence合并成一个句子

            # change the mapping to idx2tuple (start/end word idx) 将原始sentence的各个token的开始和结束位置转换为在tokenizer之后的编码中对应的开始和结束位置
            old_tok_to_char_index = []     # old tok: split by oneie 这里是最text类型的doc中每个token的位置
            old_tok_to_new_tok_index = []  # new tok: split by BART  这里是经过tokenizer编码之后，原来text中每个token在编码后字段中的位置

            curr = 0
            for tok in sent:
                if tok not in EXTERNAL_TOKENS:
                    old_tok_to_char_index.append([curr, curr+len(tok)-1])  # exact word start char and end char index
                curr += len(tok)+1

            # 开始对输入sentence编码
            enc = self.tokenizer(enc_text)
            enc_input_ids, enc_mask_ids = enc["input_ids"], enc["attention_mask"]
            if len(enc_input_ids)> self.args.max_enc_seq_length:
                raise ValueError(f"Please increase max_enc_seq_length above {len(enc_input_ids)}")

            while len(enc_input_ids) < self.args.max_enc_seq_length:
                enc_input_ids.append(self.tokenizer.pad_token_id)
                enc_mask_ids.append(self.args.pad_mask_token)

            # 这个for循环将原始doc中各个token的开始和结束位置转换为在tokenizer之后对应token的开始和结束位置
            for old_tok_idx, (char_idx_s, char_idx_e) in enumerate(old_tok_to_char_index):
                new_tok_s = enc.char_to_token(char_idx_s)  # 这个方法识别传进来的char_idx_s的值，获得一个开始位置，并将这个开始位置转换为在enc中的开始位子
                new_tok_e = enc.char_to_token(char_idx_e) + 1
                new_tok = [new_tok_s, new_tok_e]
                old_tok_to_new_tok_index.append(new_tok)

            # Deal with prompt template。这个prompt_query就是正常paie做数据处理的方式，因为还有做paiee的数据处理方式
            if self.prompt_query:
                dec_prompt_text = prompts[event_type].strip()  # 取得当前事件类型的模板
                if dec_prompt_text:
                    dec_prompt = self.tokenizer(dec_prompt_text)  # 对模板进行编码
                    dec_prompt_ids, dec_prompt_mask_ids = dec_prompt["input_ids"], dec_prompt["attention_mask"]
                    assert len(dec_prompt_ids)<=self.args.max_prompt_seq_length, f"\n{example}\n{arg_list}\n{dec_prompt_text}\n{arg_list}"
                    while len(dec_prompt_ids) < self.args.max_prompt_seq_length:  # 这个while循环是对template做padding的，长度为80
                        dec_prompt_ids.append(self.tokenizer.pad_token_id)
                        dec_prompt_mask_ids.append(self.args.pad_mask_token)
                else:
                    raise ValueError(f"no prompt provided for event: {event_type}")
            else:
                dec_prompt_text, dec_prompt_ids, dec_prompt_mask_ids = None, None, None

            # 注意这个self.argument_dict参数是父类DSET_processor中的。里面存放的是事件类型中有的角色。arg_list： ['instrument', 'killer', 'victim', 'place']。注意event_args_name存放的是当前事件的论元对应的各个角色
            arg_list = self.argument_dict[event_type.replace(':', '.')]  # 当前事件类型预先定义的所有角色
            # NOTE: Large change - original only keep one if multiple span for one arg role
            arg_quries = dict()
            arg_joint_prompt = dict()  # 记录的是模板中出现的角色名在模板编码化后的start和end位置 eg:'killer':{'tok_s': [5], 'tok_e': [6]}
            target_info = dict()  # 记录的是一个角色在事件中对应的所有论元（包括重叠论元）的text和在编码后的doc里的起止位置 eg:'killer':{'text': ['Officer Caesar Goodson Jr.'], 'span_s': [100], 'span_e': [106]}
            if os.environ.get("DEBUG", False): arg_set=set()

            # 这个循环对每个当前事件类型预定义的所有角色做处理
            for arg in arg_list:
                arg_query = None
                prompt_slots = None
                arg_target = {  # 这里存放的是当前角色的所有论元（包括重叠论元）的信息：{'text': ['Officer Caesar Goodson Jr.'], 'span_s': [100], 'span_e': [106]} 这里的start和end位置是相对于编码后的doc来说的
                    "text": list(),
                    "span_s": list(),
                    "span_e": list()
                }

                if self.arg_query:  # false
                    arg_query = self.create_dec_qury(arg, event_trigger[0])

                # 这个判断是为了抽取当前处理角色出现的位置（在模板编码后的）
                if self.prompt_query:
                    prompt_slots = {  # 这个prompt_slots记录的就是模板中出现的角色名在模板编码化后的start和end位置
                        "tok_s":list(), "tok_e":list(),
                    }
                    if role_name_mapping is not None:
                        arg_ = role_name_mapping[event_type][arg]
                    else:
                        arg_ = arg
                    # Using this more accurate regular expression might further improve rams results，查看角色在模板中的位置
                    # 这里的matching_result就是角色在文本模板中出现的start和end位置，以及角色名：<re.Match object; span=(41, 51), match='instrument'>
                    # 这个循环的目的是得到角色在转换为编码后的模板中的start和end
                    for matching_result in re.finditer(r'\b'+re.escape(arg_)+r'\b', dec_prompt_text.split('.')[0]):   # re.findall:正则匹配方法，在字符串中找到正则表达式所匹配的所有子串，并把它们作为一个迭代器返回
                        char_idx_s, char_idx_e = matching_result.span()
                        char_idx_e -= 1
                        tok_prompt_s = dec_prompt.char_to_token(char_idx_s)
                        tok_prompt_e = dec_prompt.char_to_token(char_idx_e) + 1
                        prompt_slots["tok_s"].append(tok_prompt_s);prompt_slots["tok_e"].append(tok_prompt_e)

                # answer_texts：存放角色在当前事件提及中对应的所有论元的txt
                # start_positions：存放当前角色对应的所有论元映射在编码化后的doc的开始位置
                # end_positions：存放当前角色对应的所有论元映射在编码化后的doc的结束位置
                answer_texts, start_positions, end_positions = list(), list(), list()
                if arg in event_args_name:  # 查看当前遍历的角色有没有在当前事件的论元对应角色集中
                    # Deal with multi-occurance
                    if os.environ.get("DEBUG", False): arg_set.add(arg)
                    arg_idxs = [i for i, x in enumerate(event_args_name) if x == arg]  # 获得arg这个角色在当前事件的论元对应角色集中的出现过的位置，
                    if os.environ.get("DEBUG", False): counter[0] += 1; counter[1]+=len(arg_idxs)

                    # 通过论元位置arg_idxs，这里得到这个角色对应的所有论元，arg_idxs->event_args_name->event_args
                    for arg_idx in arg_idxs:
                        # event_args是存放论元的：{'start': 26, 'end': 31, 'text': 'Om Omran and Om Mohammad', 'role': 'transporter'}
                        event_arg_info = event_args[arg_idx]
                        answer_text = event_arg_info['text']; answer_texts.append(answer_text)
                        start_old, end_old = event_arg_info['start'], event_arg_info['end']
                        start_position = old_tok_to_new_tok_index[start_old][0]; start_positions.append(start_position)
                        end_position = old_tok_to_new_tok_index[end_old-1][1]; end_positions.append(end_position)

                if self.arg_query: # false
                    arg_target["span_s"] = [1 if i in start_positions else 0 for i in range(self.args.max_enc_seq_length)]
                    arg_target["span_e"] = [1 if i in end_positions else 0 for i in range(self.args.max_enc_seq_length)]
                    if sum(arg_target["span_s"])==0:
                        arg_target["span_s"][0] = 1
                        arg_target["span_e"][0] = 1
                if self.prompt_query:
                    arg_target["span_s"]= start_positions
                    arg_target["span_e"] = end_positions

                arg_target["text"] = answer_texts
                arg_quries[arg] = arg_query  # 这个参数没用
                arg_joint_prompt[arg] = prompt_slots  # 记录角色名在模板编码后的位置，注意这里有些角色的位置有两个是因为这个模板的特殊性，存在复数可能的一些角色是以Victim (and Victim)的形式出现的
                target_info[arg] = arg_target  # 角色对应论元在doc经过编码后的位置

            if not self.arg_query:
                arg_quries = None
            if not self.prompt_query:
                arg_joint_prompt=None

            # '''开始mask处理'''
            if self.args.dataset_type == 'ace_eeqa':  # 句子级mask
                assert 0==1

            else:  # 文档级mask
                if self.args.dataset_type in ['wikievent']:
                    # window mlee wiki
                    first_word_locs = copy.deepcopy(example.first_word_locs)
                    end_word_locs = list(np.cumsum([len(sent) for sent in sentences]))

                    trigger_sents_num = event_trigger[3]
                    trigger_sents_start = first_word_locs[trigger_sents_num]
                    trigger_sents_end = end_word_locs[trigger_sents_num]

                    local_seq_len = self.args.max_enc_seq_length
                    local_attention_mask = torch.zeros((local_seq_len, local_seq_len),
                                                       dtype=torch.int64)  # max_dec_seq_len*max_dec_seq_len的矩阵
                    for start_location, end_location in zip(first_word_locs, end_word_locs):
                        local_attention_mask[start_location:end_location, start_location:end_location] = 1  # 句子自己会关注自己
                        local_attention_mask[start_location:end_location,
                        trigger_sents_start:trigger_sents_end] = 1  # 当前句子关注trigger所在句子
                        local_attention_mask[trigger_sents_start:trigger_sents_end,
                        start_location:end_location] = 1  # TSAR里面是没有这里的！！！ trigger所在句子关注当前句子

                elif self.args.dataset_type in ['MLEE', 'rams']:
                    # fix rams
                    first_word_locs = copy.deepcopy(example.first_word_locs)
                    text_tmp = []
                    end_word_locs = []
                    for sentence in sentences:
                        text_tmp += sentence
                        end_word_locs.append(len(text_tmp))

                    for num, first_word_loc in enumerate(first_word_locs):
                        first_word_locs[num] = old_tok_to_new_tok_index[first_word_loc][0]
                    for num, end_word_loc in enumerate(end_word_locs):
                        end_word_locs[num] = old_tok_to_new_tok_index[end_word_loc - 1][1]

                    trigger_sents_num = event_trigger[3]
                    trigger_sents_start = first_word_locs[trigger_sents_num]
                    trigger_sents_end = end_word_locs[trigger_sents_num]

                    local_seq_len = self.args.max_enc_seq_length
                    local_attention_mask = torch.zeros((local_seq_len, local_seq_len),
                                                       dtype=torch.int64)  # max_dec_seq_len*max_dec_seq_len的矩阵
                    for start_location, end_location in zip(first_word_locs, end_word_locs):
                        local_attention_mask[start_location:end_location, start_location:end_location] = 1  # 句子自己会关注自己
                        local_attention_mask[start_location:end_location,
                        trigger_sents_start:trigger_sents_end] = 1  # 当前句子关注trigger所在句子
                        local_attention_mask[trigger_sents_start:trigger_sents_end,
                        start_location:end_location] = 1  # TSAR里面是没有这里的！！！ trigger所在句子关注当前句子
                else:
                    assert (0 == 1)

            """开始co_occur处理"""
            if self.co_occur:
                # 取得共现事件模板
                co_prompts_texts = []
                if len(event_types) <= self.args.max_co_occur_template:
                    for event_type in event_types:
                        co_prompts_texts.append(prompts[event_type].strip()) # 取得共现事件类型的模板
                if len(event_types) > self.args.max_co_occur_template:
                    event_no = random.sample(range(0, len(event_types)), 5)
                    for i in event_no:
                        co_prompts_texts.append(prompts[event_types[i]].strip())
                # 编码
                if co_prompts_texts:
                    co_prompt=''
                    for co_prompt_text in co_prompts_texts:
                        co_prompt += co_prompt_text
                        co_prompt += '\n'
                    co_prompt_tok = self.tokenizer(co_prompt)  # 对模板进行编码
                    co_prompt_ids, co_prompt_mask_ids = co_prompt_tok["input_ids"], co_prompt_tok["attention_mask"]
                    assert len(co_prompt_ids) <= self.args.max_co_occur_template_length
                    while len(co_prompt_ids) < self.args.max_co_occur_template_length:
                        co_prompt_ids.append(self.tokenizer.pad_token_id)
                        co_prompt_mask_ids.append(self.args.pad_mask_token)
                else:
                    raise ValueError(f"no prompt provided for event: {event_type}")
            else:
                co_prompt, co_prompt_ids, co_prompt_mask_ids = None, None, None

            # NOTE: one annotation as one decoding input
            # 注意这里将数据都整合成了自定义的InputFeatures数据类型
            feature_idx = len(features)
            features.append(
                    InputFeatures(example_id, feature_idx, 
                                event_type, event_trigger,
                                enc_text, enc_input_ids, enc_mask_ids, 
                                dec_prompt_text, dec_prompt_ids, dec_prompt_mask_ids,
                                arg_quries, arg_joint_prompt, target_info,
                                old_tok_to_new_tok_index=old_tok_to_new_tok_index, full_text=example.full_text, arg_list=arg_list,
                                local_attention_mask=local_attention_mask,
                                co_prompt_ids=co_prompt_ids, co_prompt_mask_ids=co_prompt_mask_ids
                    )
            )

        if os.environ.get("DEBUG", False): print('\033[91m'+f"distinct/tot arg_role: {counter[0]}/{counter[1]} ({counter[2]})"+'\033[0m')
        return features

    
    def convert_features_to_dataset(self, features):
        dataset = ArgumentExtractionDataset(features)
        return dataset