This is the implementation of the paper [One Small and One Large for Document-level Event Argument Extraction]


## Quick links

* [Overview](#overview)
* [Preparation](#preparation)
  * [Environment](#environment)
  * [Data](#data)
* [Run the model](#run-lm-bff)
  * [Quick start](#quick-start)
* [Citation](#citation)

## Overview

In this work we present CsEAE and CsLLMs for document-level event argument extraction. 

We formulate highlights of CsEAE as follow:

<p align="center" width="100%">
<img src="./Figures/CsEAE.png" alt="CsEAE" style="width: 60%; height: auto; display: inline-block; margin: auto; border-radius: 40%;">
</p>

- Multiple-event prompts aid in enhancing the model's performance when dealing with complex event relationships.
- Constructing structured information by limiting the receptive field can alleviate the interference of redundant information.
- The prefix-based approach can integrate various auxiliary perceptual information.

We formulate highlights of CsLLMs as follow:

<p align="center" width="100%">
<img src="./Figures/CsLLMs_prompt.png" alt="Prompt for CsLLMs" style="width: 40%; height: auto; display: inline-block; margin: auto; border-radius: 40%;">
</p>
<p align="center" width="100%">
<img src="./Figures/CsLLMs.png" alt="CsLLMs" style="width: 60%; height: auto; display: inline-block; margin: auto; border-radius: 40%;">
</p>

- We designed different prompts for various datasets and further used SFT to enhance the performance of LLMs. 
- We proposed multiple datasets SFT and supplementary dataset enhancement training, which led to even better performance.
- We applied insights from SLMs to LLMs, resulting in further performance improvements. This shows that reliable insights validated on SLMs are also effective for LLMs.

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
We conduct experiments on three common datasets: RAMS, WIKIEVENTS and MLEE.

## Run the model

### Quick start
You could simply run CsEAE with following commands: 
```bash
bash .CsEAE/scripts/train_{mlee|rams|wikievent}_large.sh
```
Folders will be created automatically to store: 

1. Subfolder `checkpoint`: model parameters with best dev set result.
2. File `log.txt`: recording hyper-parameters, training process and evaluation result.
3. File `best_dev_results.log`/`best_test_related_results.log`: showing prediction results of checkpoints on every sample in dev/test set.

You could see hyperparameter setting in `./scripts/train_[dataset].sh` and `config_parser.py`. We give most of hyperparameters a brief explanation in `config_parser.py`.



## Citation
Please cite our paper if you use CsEAE in your work:
```bibtex

```
