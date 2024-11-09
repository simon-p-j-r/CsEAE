import torch.nn as nn
import logging
logger = logging.getLogger(__name__)


class BaseTrainer:
    def __init__(
        self,
        cfg=None,
        data_loader=None,
        model=None,
        optimizer=None,
        scheduler=None,
    ):

        self.cfg = cfg
        self.data_loader = data_loader
        self.data_iterator = iter(self.data_loader)
        self.model = model

        self.optimizer = optimizer
        self.scheduler = scheduler
        self._init_metric()

    # 这些方法都写的很脱裤子放屁
    def _init_metric(self):
        self.metric = {
            "global_steps": 0,
            "smooth_loss": 0.0,
        }


    def write_log(self):
        logger.info("-----------------------global_step: {} -------------------------------- ".format(self.metric['global_steps']))
        logger.info('lr: {}'.format(self.scheduler.get_last_lr()[0]))
        logger.info('smooth_loss: {}'.format(self.metric['smooth_loss']))
        self.metric['smooth_loss'] = 0.0


    def train_one_step(self):
        self.model.train()
        try:
            batch = next(self.data_iterator)  # 在Dataset的__getitem__把一条一条的数据发出来以后，Dataloader会根据你定义的batch_size参数把这些东西组织起来（其实是一个batch_list）。然后再送给collate_fn组织成batch最后的样子，
        except StopIteration:
            self.data_iterator = iter(self.data_loader)
            batch = next(self.data_iterator)
        # 这个方法将该送进cuda的送进cuda
        self.model.training = True
        inputs = self.convert_batch_to_inputs(batch)  # 子类中定义的方法
        loss, _= self.model(inputs)  # 训练的时候不需要模型到底预测出来的是什么，只需要损失即可

        if self.cfg.gradient_accumulation_steps > 1:
            loss = loss / self.cfg.gradient_accumulation_steps
        loss.backward()

        if self.cfg.max_grad_norm != 0:
            nn.utils.clip_grad_norm_(self.model.parameters(), self.cfg.max_grad_norm)
        
        self.metric['smooth_loss'] += loss.item()/self.cfg.logging_steps
        if (self.metric['global_steps']+1)%self.cfg.gradient_accumulation_steps==0:
            self.optimizer.step()
            self.scheduler.step()
            self.model.zero_grad()
            self.metric['global_steps'] += 1


    def convert_batch_to_inputs(self, batch):
        raise NotImplementedError()

# 主要是实现了convert_batch_to_inputs()方法
class Trainer(BaseTrainer):
    def __init__(self, cfg=None, data_loader=None, model=None, optimizer=None, scheduler=None):
        super().__init__(cfg, data_loader, model, optimizer, scheduler)

    
    def convert_batch_to_inputs(self, batch):
        if self.cfg.model_type in ["paie", 'amr']:
            inputs = {
                'input_ids':  batch[0].cuda(),
                'enc_mask_ids':   batch[1].cuda(),
                'dec_prompt_ids':           batch[4].cuda(),
                'dec_prompt_mask_ids':      batch[5].cuda(),
                'target_info':              batch[6], 
                'old_tok_to_new_tok_indexs':batch[7],
                'arg_joint_prompts':        batch[8],
                'arg_list':       batch[9],
                'local_attention_mask': batch[12].cuda(),
                'co_input_ids': batch[13].cuda(),
                'co_prompt_mask_ids': batch[14].cuda(),
            }
        elif self.cfg.model_type=="base":
            inputs = {
                'enc_input_ids':  batch[0].cuda(),
                'enc_mask_ids':   batch[1].cuda(),
                'decoder_prompt_ids_list':      [item.cuda() for item in batch[2]],
                'decoder_prompt_mask_list': [item.cuda() for item in batch[3]],
                'arg_list':       batch[9],
                'decoder_prompt_start_positions_list': [item.cuda() for item in batch[12]],
                'decoder_prompt_end_positions_list': [item.cuda() for item in batch[13]],
                'start_position_ids': [item.cuda() for item in batch[14]],
                'end_position_ids': [item.cuda() for item in batch[15]],
            }

        return inputs
