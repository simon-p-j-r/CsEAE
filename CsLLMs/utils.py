import re

import jsonlines
import torch
import numpy as np
from random import seed
from collections import Counter, defaultdict
import copy


def set_seed(args):
    if isinstance(args, int):
        seed(args)
        np.random.seed(args)
        torch.manual_seed(args)
    else:
        seed(args.seed)
        np.random.seed(args.seed)
        torch.manual_seed(args.seed)

def eval_rpf(gt_num, pred_num, correct_num):
    recall = correct_num/gt_num if gt_num!=0 else .0
    precision = correct_num/pred_num if pred_num!=0 else .0
    f1 = 2*recall*precision/(recall+precision) if (recall+precision)>1e-4 else .0
    res = {
        "recall": recall, "precision": precision, "f1": f1,
        "gt_num": gt_num, "pred_num": pred_num, "correct_num": correct_num,
    }
    return res

# 计算p,r,f1的
def eval_score(gt_list_all, pred_list_all, rerank_output_list):
    gt_num, pred_num, correct_num = 0, 0, 0
    gt_num_identify, pred_num_identify, correct_identify_num = 0, 0, 0
    for num, output_list in enumerate(rerank_output_list):
        pred = pred_list_all[num]
        gt = gt_list_all[num]

        all_pred_list = list()
        all_gt_list = list()

        for role in output_list['role_name']:
            gt_list = gt[role] if role in gt else list()  # text ground truth
            try:
                pred_list = list(set(pred[role])) if (role in pred) and (pred[role] is not None) else list()  # 存储针对这个feature预测出来的span对应于编码前的doc的start和end
            except:
                pred_list = list()
            gt_num += len(gt_list)
            pred_num += len(pred_list)

            for gt_words in gt_list:
                if gt_words in pred_list:
                    correct_num += 1

            all_pred_list.extend(copy.deepcopy(pred_list))
            all_gt_list.extend(gt_list)

        all_pred_list = list(set(all_pred_list))
        all_gt_list = list(set(all_gt_list))
        pred_num_identify += len(all_pred_list)
        gt_num_identify += len(all_gt_list)
        for gt_span in all_gt_list:
            if gt_span in all_pred_list:
                correct_identify_num += 1

    res_classification = eval_rpf(gt_num, pred_num, correct_num)
    res_identification = eval_rpf(gt_num_identify, pred_num_identify, correct_identify_num)
    return res_classification, res_identification


def ensemble_pred_res(pred_list, repeat_time, occur_th=0, task='ED'):
    ensemble_pred_list, ensemble_counter_list = list(), list()
    pred_list_list = list_merge(pred_list, repeat_time)
    
    for pred_list_this_example in pred_list_list:
        ensemble_pred = list()
        if task in ['ED', 'NER']:  # False
            span_counter = defaultdict(list) 
            for pred_list_one_trace in pred_list_this_example:
                if pred_list_one_trace=="failed":
                    continue
                for label, span in pred_list_one_trace:
                    span_counter[span].append(label)
            for span, labels in span_counter.items():
                voted_label, occur_time = Counter(labels).most_common(1)[0]
                if occur_time>occur_th:
                    ensemble_pred.append((voted_label, span))
            ensemble_pred_list.append(ensemble_pred)
            ensemble_counter_list.append(
                {span:Counter(labels).most_common() for span, labels in span_counter.items()}
            )
        elif task=="EE":  # False
            span_counter = defaultdict(list) 
            for pred_list_one_trace in pred_list_this_example:
                if pred_list_one_trace=="failed":
                    continue
                for event, trigger, label, span in pred_list_one_trace:
                    key = "___|___".join([event, trigger, span])
                    span_counter[key].append(label)
            for key, labels in span_counter.items():
                event, trigger, span = key.split("___|___")
                voted_label, occur_time = Counter(labels).most_common(1)[0]
                if occur_time>occur_th:
                    ensemble_pred.append((event, trigger, voted_label, span))
            ensemble_pred_list.append(ensemble_pred)
            ensemble_counter_list.append(
                {span:Counter(labels).most_common() for key, labels in span_counter.items()}
            )
        else:  # True
            relation_counter = Counter([pred for pred in pred_list_this_example if pred!="failed"]).most_common()  # 计算列表中元素出现的频数，返回的结果是元组列表，不是字典.
            if not relation_counter:
                voted_label = "None"
            else:
                voted_label, occur_time = relation_counter[0]
                if occur_time<=occur_th:
                    voted_label = "None"
            ensemble_pred_list.append(voted_label)
            ensemble_counter_list.append(relation_counter)       

    return ensemble_pred_list, ensemble_counter_list


def list_merge(input_list, repeat_time):
    merged_list = list()
    assert(len(input_list)%repeat_time==0)
    for idx, input in enumerate(input_list):
        pred_idx, repeat_idx = idx//repeat_time, idx%repeat_time
        if repeat_idx==0:
            merged_list.append(list())
        merged_list[pred_idx].append(input)
    return merged_list


def parse_res(raw_res, datatype):

    if raw_res.startswith('```'):
        str4 = raw_res.split('```')
        str5 = str4[1]
        str6 = str5.split('json')
        raw_res = str6[1]
    if raw_res.startswith('Response: '):
        str4 = raw_res.split('Response: ')
        raw_res = str4[1]
    if raw_res.startswith('Output: '):
        str4 = raw_res.split('Output: ')
        raw_res = str4[1]
    if raw_res.startswith('Output:'):
        str4 = raw_res.split('Output:')
        raw_res = str4[1]
    if raw_res.startswith('Answer:'):
        str4 = raw_res.split('Answer:')
        raw_res = str4[1]
    if raw_res.startswith('Solution: '):
        str4 = raw_res.split('Solution: ')
        raw_res = str4[1]
    if raw_res.startswith('Events:'):
        str4 = raw_res.split('Events:')
        raw_res = str4[1]
    if raw_res.startswith('Please output: '):
        str4 = raw_res.split('Please output: ')
        raw_res = str4[1]
    if raw_res.startswith('You need to output: '):
        str4 = raw_res.split('You need to output: ')
        raw_res = str4[1]
    if raw_res.startswith('Please output:'):
        str4 = raw_res.split('Please output:')
        raw_res = str4[1]
    if raw_res.startswith('You need to output:'):
        str4 = raw_res.split('You need to output:')
        raw_res = str4[1]
    if raw_res.startswith('What is the output?'):
        str4 = raw_res.split('What is the output?')
        raw_res = str4[1]


    raw_res = raw_res.replace('null', 'None')
    pred = eval(raw_res)

    for pre in pred:
        args = pred[pre]
        if isinstance(args, str):
            if datatype == 'Finance':
                args = list(args.split('、'))
            else:
                args = list(args.split(', '))
        if isinstance(args, int):
            args=[args]
        pred[pre] = args

    return pred