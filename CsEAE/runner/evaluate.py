import torch
import logging
logger = logging.getLogger(__name__)

from utils import get_best_indexes, get_best_index


class BaseEvaluator:
    def __init__(
        self,
        cfg=None,
        data_loader=None,
        model=None,
        metric_fn_dict=None,
    ):

        self.cfg = cfg
        self.eval_loader = data_loader
        self.model = model
        self.metric_fn_dict = metric_fn_dict

    
    def _init_metric(self):
        self.metric_val_dict = {metric:None for metric in self.metric_fn_dict}

    # 得到模型对一个batch的dev/test的预测值
    def calculate_one_batch(self, batch):
        inputs, named_v = self.convert_batch_to_inputs(batch)
        with torch.no_grad():
            self.model.training = False
            _, outputs_list = self.model(inputs)
        return outputs_list, named_v

    # 调用calculate_one_batch()得到对dev/test一个batch的预测值，并调用collect_fn()方法对数据做一些整理，例如将角色与预测结果相关联等
    def evaluate_one_batch(self, batch):
        outputs_list, named_v = self.calculate_one_batch(batch)
        self.collect_fn(outputs_list, named_v, batch)

    # 初始化一些参数，然后调用evaluate_one_batch()，得到角色和预测结果的对应数据，
    # 再调用predict得到预测出来的text格式结果，并计算F1等评估数据。
    def evaluate(self):
        self.model.eval()
        self.build_and_clean_record()  # 子类定义
        self._init_metric()  # 当前类定义
        for batch in self.eval_loader:  # 运行在dev/test数据集上的结果
            self.evaluate_one_batch(batch)
        output = self.predict()
        return output


    def build_and_clean_record(self):
        raise NotImplementedError()


    def collect_fn(self, outputs_list, named_v, batch):
        raise NotImplementedError()

     
    def convert_batch_to_inputs(self, batch):
        return NotImplementedError()


    def predict(self):
        raise NotImplementedError()

