# CsLLMs (**C**o and **S**tructure **L**arge **L**anguage **M**odels)

This is the implementation of **CsLLMs** in [One Small and One Large for Document-level Event Argument Extraction]

If you have any question about this work, feel free to contact 1354527247@qq.com (Jiaren Peng)

## Prerequisite
**Environment**
* python 3.10.5
* torch 2.0.1
* openai 1.6.1
* Transformers 4.37.1
* backoff
* sentencepiece

**OpenAI API key**
```
It you use models of OpenAI as the LLMs, please set up your openAI API key by:

修改LLM_wrapper.py顶部的：
client = OpenAI(
    api_key='Your own API',
    base_url="https://..."
)
```

## Datasets
**RAMS**
请按照
[TabEAE](https://github.com/Stardust-hyx/TabEAE)
的方法进行数据预处理

**WikiEvents**
请按照
[TabEAE](https://github.com/Stardust-hyx/TabEAE)
的方法进行数据预处理

**MLEE**
请按照
[TabEAE](https://github.com/Stardust-hyx/TabEAE)
的方法进行数据预处理

**ACE**
请按照
[TabEAE](https://github.com/Stardust-hyx/TabEAE)
的方法进行数据预处理

**GENEVA**
直接拿过来就行，原数据集已经处理的很好了。

```
以上数据集的预处理，如果你觉得太麻烦，可以email给我，直接找我要，ACE除外，这个数据集不是免费的。感谢上述数据集的制作者们！
```


## Quick start
```
注意，你需要修改run.py中的：
# data_type: 你使用的数据集名称 and must in [ACE, WikiEvent, RAMS, MLEE, GENEVA]
# train_res_path: 数据集的训练集地址
# test_res_path: 数据集的测试集地址
# model_name: 使用的LLMs地址

然后直接运行run.py即可
```

## Thanks
```bibtex
感谢Yubo Ma提供的基础代码：
@misc{ma2023large,
      title={Large Language Model Is Not a Good Few-shot Information Extractor, but a Good Reranker for Hard Samples!}, 
      author={Yubo Ma and Yixin Cao and YongChing Hong and Aixin Sun},
      year={2023},
      eprint={2303.08559},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}

感谢Yubo Ma提供的数据预处理方法：
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
@misc{peng2024smalllargedocumentlevelevent,
      title={One Small and One Large for Document-level Event Argument Extraction}, 
      author={Jiaren Peng and Hongda Sun and Wenzhong Yang and Fuyuan Wei and Liang He and Liejun Wang},
      year={2024},
      eprint={2411.05895},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2411.05895}, 
}
```
