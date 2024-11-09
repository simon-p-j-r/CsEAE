import re
import time
import string
import random
import logging
logger = logging.getLogger(__name__)
import torch
import numpy as np
from scipy.optimize import linear_sum_assignment


MAX_NUM_EVENTS = 20
EXTERNAL_TOKENS = ['<t--1>', '</t--1>', '<t>', '</t>']
for i in range(MAX_NUM_EVENTS):
    EXTERNAL_TOKENS.append('<t-%d>' % i)
    EXTERNAL_TOKENS.append('</t-%d>' % i)
_PREDEFINED_QUERY_TEMPLATE = "Argument: {arg:}. Trigger: {trigger:} "

def set_seed(args):
    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)


def count_time(f):
    def run(**kw):
        time1 = time.time()
        result = f(**kw)
        time2 = time.time()
        logger.info("The time of executing {}: {}".format(f.__name__, time2-time1))
        return result
    return run


def hungarian_matcher(predicted_spans, target_spans):
    """
    Args:
        predictions: prediction of one arg role type, list of [s,e]
        targets: target of one arg role type, list of [s,e]
    Return:
        (index_i, index_j) where index_i in prediction, index_j in target 
    """
    # L1 cost between spans, torch.cdist(x1,x2,p=2)批量计算两个向量集合的距离。其中， x1和x2是输入的两个向量集合。p 默认为2，为欧几里德距离。如果x1的shape是 [B,P,M], x2的shape是[B,R,M]，则cdist的结果shape是 [B,P,R]
    cost_spans = torch.cdist(torch.FloatTensor(predicted_spans).unsqueeze(0), torch.FloatTensor(target_spans).unsqueeze(0), p=1)
    indices = linear_sum_assignment(cost_spans.squeeze(0)) 
    return [torch.as_tensor(indices[0], dtype=torch.int64), torch.as_tensor(indices[1], dtype=torch.int64)]

# 对抽取出来的text做一些标准化，这里不行！！会把评价指标数据抬高,TabEAE舍弃text这个指标
def _normalize_answer(s):
    """Lower text and remove punctuation, articles and extra whitespace. (Squad Style) """
    def remove_articles(text):  # 删除特殊字符
        # 使用 compile 函数将正则表达式的字符串形式编译为一个Pattern对象
        # re.sub用于将匹配到的pattern中的字符都替换成指定字符，其中必须传入的三个参数：
        # （1）pattern：该参数表示正则中的模式字符串；
        # （2）repl：该参数表示要替换的字符串（即匹配到pattern后替换为repl），也可以是个函数；
        # （3）string：该参数表示要被处理（查找替换）的原始字符串；
        regex = re.compile(r'\b(a|an|the)\b', re.UNICODE)
        return re.sub(regex, ' ', text)
    def white_space_fix(text):  # 删除空格
        return ' '.join(text.split())
    def remove_punc(text):  # 删除标点符号
        exclude = set(string.punctuation)  # 得到text中可能会有的所有标点符号
        return ''.join(ch for ch in text if ch not in exclude)  # 然后删了
    def lower(text):  # 整成小写的
        return text.lower()
    s_normalized = white_space_fix(remove_articles(remove_punc(lower(s))))
    return s_normalized


def get_best_span(start_logit, end_logit, old_tok_to_new_tok_index, max_span_length):
    # time consuming
    best_score = start_logit[0] + end_logit[0]
    best_answer_span = (0, 0)
    context_length = len(old_tok_to_new_tok_index)

    for start in range(context_length):
        for end in range(start+1, min(context_length, start+max_span_length+1)):
            start_index = old_tok_to_new_tok_index[start][0] # use start token idx
            end_index = old_tok_to_new_tok_index[end-1][1] 

            score = start_logit[start_index] + end_logit[end_index]
            answer_span = (start_index, end_index)
            if score > best_score:
                best_score = score
                best_answer_span = answer_span

    return best_answer_span


def get_best_span_simple(start_logit, end_logit):
    # simple constraint version
    _, s_idx = torch.max(start_logit, dim=0)
    _, e_idx = torch.max(end_logit[s_idx:], dim=0)  # 这个e_idx是相对于s_idx往后移几个
    return [s_idx, s_idx+e_idx]


def get_sentence_idx(first_word_locs, word_loc):
    sent_idx = -1
    for i, first_word_loc in enumerate(first_word_locs):
        if word_loc>=first_word_loc:
            sent_idx = i
        else:
            break
    return sent_idx

# 实现C
def get_maxtrix_value(X):
    """
    input: batch of matrices. [B, M, N]
    output: indexes of argmax for each matrix in batch. [B, 2]
    """
    t1 = time.time()
    col_max, col_max_loc = X.max(dim=-1)
    _, row_max_loc = col_max.max(dim=-1)  # 实现公式7,成功找到batch_size predicted span of batch_size slot and span selector
    t2 = time.time()
    cal_time = (t2-t1)

    row_index = row_max_loc
    col_index = col_max_loc[torch.arange(row_max_loc.size(0)), row_index]  # torch.arange(row_max_loc.size(0))=[0, 1, 2, ..., 30, 31]

    return torch.stack((row_index, col_index)).T, cal_time