# 主要是实现了上面的四个方法
class Evaluator(BaseEvaluator):
    def __init__(
        self, 
        cfg=None, 
        data_loader=None, 
        model=None, 
        metric_fn_dict=None,
        features=None,
        set_type=None,
        invalid_num=0,
    ):
        super().__init__(cfg, data_loader, model, metric_fn_dict)
        self.features = features
        self.set_type = set_type
        self.invalid_num = invalid_num

    
    def convert_batch_to_inputs(self, batch):
        if self.cfg.model_type in ["paie", 'amr']:
            inputs = {
                'input_ids':  batch[0].to(self.cfg.device),
                'enc_mask_ids':   batch[1].to(self.cfg.device), 
                'dec_prompt_ids':           batch[4].to(self.cfg.device),
                'dec_prompt_mask_ids':      batch[5].to(self.cfg.device),
                'old_tok_to_new_tok_indexs':batch[7],
                'arg_joint_prompts':        batch[8],
                'target_info':              None, 
                'arg_list':       batch[9],
                'local_attention_mask': batch[12].cuda(),
                'co_input_ids': batch[13].cuda(),
                'co_prompt_mask_ids': batch[14].cuda(),
            }
        elif self.cfg.model_type=="base":
            inputs = {
                'enc_input_ids':  batch[0].to(self.cfg.device), 
                'enc_mask_ids':   batch[1].to(self.cfg.device), 
                'decoder_prompt_ids_list':      [item.to(self.cfg.device) for item in batch[2]], 
                'decoder_prompt_mask_list': [item.to(self.cfg.device) for item in batch[3]],
                'arg_list':       batch[9],
                'decoder_prompt_start_positions_list': [item.to(self.cfg.device) for item in batch[12]],
                'decoder_prompt_end_positions_list': [item.to(self.cfg.device) for item in batch[13]],
            }

        named_v = {
            "arg_roles": batch[9],
            "feature_ids": batch[11],
        }
        return inputs, named_v


    def build_and_clean_record(self):
        self.record = {
            "feature_id_list": list(),
            "role_list": list(),
            "full_start_logit_list": list(),
            "full_end_logit_list": list()
        }

    # paie整个代码的collect_fn/collate_fn都只是对输入的数据做一些整理，并没有真的做一些改变原有数据的事。比如下属方法只是对输出的角色和结果相关联，记录到self.record里面
    def collect_fn(self, outputs_list, named_v, batch):   
        bs = len(batch[0])
        for i in range(bs):
            predictions = outputs_list[i]
            feature_id = named_v["feature_ids"][i].item()  # 当前数据集的第几个example
            for arg_role in named_v["arg_roles"][i]:
                [start_logits_list, end_logits_list] = predictions[arg_role]  # NOTE base model should also has these kind of output
                # 记录了所有role specific span selector得到的结果
                for (start_logit, end_logit) in zip(start_logits_list, end_logits_list):  # 这里将所有的数据都组成了list
                    self.record["feature_id_list"].append(feature_id)  # 最终self.record[]会记录dev/test数据集所有预测出来的start和end，然后一起送入predict计算指标
                    self.record["role_list"].append(arg_role)
                    self.record["full_start_logit_list"].append(start_logit)
                    self.record["full_end_logit_list"].append(end_logit)
    # 注意这个predict是对dev/test数据集所有的span selector一起predict
    def predict(self):
        for feature in self.features:
            feature.init_pred()
            feature.set_gt(self.cfg.model_type, self.cfg.dataset_type)

        if self.cfg.model_type=='paie' or 'amr':
            pred_list = []
            # 这个循环得到了所有span selector选择出来的start和end,存储到pred_list里面.pred_list的数据和self.record里面的数据一一对应
            for s in range(0, len(self.record["full_start_logit_list"]), self.cfg.infer_batch_size):  # 这里步长设置成了infer_batch_size，注意这个Batch_size和之前把数据feed到模型的batch_size不一样,这里这个infer_batch_size有32,它将所有的跨度选择器看作是独立的样本,然后32个32个的处理,没有说一个feature的跨度选择器必须在一起处理
                sub_max_locs, cal_time, mask_time, score_time = \
                    get_best_indexes(self.features, self.record["feature_id_list"][s:s+self.cfg.infer_batch_size], \
                    self.record["full_start_logit_list"][s:s+self.cfg.infer_batch_size], self.record["full_end_logit_list"][s:s+self.cfg.infer_batch_size], self.cfg)  # 之所以上面range将步长设置成了infer_batch_size，是因为这里一次性就会处理infer_batch_size的数据
                pred_list.extend(sub_max_locs)  # 里面存储的全是span selector选择出来的span的end和start,所以len(pred_list)==len(record['feature_id_list'])
            # 这个循环将所有span selector得到的span转化为对应于编码前的doc的span,并存储到每一个feature里面的self.pred_dict_word里面。每次处理一个论元
            for (pred, feature_id, role) in zip(pred_list, self.record["feature_id_list"], self.record["role_list"]):  # 每次获得一个span,span对应的feature的id,span对应的角色.
                pred_span = (pred[0].item(), pred[1].item())  #
                feature = self.features[feature_id]
                feature.add_pred(role, pred_span, self.cfg.dataset_type)
        else:  # 不会进入此代码块
            for feature_id, role, start_logit, end_logit in zip(
                self.record["feature_id_list"], self.record["role_list"], self.record["full_start_logit_list"], self.record["full_end_logit_list"]
            ):
                feature = self.features[feature_id]
                answer_span_pred_list = get_best_index(feature, start_logit, end_logit, \
                    max_span_length=self.cfg.max_span_length, 
                    max_span_num=int(self.cfg.max_span_num_dict[feature.event_type][role]), 
                    delta=self.cfg.th_delta)
                for pred_span in answer_span_pred_list:
                    feature.add_pred(role, pred_span, self.cfg.dataset_type)

        for metric, eval_fn in self.metric_fn_dict.items():
            perf_c, perf_i = eval_fn(self.features, self.invalid_num)
            self.metric_val_dict[metric] = (perf_c, perf_i)
            logger.info('{}-Classification. {} ({}): R {} P {} F {}'.format(
                metric, self.set_type, perf_c['gt_num'], perf_c['recall'], perf_c['precision'], perf_c['f1']))
            logger.info('{}-Identification. {} ({}): R {} P {} F {}'.format(
                metric, self.set_type, perf_i['gt_num'], perf_i['recall'], perf_i['precision'], perf_i['f1']))

        return self.metric_val_dict['span']