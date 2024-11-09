import os
# os.environ['MKL_SERVICE_FORCE_INTEL'] = "0"
os.environ["CUDA_VISIBLE_DEVICES"] = "6"
if os.environ.get('DEBUG', False): print('\033[92m'+'Running code in DEBUG mode'+'\033[0m')
import logging

from models import build_model
from processors import build_processor
from utils import set_seed
from runner.runner import Runner

logger = logging.getLogger(__name__)


def run(args, model, processor, optimizer, scheduler):
    set_seed(args)

    # 开始初始化Dataloader,注意初始化Dataloader是每个数据集都会做的,所以 这里是在父类定义的方法
    logger.info("train dataloader generation")
    train_examples, train_features, train_dataloader, args.train_invalid_num = processor.generate_dataloader('train')
    print('train finish')
    logger.info("dev dataloader generation")
    dev_examples, dev_features, dev_dataloader, args.dev_invalid_num = processor.generate_dataloader('dev')
    print('dev finish')
    logger.info("test dataloader generation")
    test_examples, test_features, test_dataloader, args.test_invalid_num = processor.generate_dataloader('test')
    print('test finish')

    runner = Runner(
        cfg=args,
        data_samples=[train_examples, dev_examples, test_examples],
        data_features=[train_features, dev_features, test_features],
        data_loaders=[train_dataloader, dev_dataloader, test_dataloader],
        model=model,
        optimizer=optimizer,
        scheduler=scheduler,
        metric_fn_dict=None,
    )
    runner.run()


def main():
    from config_parser import get_args_parser
    args = get_args_parser()

    if not args.inference_only:
        print(f"Output full path {os.path.join(os.getcwd(), args.output_dir)}")
        if not os.path.exists(args.output_dir):
            os.makedirs(args.output_dir)

        logging.basicConfig(
            filename=os.path.join(args.output_dir, "log.txt"), \
            format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s', \
            datefmt='%m/%d/%Y %H:%M:%S', level = logging.INFO
            )
    else:
        logging.basicConfig(
            format = '%(asctime)s - %(levelname)s - %(name)s -   %(message)s', \
            datefmt = '%m/%d/%Y %H:%M:%S', level = logging.INFO
            )
    set_seed(args)

    model, tokenizer, optimizer, scheduler = build_model(args, args.model_type) 
    model.cuda() # 什么时候能有卡啊啊啊啊

    processor = build_processor(args, tokenizer)

    logger.info("Training/evaluation parameters %s", args)
    run(args, model, processor, optimizer, scheduler)
            

if __name__ == "__main__":
    main()