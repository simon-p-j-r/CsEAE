import logging, os
import numpy as np
import torch
import torch.nn as nn
from transformers import AutoConfig, AutoModelForPreTraining
from transformers.modeling_outputs import BaseModelOutput
from .model_copyutils import CopyBartWithReg
from .prefix_gen_bart import PrefixGenBartForConditionalGeneration
from .projector import Projector
import ipdb

logger = logging.getLogger(__name__)


class GenerativeModel(nn.Module):
    def __init__(self, config, tokenizer):
        super().__init__()
        self.config = config
        self.tokenizer = tokenizer
        self.model = AMRPrefixGenCopyReg(config, tokenizer)


    def forward(self, batch):
        return self.model(batch)

    def predict(self, batch, num_beams=4, max_length=50):
        return self.model.predict(batch, num_beams, max_length)

    def generate(self, input_ids, attention_mask, num_beams=4, max_length=50,
                 **kwargs):
        self.eval()
        with torch.no_grad():
            output = self.model.generate(input_ids, attention_mask, num_beams, max_length, **kwargs)
        self.eval()
        return output

    def save_model(self, save_path):
        """
        This save model is created mainly in case we need partial save and load. Such as cases with pretraining.
        """
        self.model.save_model(save_path)

    def load_model(self, load_path):
        """
        This load model is created mainly in case we need partial save and load. Such as cases with pretraining.
        """
        self.model.load_model(load_path)


class AMRPrefixGenBase(nn.Module):
    def __init__(self, config, tokenizer):
        super().__init__()
        """
        Need to init by class
        """

    def get_AMR_embedding(self, AMR_string):
        return self.AMR_model.get_encoder_output(AMR_string)

    def get_prefix(self, Doc_token=None, Doc_mask=None, local_mask=None, CO_token=None, co_mask=None):
        batch_size = Doc_token.size()[0]
        input_tokens = torch.arange(self.config.prefix_length).long().cuda()
        input_tokens = input_tokens.unsqueeze(0).expand(batch_size, -1)
        input_embeds = self.wte(input_tokens)  # (bz, prefix_len, dim)=(4, 40, 1024)  制作长度l=40的query
        prefix = {}
        Co_embedding = self.model.model(input_ids=CO_token, attention_mask=co_mask, return_dict=True).last_hidden_state
        Doc_embedding = self.model.model(input_ids=Doc_token, attention_mask=local_mask, return_dict=True, ).last_hidden_state
        if self.model_config.use_encoder_prefix:
            prefix['encoder_prefix'] = self.enc_prefix_projector.project(Doc_embedding, input_embeds, Doc_mask)
        if self.model_config.use_cross_prefix:
            prefix['cross_prefix'] = self.cross_prefix_projector.project(Doc_embedding, input_embeds, Doc_mask)
        if self.model_config.use_decoder_prefix:
            prefix['decoder_prefix'] = self.dec_prefix_projector.project(Doc_embedding, input_embeds, Doc_mask)
        if self.model_config.use_local_mask and Doc_token is not None and local_mask is not None:
            prefix['local_prefix'] = self.local_prefix_projector.project(Co_embedding, input_embeds, co_mask)
        return prefix

    def forward(self, batch):
        # 这三句代码就是数据的总流图
        prefix = self.get_prefix(
            Doc_token=batch['input_ids'],
            Doc_mask=batch['enc_mask_ids'], local_mask=batch['local_attention_mask'],
            CO_token=batch['co_input_ids'], co_mask=batch['co_prompt_mask_ids'])
        # 下面这句代码是这个forward的核心，作用是调用子类定义的self.model的forward方法
        outputs = self.model(input_ids=batch['input_ids'],  # 这个self.model是子类定义的，子类并没有重写forward，所以子类在被调用forward的时候会直接跳转到这里
                             prefix=prefix,
                             attention_mask=batch['enc_mask_ids'],
                             decoder_input_ids=batch['dec_prompt_ids'],
                             decoder_attention_mask=batch['dec_prompt_mask_ids'],
                             arg_joint_prompts = batch['arg_joint_prompts'],
                             target_info = batch['target_info'],
                             old_tok_to_new_tok_indexs=batch['old_tok_to_new_tok_indexs'],
                             arg_list=batch['arg_list'],
                             return_dict=True)

        return outputs

    def save_model(self, save_path):
        self.model.save_pretrained(os.path.join(save_path, "checkpoint-bart"))
        torch.save(self.wte.state_dict(), os.path.join(save_path, "wte.mdl"))
        torch.save(self.AMR_model.state_dict(), os.path.join(save_path, "amrmodel.mdl"))
        if self.model_config.use_encoder_prefix:
            self.enc_prefix_projector.save(os.path.join(save_path, "enc_prefix_projector.mdl"))
        if self.model_config.use_cross_prefix:
            self.cross_prefix_projector.save(os.path.join(save_path, "cross_prefix_projector.mdl"))
        if self.model_config.use_decoder_prefix:
            self.dec_prefix_projector.save(os.path.join(save_path, "dec_prefix_projector.mdl"))
        if self.model_config.use_local_mask:
            self.local_prefix_projector.save(os.path.join(save_path, "local_prefix_projector.mdl"))


    def load_model(self, load_path):
        logger.info(f"Loading model from {load_path}")
        self.model.from_pretrained(os.path.join(load_path, "checkpoint-bart"))
        self.wte.load_state_dict(
            torch.load(os.path.join(load_path, "wte.mdl"), map_location=f'cuda:{self.config.gpu_device}'))
        self.AMR_model.load_state_dict(
            torch.load(os.path.join(load_path, "amrmodel.mdl"), map_location=f'cuda:{self.config.gpu_device}'))
        if self.model_config.use_encoder_prefix:
            self.enc_prefix_projector.load(os.path.join(load_path, "enc_prefix_projector.mdl"))
        if self.model_config.use_cross_prefix:
            self.cross_prefix_projector.load(os.path.join(load_path, "cross_prefix_projector.mdl"))
        if self.model_config.use_decoder_prefix:
            self.dec_prefix_projector.load(os.path.join(load_path, "dec_prefix_projector.mdl"))
        if self.model_config.use_local_mask:
            self.local_prefix_projector.load(os.path.join(load_path, "local_prefix_projector.mdl"))


