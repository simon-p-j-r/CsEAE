import json
from .processor_multiarg import MultiargProcessor


_DATASET_DIR = {
    'rams':{
        "train_file": './data/RAMS_1.0/train.jsonlines',
        "dev_file": './data/RAMS_1.0/dev.jsonlines',
        "test_file": './data/RAMS_1.0/test.jsonlines',
        "max_span_num_file": "./data/dset_meta/role_num_rams.json",
    },

    "wikievent": {
        "train_file": './data/WikiEvent/train.jsonl',
        "dev_file": './data/WikiEvent/dev.jsonl',
        "test_file": './data/WikiEvent/test.jsonl',
        "max_span_num_file": "./data/dset_meta/role_num_wikievent.json",
    },
    "MLEE": {
        "train_file": './data/MLEE/train.json',
        "dev_file": './data/MLEE/train.json',
        "test_file": './data/MLEE/test.json',
        "role_name_mapping": './data/MLEE/MLEE_role_name_mapping.json',
    },
}


def build_processor(args, tokenizer):
    if args.dataset_type not in _DATASET_DIR: 
        raise NotImplementedError("Please use valid dataset name")
    args.train_file=_DATASET_DIR[args.dataset_type]['train_file']
    args.dev_file = _DATASET_DIR[args.dataset_type]['dev_file']
    args.test_file = _DATASET_DIR[args.dataset_type]['test_file']

    args.role_name_mapping = None
    if args.dataset_type=="MLEE":
        with open(_DATASET_DIR[args.dataset_type]['role_name_mapping']) as f:
            args.role_name_mapping = json.load(f)

    processor = MultiargProcessor(args, tokenizer)
    return processor

