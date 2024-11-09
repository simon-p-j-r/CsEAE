# CsEAE (**C**o and **S**tructure **E**vent **A**rgument **E**xtraction)
This is the implementation of CsEAE in the paper [One Small and One Large for Document-level Event Argument Extraction]
If you have any question about this work, feel free to contact 1354527247@qq.com (Jiaren Peng)

## Quick links

* [Overview](#overview)
* [Preparation](#preparation)
  * [Environment](#environment)
  * [Data](#data)
* [Run the model](#run-the-model)
  * [Quick start](#quick-start)
  * [Experiments with multiple runs](#experiments-with-multiple-runs)
* [Citation](#citation)

## Overview
Document-level Event Argument Extraction (EAE) faces numerous challenges compared to sentence-level EAE due to the surge in input text. In this paper, we primarily address two issues: a) difficulty in distinguishing semantic boundaries between events, b) dispersion of attention caused by redundant information. To tackle these problems, we propose a **C**o and **S**tructure aware generative-based of **E**vent **A**rgument **E**xtraction model (**CsEAE**).


## Preparation

### Environment

```
python==3.8.17
torch==2.0.1
transformers==4.18.0
spacy==3.6.1
scipy==1.5.4
pem,am==1.2.2
networkx==3.1
jsonlines==2.0.0
tqdm==4.66.1
ipdb==0.13.9
```


### Data
We conduct experiments on 3 datasets: RAMS, WikiEvents and MLEE.
请按照
[TabEAE](https://github.com/Stardust-hyx/TabEAE)
的方法进行数据预处理


Please make sure your data folder structure as below.
```bash
data
  ├── RAMS_1.0
  │   ├── train.jsonlines
  │   ├── dev.jsonlines
  │   └── test.jsonlines
  ├── WikiEvent
  │   ├── train.jsonl
  │   ├── dev.jsonl
  │   └── test.jsonl
  ├── MLEE
  │   ├── train.json
  │   └── test.json
  ├── prompts
  │   ├── prompts_ace_full.csv
  │   ├── prompts_wikievent_full.csv
  │   └── prompts_rams_full.csv
  └── dset_meta
      ├── description_ace.csv
      ├── description_rams.csv
      └── description_wikievent.csv
```

## Run the model

### Quick start
You could simply run PAIE with following commands: 
```bash
bash ./scripts/train_{mlee|rams|wikievent}_large.sh
```
Folders will be created automatically to store: 

1. Subfolder `checkpoint`: model parameters with best dev set result
2. File `log.txt`: recording hyper-parameters, training process and evaluation result
3. File `best_dev_results.log`/`best_test_related_results.log`: showing prediction results of checkpoints on every sample in dev/test set.

You could see hyperparameter setting in `./scripts/train_[dataset]_large.sh` and `config_parser.py`. We give most of hyperparameters a brief explanation in `config_parser.py`.

Above three scripts train models with BART-Large. If you want to train models with it, please change `--model_name_or_path` from [Huggingface](https://huggingface.co/facebook/bart-large) and run following commands:
```bash
bash ./scripts/train_{ace|rams|wikievent}_large.sh
```

### Experiments with multiple runs

You could run experiments multiple times to get a more stable and reliable results.

```bash
for seed in 13 21 42 88 100 3401
do
    for lr in 1e-5 2e-5 3e-5 5e-5
    do
        bash ./scripts/train_{mlee|rams|wikievent}_large.sh $seed $lr
    done
done
```

## Acknowledgments
We gratefully acknowledge the contributions of Yubo Ma, I-Hung Hsuand Yuxin He for their foundational code and data preprocessing methods.
```bibtex
感谢Yubo Ma提供的基础代码：
@inproceedings{ma-etal-2022-prompt,
    title = "{P}rompt for Extraction? {PAIE}: {P}rompting Argument Interaction for Event Argument Extraction",
    author = "Ma, Yubo  and
      Wang, Zehao  and
      Cao, Yixin  and
      Li, Mukai  and
      Chen, Meiqi  and
      Wang, Kun  and
      Shao, Jing",
    booktitle = "Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
    month = may,
    year = "2022",
    address = "Dublin, Ireland",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2022.acl-long.466",
    doi = "10.18653/v1/2022.acl-long.466",
    pages = "6759--6774",
}

感谢I-Hung Hsu提供的基础代码：
@inproceedings{acl2023ampere,
    author    = {I-Hung Hsu and Zhiyu Xie and Kuan-Hao Huang and Premkumar Natarajan and Nanyun Peng},
    title     = {AMPERE: AMR-Aware Prefix for Generation-Based Event Argument Extraction Model},
    booktitle = {Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (ACL)},
    year      = {2023},
}

感谢yuxin He提供的数据预处理方法：
@inproceedings{he-etal-2023-revisiting,
    title = "Revisiting Event Argument Extraction: Can {EAE} Models Learn Better When Being Aware of Event Co-occurrences?",
    author = "He, Yuxin  and
      Hu, Jingyue  and
      Tang, Buzhou",
    booktitle = "Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
    month = jul,
    year = "2023",
    address = "Toronto, Canada",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.acl-long.701",
    pages = "12542--12556",
}
```
## Citation
Please cite our paper if it is helpful for your work:
```bibtex
@misc{
}
```