# 子类AMRPrefixGenCopyReg申明要用的子模块，父类AMRPrefixGenBase组装子模块来实现数据流动
class AMRPrefixGenCopyReg(AMRPrefixGenBase):
    def __init__(self, config, tokenizer):
        super().__init__(config, tokenizer)
        self.config = config
        self.tokenizer = tokenizer
        logger.info(f'Using model {self.__class__.__name__}')
        logger.info(f'Loading pre-trained model {self.config.model_name_or_path}')

        if self.config.model_name_or_path.startswith('../plm/bart-'):
            # main model
            self.model_config = AutoConfig.from_pretrained(self.config.model_name_or_path)
            self.model_config.output_attentions = False

            # we observe that using prefix in encoder self-attention blocks and decoder cross-attention blocks works best in AMPERE.
            self.model_config.use_encoder_prefix = self.config.use_encoder_prefix
            self.model_config.use_cross_prefix = self.config.use_cross_prefix
            self.model_config.use_decoder_prefix = self.config.use_decoder_prefix
            self.model_config.prefix_length = self.config.prefix_length
            self.model_config.bipartite = self.config.bipartite
            self.model_config.matching_method_train = self.config.matching_method_train
            self.model_config.model_name_or_path = self.config.model_name_or_path
            self.model_config.device = self.config.device
            self.model_config.context_representation = self.config.context_representation
            self.model_config.latent_dim = self.config.latent_dim

            # mask
            self.model_config.use_local_mask = self.config.use_local_mask

            # co-occur
            self.model_config.use_co_occur = self.config.co_occur

            # backbone
            self.model = CopyBartWithReg.from_pretrained(self.config.model_name_or_path,
                                                         config=self.model_config)

            # ## Load AMR
            # if config.AMR_model_path.startswith('../plm/AMRBART-'):
            #     self.AMR_model = AMRBart(self.config)


            ## Prefix Generator
            self.wte = nn.Embedding(config.prefix_length,
                                    config.latent_dim)  # 这个全连接层是用来做projector里面长度为l=40的query的，会在父类AMRPrefixGenBase使用

            if self.model_config.use_encoder_prefix:
                self.enc_prefix_projector = Projector(self.config, self.model_config, "Self_AttIndep")
            if self.model_config.use_cross_prefix:
                self.cross_prefix_projector = Projector(self.config, self.model_config, "Self_AttIndep")
            if self.model_config.use_decoder_prefix:
                self.dec_prefix_projector = Projector(self.config, self.model_config, "Self_AttIndep")
            if self.model_config.use_local_mask:
                self.local_prefix_projector = Projector(self.config, self.model_config, "Self_AttIndep")

        else:
            raise ValueError("Model does not support yet.")