# 由evaluate.py中的predict()方法调用。传进来的是当前set所有的features，feature_id_list，start_logit_list，end_logit_list都是一个batch的,这个方法实现了Inference中提到的两个公式,抽取出了预测出来的论元的start和end
def get_best_indexes(features, feature_id_list, start_logit_list, end_logit_list, args):
    t1 = time.time()
    start_logits = torch.stack(tuple(start_logit_list)).unsqueeze(-1)         # [B, M, 1]
    end_logits = torch.stack(tuple(end_logit_list)).unsqueeze(1)              # [B, 1, M] 注意这两个的维度不一样！！！
    scores = (start_logits + end_logits).float()  # 这里实现了公式6,上面维度为1的位置加的很巧妙,这样确实广播到了所有i和j的可能,但是不是正常的span,是穷举的span,所以下面会有mask的生成
    t2 = time.time()
    score_time = t2 - t1
    # 枚举所有span,实现论文中Inference所说的C
    def generate_mask(feature):  # 传进来一个feature
        mask = torch.zeros((args.max_enc_seq_length, args.max_enc_seq_length), dtype=float, device=args.device)
        context_length = len(feature.old_tok_to_new_tok_index)
        for start in range(context_length):
            start_index = feature.old_tok_to_new_tok_index[start][0]
            end_index_list = [feature.old_tok_to_new_tok_index[end-1][1] for end in range(start+1, min(context_length, start+args.max_span_length+1))]  # 这个args.max_span_length就是论文中说的threshold l
            mask[start_index, end_index_list] = 1.0
        mask[0][0] = 1.0
        return torch.log(mask).float().unsqueeze(0)
    
    t1 = time.time()
    candidate_masks = {feature_id:generate_mask(features[feature_id]) for feature_id in set(feature_id_list)}  # 注意这里做了一个set操作,所以是为每一个feature做了一个C
    masks = torch.cat([candidate_masks[feature_id] for feature_id in feature_id_list], dim=0)  # 虽然获得了针对每一个feature的C,但是其实这些C要与span selector相乘获得候选span,所以这里为每一个span selector制作了一个C

    t2 = time.time()
    mask_time = t2-t1
    masked_scores = scores + masks
    max_locs, cal_time = get_maxtrix_value(masked_scores)
    max_locs = [tuple(a) for a in max_locs]

    return max_locs, cal_time, mask_time, score_time


def get_best_index(feature, start_logit, end_logit, max_span_length, max_span_num, delta):
    th = start_logit[0] + end_logit[0]
    answer_span_list = []
    context_length = len(feature.old_tok_to_new_tok_index)

    for start in range(context_length):
        for end in range(start+1, min(context_length, start+max_span_length+1)):
            start_index = feature.old_tok_to_new_tok_index[start][0] # use start token idx
            end_index = feature.old_tok_to_new_tok_index[end-1][1] 

            score = start_logit[start_index] + end_logit[end_index]
            answer_span = (start_index, end_index, score)

            if score > (th+delta):
                answer_span_list.append(answer_span)
    
    if not answer_span_list:
        answer_span_list.append((0, 0, th))
    return filter_spans(answer_span_list, max_span_num)


def filter_spans(candidate_span_list, max_span_num):
    candidate_span_list = sorted(candidate_span_list, key=lambda x:x[2], reverse=True)
    candidate_span_list = [(candidate_span[0], candidate_span[1]) for candidate_span in candidate_span_list]

    def is_intersect(span_1, span_2):
        return False if min(span_1[1], span_2[1]) < max(span_1[0], span_2[0]) else True

    if len(candidate_span_list) == 1:
        answer_span_list = candidate_span_list
    else:
        answer_span_list = []
        while candidate_span_list and len(answer_span_list)<max_span_num:
            selected_span = candidate_span_list[0]
            answer_span_list.append(selected_span)
            candidate_span_list = candidate_span_list[1:]  

            candidate_span_list = [candidate_span for candidate_span in candidate_span_list if not is_intersect(candidate_span, selected_span)]
    return answer_span_list


def check_tensor(tensor, var_name):
    print("******Check*****")
    print("tensor_name: {}".format(var_name))
    print("shape: {}".format(tensor.size()))
    if len(tensor.size())==1 or tensor.size(0)<=3:
        print("value: {}".format(tensor))
    else:
        print("part value: {}".format(tensor[0,:]))
    print("require_grads: {}".format(tensor.requires_grad))
    print("tensor_type: {}".format(tensor.dtype))


from spacy.tokens import Doc
class WhitespaceTokenizer:
    def __init__(self, vocab):
        self.vocab = vocab

    def __call__(self, text):
        words = text.split(" ")
        return Doc(self.vocab, words=words)


def find_head(arg_start, arg_end, doc):
    arg_end -= 1
    cur_i = arg_start
    while doc[cur_i].head.i >= arg_start and doc[cur_i].head.i <=arg_end:
        if doc[cur_i].head.i == cur_i:
            # self is the head 
            break 
        else:
            cur_i = doc[cur_i].head.i
        
    arg_head = cur_i
    head_text = doc[arg_head]
    return head_text