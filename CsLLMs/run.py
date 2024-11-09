import os
import json
import argparse
from utils import eval_score, set_seed
from preprocess import get_res_list

from prompr2instance.prompt2instance import rerank
os.environ["CUDA_VISIBLE_DEVICES"] = "4"


if __name__ == "__main__": 
    parser = argparse.ArgumentParser()

    parser.add_argument("--data_type", default="ACE", type=str)
    parser.add_argument("--train_res_path", default="./datasets/ace_eeqa/train_convert.json", type=str)
    parser.add_argument("--test_res_path", default="./datasets/ace_eeqa/test_convert.json", type=str)
    # parser.add_argument("--data_type", default="WikiEvent", type=str)
    # parser.add_argument("--train_res_path", default="./datasets/WikiEvent/train.jsonl", type=str)
    # parser.add_argument("--test_res_path", default="./datasets/WikiEvent/test.jsonl", type=str)
    # parser.add_argument("--data_type", default="RAMS", type=str)
    # parser.add_argument("--train_res_path", default="./datasets/RAMS/train.jsonlines", type=str)
    # parser.add_argument("--test_res_path", default="./datasets/RAMS/test.jsonlines", type=str)
    # parser.add_argument("--data_type", default="MLEE", type=str)
    # parser.add_argument("--train_res_path", default="./datasets/MLEE/train.json", type=str)
    # parser.add_argument("--test_res_path", default="./datasets/MLEE/test.json", type=str)
    # parser.add_argument("--data_type", default="GENEVA", type=str)
    # parser.add_argument("--train_res_path", default="./datasets/GENEVA/train.json", type=str)
    # parser.add_argument("--test_res_path", default="./datasets/GENEVA/test.json", type=str)

    # CsLLMs
    parser.add_argument("--occur", default=True, type=bool)
    parser.add_argument("--structure", default=True, type=bool)

    # parser.add_argument("--model_name", default="../../bert/Llama-3-8B-Instruct", type=str)
    # parser.add_argument("--model_name", default="../../bert/Meta-Llama-3-8B", type=str)
    parser.add_argument("--model_name", default="gpt-3.5-turbo-0125", type=str)
    # parser.add_argument("--model_name", default="gpt-4o", type=str)
    # parser.add_argument("--model_name", default="gpt-4o-mini", type=str)

    parser.add_argument("--output_path", default="./outputs/", type=str)
    parser.add_argument("--batch_size", default=4, type=int)
    parser.add_argument("--temperature", default=0.0, type=float)
    parser.add_argument("--seed", default=42, type=int)
    parser.add_argument("--device", default="cuda", type=str)

    args = parser.parse_args()
    set_seed(args.seed)
    if not os.path.exists(args.output_path):
        os.makedirs(args.output_path)

    res_list_test = get_res_list(args.test_res_path, args, dataset_type=args.data_type, train=False)
    # res_list_train = get_res_list(args.train_res_path, args, dataset_type = args.data_type, train=True)
    res_list_train=None
    # res_list_test = None
    rerank_gt_list, rerank_pred_list, rerank_output_list = rerank(
        args, 
        res_list=res_list_test,
        res_list_train=res_list_train,
    )

    res_classification, res_identification = eval_score(gt_list_all=rerank_gt_list, pred_list_all=rerank_pred_list, rerank_output_list=rerank_output_list)
    print(res_identification['f1'], res_classification['f1'])
    with open(os.path.join(args.output_path, "all-cs-geneva.json"), 'w', encoding='utf-8') as f:
        json.dump(rerank_pred_list, f, ensure_ascii=False)