This is the implementation of the paper [One Small and One Large for Document-level Event Argument Extraction]


## Quick links

* [Overview](#overview)
* [Preparation](#preparation)
  * [Environment](#environment)
  * [Data](#data)
* [Run the model](#run-the-model)
  * [Quick start](#quick-start)
* [Acknowledgments](#acknowledgments)
* [Citation](#citation)
--- 
## Overview

In this work we present CsEAE and CsLLMs for document-level event argument extraction. 

We formulate highlights of CsEAE as follow:

<p align="center" width="100%">
<img src="./Figures/CsEAE.png" alt="CsEAE" style="width: 60%; height: auto; display: inline-block; margin: auto; border-radius: 40%;">
</p>

- Multiple-event prompts aid in enhancing the model's performance when dealing with complex event relationships.
- Constructing structured information by limiting the receptive field can alleviate the interference of redundant information.
- The prefix-based approach can integrate various auxiliary perceptual information.

We formulate contributions of CsLLMs as follow:

<p align="center" width="100%">
<img src="./Figures/CsLLMs_prompt.png" alt="Prompt for CsLLMs" style="width: 40%; height: auto; display: inline-block; margin: auto; border-radius: 40%;">
</p>
<!-- <p align="center" width="100%">
<img src="./Figures/CsLLMs.png" alt="CsLLMs" style="width: 60%; height: auto; display: inline-block; margin: auto; border-radius: 40%;">
</p> -->

- We designed different prompts for various datasets and further used SFT to enhance the performance of LLMs. 
- We proposed multiple datasets SFT and supplementary dataset enhancement training, which led to even better performance.
- We applied insights from SLMs to LLMs, resulting in further performance improvements. This shows that reliable insights validated on SLMs are also effective for LLMs.
--- 
## Preparation

### Environment
To run our code of CsEAE, please install all the dependency packages by using the following command:

```
pip install -r CsEAE/requirements.txt
```
All experiments run with BART_Large, You can install from [Huggingface](https://huggingface.co/facebook/bart-large).

To run our code of CsLLMs, please install all the dependency packages by using the following command:

```
pip install -r CsLLMs/requirements.txt
```
You can install the LLMs of Open-source from [Huggingface](https://huggingface.co/collections/meta-llama/meta-llama-3-66214712577ca38149ebb2b6).

### Data
We conduct experiments on three commonly used datasets: **RAMS**, **WikiEvents**, and **MLEE**.

We used the data preprocessing method from [TabEAE](https://github.com/Stardust-hyx/TabEAE). For details, please refer to the TabEAE repository. 
If you find the preprocessing steps too complicated, feel free to email me directly for the preprocessed data (except for ACE, as it is not free). 
Thanks to the creators of these datasets for making their work available!

---

## Run the Model

### Quick Start
For detailed usage and additional information, please refer to the documentation of **CsEAE** or **CsLLMs**.

--- 
## Acknowledgments
We gratefully acknowledge the contributions of Yubo Ma, I-Hung Hsu and Yuxin He for their foundational code and data preprocessing methods.
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

感谢Yubo Ma提供的基础代码：
@misc{ma2023large,
      title={Large Language Model Is Not a Good Few-shot Information Extractor, but a Good Reranker for Hard Samples!}, 
      author={Yubo Ma and Yixin Cao and YongChing Hong and Aixin Sun},
      year={2023},
      eprint={2303.08559},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
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
--- 
## Citation
Please cite our paper if you use CsEAE or CsLLMs in your work:
```bibtex

```
