import sys
sys.path.append("../../")
import copy
import logging
logger = logging.getLogger(__name__)

from transformers import BartConfig, BartTokenizerFast
from transformers import AdamW, get_linear_schedule_with_warmup
from utils import EXTERNAL_TOKENS
from processors.processor_multiarg import MultiargProcessor
from .csmodel import GenerativeModel


MODEL_CLASSES = {
    'amr': (BartConfig, GenerativeModel, BartTokenizerFast)
}


def build_model(args, model_type):
    config_class, model_class, tokenizer_class = MODEL_CLASSES[model_type]
    if args.inference_only:
        config = config_class.from_pretrained(args.inference_model_path)  # 如果是推理阶段，这里会读取checkpoint的模型
    else:
        config = config_class.from_pretrained(args.model_name_or_path)

    config.model_name_or_path = args.model_name_or_path
    config.device = args.device
    config.context_representation = args.context_representation

    # length
    config.max_enc_seq_length = args.max_enc_seq_length  # encoder输入的最大长度
    config.max_dec_seq_length= args.max_dec_seq_length  # decoder输入的最大长度
    config.max_prompt_seq_length=args.max_prompt_seq_length  # prompt的最大长度
    config.max_span_length = args.max_span_length  # span text的最大长度，也就是论元最多是由多少个单词组成的

    config.bipartite = args.bipartite
    config.matching_method_train = args.matching_method_train

    config.ignore_first_header= args.ignore_first_header
    config.use_encoder_prefix= args.use_encoder_prefix
    config.use_cross_prefix = args.use_cross_prefix
    config.use_decoder_prefix = args.use_decoder_prefix
    config.latent_dim = args.latent_dim
    config.prefix_length = args.prefix_length

    # mask
    config.use_local_mask = args.use_local_mask

    # co_occur
    config.co_occur = args.co_occur

    tokenizer = tokenizer_class.from_pretrained(args.model_name_or_path, add_special_tokens=True)
    # 注意一般调用PLM都是用类似于：
    # self.model = AutoModelForPreTraining.from_pretrained(config.model_name, cache_dir=config.cache_dir, config=self.model_config)
    # 但是这里调用PLM用的是PAIE.from_pretrained，相当于在transformers里面注册了一个model，调用transformers的from_pretrained方法来初始化这个model
    if args.inference_only:
        model = model_class.from_pretrained(args.inference_model_path, from_tf=bool('.ckpt' in args.inference_model_path), config=config)
    elif model_type == 'amr':
        model = GenerativeModel(config, tokenizer)
    else:
        model = model_class.from_pretrained(args.model_name_or_path, from_tf=bool('.ckpt' in args.model_name_or_path), config=config)

    # Add trigger special tokens and continuous token (maybe in prompt)
    new_token_list = copy.deepcopy(EXTERNAL_TOKENS)
    prompts = MultiargProcessor._read_prompt_group(args.prompt_path)  # 返回了一个模板构成的字典：{事件类型:prompt}
    for event_type, prompt in prompts.items():
        token_list = prompt.split()
        for token in token_list:  # 这里是为了判断prompt中有没有类似于‘<t>’这样的特殊符号
            if token.startswith('<') and token.endswith('>') and token not in new_token_list:  # new_token_list：['<t>', '</t>']
                new_token_list.append(token)  # 记录prompt中的特殊字符
    tokenizer.add_tokens(new_token_list)  # 将prompt中的特殊字符都加进tokenizer
    logger.info("Add tokens: {}".format(new_token_list))

    if model_type == 'amr':
        # 这里的model是GenerativeModel
        # model.model是AMRPrefixGenCopyReg
        model.model.model.resize_token_embeddings(len(tokenizer))
    else:
        model.resize_token_embeddings(len(tokenizer))  # tokenizer.add_tokens之后需要改变其embedding，两句代码配合使用

    # 判断是训练阶段还是推理阶段
    if args.inference_only:
        optimizer, scheduler = None, None
    else:

        param_groups = [{'params': [p for n, p in model.named_parameters() if "projector" in n],
                         'lr': 2e-5, 'weight_decay': 1e-5},
                        {'params': [p for n, p in model.named_parameters() if "projector" not in n],
                         'lr': args.learning_rate, 'weight_decay': args.weight_decay}]

        optimizer = AdamW(params=param_groups)
        scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=args.max_steps*args.warmup_steps, num_training_steps=args.max_steps)

    return model, tokenizer, optimizer, scheduler