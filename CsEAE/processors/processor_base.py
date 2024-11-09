import csv
import json
import jsonlines
import numpy as np
import torch

from random import sample
from torch.utils.data import DataLoader, RandomSampler, SequentialSampler, TensorDataset
import copy                             
import logging
logger = logging.getLogger(__name__)


# Event(doc_key+str(event_idx), None, cut_text, event_type, event_trigger, event_args, full_text, first_word_locs)
class Event:
    def __init__(self, doc_id, sent_id, sent, event_type, event_trigger, event_args, full_text, first_word_locs=None, sentences=None, event_types=None):
        self.doc_id = doc_id
        self.sent_id = sent_id
        self.sent = sent
        self.type = event_type
        self.trigger = event_trigger
        self.args = event_args
        
        self.full_text = full_text
        self.first_word_locs = first_word_locs

        self.sentences = sentences


        self.event_types = event_types


    def __str__(self):
        return self.__repr__()
    

    def __repr__(self):
        s = ""
        s += "doc id: {}\n".format(self.doc_id)
        s += "sent id: {}\n".format(self.sent_id)
        s += "text: {}\n".format(" ".join(self.sent))
        s += "event_type: {}\n".format(self.type)
        s += "trigger: {}\n".format(self.trigger['text'])
        for arg in self.args:
            s += "arg {}: {} ({}, {})\n".format(arg['role'], arg['text'], arg['start'], arg['end'])
        s += "----------------------------------------------\n"
        return s


class InputFeatures(object):
    """A single set of features of data."""

    def __init__(self, example_id, feature_id, 
                 enc_text, dec_text,
                 enc_tokens, dec_tokens, 
                 old_tok_to_new_tok_index,  
                 event_type, event_trigger, argument_type,
                 enc_input_ids, enc_mask_ids, 
                 dec_input_ids, dec_mask_ids,
                 answer_text, start_position=None, end_position=None):

        self.example_id = example_id
        self.feature_id = feature_id
        self.enc_text = enc_text
        self.dec_text = dec_text
        self.enc_tokens = enc_tokens
        self.dec_tokens = dec_tokens
        self.old_tok_to_new_tok_index = old_tok_to_new_tok_index
        self.event_type = event_type
        self.event_trigger = event_trigger
        self.argument_type = argument_type
        
        self.enc_input_ids = enc_input_ids
        self.enc_mask_ids = enc_mask_ids
        self.dec_input_ids = dec_input_ids
        self.dec_mask_ids = dec_mask_ids

        self.answer_text = answer_text
        self.start_position = start_position
        self.end_position = end_position


    def __str__(self):
        return self.__repr__()
    

    def __repr__(self):
        s = "" 
        s += "example_id: {}\n".format(self.example_id)
        s += "event_type: {}\n".format(self.event_type)
        s += "trigger_word: {}\n".format(self.event_trigger)
        s += "argument_type: {}\n".format(self.argument_type)
        s += "enc_tokens: {}\n".format(self.enc_tokens)
        s += "dec_tokens: {}\n".format(self.dec_tokens)
        s += "old_tok_to_new_tok_index: {}\n".format(self.old_tok_to_new_tok_index)
        
        s += "enc_input_ids: {}\n".format(self.enc_input_ids)
        s += "enc_mask_ids: {}\n".format(self.enc_mask_ids)
        s += "dec_input_ids: {}\n".format(self.dec_input_ids)
        s += "dec_mask_ids: {}\n".format(self.dec_mask_ids)
        
        s += "answer_text: {}\n".format(self.answer_text)
        s += "start_position: {}\n".format(self.start_position)
        s += "end_position: {}\n".format(self.end_position) 
        return s


class DSET_processor:
    def __init__(self, args, tokenizer):
        self.args = args
        self.tokenizer = tokenizer
        # self.template_dict是  角色名:模板格式的字典，例如'personnel.endposition.quitretire_employee':'to be continue'，这里之后也没用
        # self.argument_dict是  事件类型:角色表格式的字典，例如：'personnel.endposition.quitretire':['employee', 'place', 'placeofemployment']'
        self.template_dict, self.argument_dict = self._read_roles(self.args.role_path)
        self.collate_fn = None

    # 只是读出每个set数据中的每一行的每一个键值对,没有做任何处理,只是读出
    def _read_jsonlines(self, input_file):
        lines = []
        with jsonlines.open(input_file) as reader:
            for obj in reader:
                lines.append(obj)  # 将文档中的数据一行一行读出来放进list
        return lines

    def _read_json(self, input_file):
        with open(input_file, "r", encoding='utf-8') as f:
            return json.load(f)

    # 得到关于事件的一些基本信息，例如事件类型，事件类型中存在的角色等
    def _read_roles(self, role_path):
        template_dict = {}  # 角色名:模板格式的字典，例如'personnel.endposition.quitretire_employee':'to be continue'
        role_dict = {}  # 事件类型:角色表格式的字典，例如：'personnel.endposition.quitretire':['employee', 'place', 'placeofemployment']'
        if 'MLEE' in role_path:
            with open(role_path) as f:
                role_name_mapping = json.load(f)
                for event_type, mapping in role_name_mapping.items():
                    roles = list(mapping.keys())
                    role_dict[event_type] = roles

            return None, role_dict
        with open(role_path, "r", encoding='utf-8') as f:
            csv_reader = csv.reader(f)
            for line in csv_reader:

                event_type_arg, template = line
                template_dict[event_type_arg] = template

                event_type, arg = event_type_arg.split('_')
                # 判断事件-角色表role_dict里面是否有当前事件类型，没有就添加
                if event_type not in role_dict:
                    role_dict[event_type] = []
                # 在事件-角色表role_dict的键（事件类型）对应的值（事件类型对应的角色列表）添加相对应的事件类型
                role_dict[event_type].append(arg)

        return template_dict, role_dict

    def _create_example_mlee(self, lines):
        W = self.args.window_size
        examples = []

        for line in lines:
            doc_id = line["id"]
            context = line['context']
            events = line["events"]
            sentences = line['sents']
            num_events = len(events)
            events = sorted(events, key=lambda x: x['trigger'])
            context_length = len(context)

            if num_events < 1:
                print('[num_events < 1]', doc_id)
                continue

            if context_length > W:  # TabEAE不同于PAIE,超过窗口大小的sentence,这里直接删了
                assert (0==1)

            if num_events > self.args.max_num_event:  # 事件数太多的直接把多余的删了
                for event in events[self.args.max_num_event:]:
                    self.invalid_arg_num += len(event['args'])
                events = events[:self.args.max_num_event]
                print('[num_events > max_num_event] %s\t\t%d' % (doc_id, num_events))
            assert len(events) <= self.args.max_num_event

            for event in events:

                # co-occur
                event_types = []
                for event_temp in events:
                    event_type = {}
                    event_type['event_type'] = event_temp['event_type']
                    event_type['trigger'] = event_temp['trigger']
                    event_types.append(event_type)

                # every sent start/end
                text_tmp = []
                first_word_locs = []
                for sent in sentences:
                    first_word_locs.append(len(text_tmp))
                    text_tmp += sent
                end_word_locs = list(np.cumsum([len(sent) for sent in sentences]))

                # type
                event_type = event['event_type']

                # trigger
                event_trigger = dict()
                event_trigger['start'] = event['trigger'][0]
                event_trigger['end'] = event['trigger'][1]
                event_trigger['offset'] = 0
                # 提取trigger的txt文本
                # 从这里可以看出，数据集中记录论元和触发词start和end位置的编号均是相对于整个sentence来的，而不是相对于五个段中的每一个单独的段
                event_trigger['text'] = " ".join(context[event_trigger['start']:event_trigger['end']])
                for num, sent_start in enumerate(first_word_locs):
                    if event_trigger['start'] >= sent_start and event_trigger['end'] <= end_word_locs[num]:
                        event_trigger['sent_idx'] = num

                # args
                event_args = list()
                for arg_info in event['args']:
                    evt_arg = dict()  # evt_arg用于记录论元及其对应的角色
                    evt_arg['start'] = arg_info[0]
                    evt_arg['end'] = arg_info[1]
                    evt_arg['text'] = " ".join(context[evt_arg['start']:evt_arg['end']])
                    evt_arg['role'] = arg_info[3]
                    event_args.append(evt_arg)

                examples.append(Event(doc_id, None, context, event_type, event_trigger, event_args, context,
                                      first_word_locs=first_word_locs,
                                      sentences=sentences, event_types=event_types))

        print("{} examples collected. {} arguments dropped.".format(len(examples), self.invalid_arg_num))
        return examples


    def _create_example_rams(self, lines):
        W = self.args.window_size
        assert (W % 2 == 0)
        all_args_num = 0  # 这个参数记录了数据集（train/dev/test）中所有论元的数量

        # 这个for循环每次处理一个sentence
        examples = []
        for line in lines:
            if len(line["events"]) == 0:  # 没有事件的句子就跳过了
                continue
            doc_key = line["id"]  # "doc_key"记录了事件提及的编号
            # ‘evt_triggers’字段里面是：触发词位置，事件类型，数据版本
            # eg: [[69, 69, [['life.die.deathcausedbyviolentevents', 1.0]]]]
            events = line["events"]
            # 但是注意，这个数据集的一条sentence被分成了五个list组成得sentences，这里将五个list合成一个了
            full_text = copy.deepcopy(line['context'])
            cut_text = line['context']
            sent_length = sum([len(sent) for sent in line['sents']])
            sentences = line['sents']

            # event:[69, 69, [['life.die.deathcausedbyviolentevents', 1.0]]]
            for event_idx, event in enumerate(events):
                # co-occur
                event_types = []
                for event_temp in events:
                    event_type = {}
                    event_type['event_type'] = event_temp['event_type']
                    event_type['trigger'] = event_temp['trigger']
                    event_types.append(event_type)

                # mask
                text_tmp = []
                first_word_locs = []
                end_word_locs = list(np.cumsum([len(sent) for sent in sentences]))
                for sent in sentences:
                    first_word_locs.append(len(text_tmp))
                    text_tmp += sent

                event_trigger = dict()
                event_trigger['start'] = event['trigger'][0]
                event_trigger['end'] = event['trigger'][1]
                # 提取trigger的txt文本
                event_trigger['text'] = " ".join(full_text[event_trigger['start']:event_trigger['end']])
                for num, sent_start in enumerate(first_word_locs):
                    if event_trigger['start'] >= sent_start and event_trigger['end'] <= end_word_locs[num]:
                        event_trigger['sent_idx'] = num
                event_type = event['event_type']  # 提取事件类型，eg:'life.die.deathcausedbyviolentevents'

                # 这个代码块是为了处理事件提及过长要进行切割的
                offset, min_s, max_e = 0, 0, W + 1
                event_trigger['offset'] = offset
                if sent_length > W + 1:  # 如果数据经过TabEAE划分，就不会出现超过窗口值的输入
                    assert (0 == 1)

                # 这个for循环是为了处理论元及其对应角色的
                event_args = list()
                # "gold_evt_links"里面是一个（触发词，论元，角色）的三元组
                # arg_info:[[69, 69], [85, 88], 'evt090arg01killer']
                for arg_info in event["args"]:
                    all_args_num += 1

                    evt_arg = dict()  # evt_arg用于记录论元及其对应的角色
                    evt_arg['start'] = arg_info[0]
                    evt_arg['end'] = arg_info[1]
                    evt_arg['text'] = " ".join(full_text[evt_arg['start']:evt_arg['end']])
                    evt_arg['role'] = arg_info[3]  # 提取论元对应的角色
                    event_args.append(evt_arg)

                if event_idx > 0:
                    examples.append(Event(doc_key + str(event_idx), None, cut_text, event_type, event_trigger,
                                          event_args, full_text, first_word_locs, sentences, event_types))

                else:
                    examples.append(Event(doc_key, None, cut_text, event_type, event_trigger, event_args, full_text,
                                          first_word_locs=first_word_locs,
                                          sentences=sentences, event_types=event_types))

        print("{} examples collected. {} arguments dropped.".format(len(examples), self.invalid_arg_num))
        return examples

    # 注意每一个example都是以事件为单位的Event类型的数据
    def _create_example_wikievent(self, lines):
        W = self.args.window_size
        assert(W%2==0)

        examples = []
        for line in lines:  # 这里和rams不一样，rams每一行只有一个事件类型，但是这里的每一行包括事件提及中出现过的所有事件
            entity_dict = {entity['id']:entity for entity in line['entity_mentions']}
            events = line["event_mentions"]
            if not events:
                continue
            doc_key = line["doc_id"]
            full_text = line['tokens']
            sent_length = len(full_text)

            # 每次处理一个事件,这里最终会存储event类的数据，所有在event里面会有不同的都放在下面这个循环
            for event in events:

                # co-occur
                event_types = []
                trigger_temp = []
                for event_temp in events:
                    event_type = {}
                    event_type['event_type'] = event_temp['event_type']
                    trigger = event_temp['trigger']
                    trigger_temp.append(trigger['start'])
                    trigger_temp.append(trigger['end'])
                    trigger_temp.append(trigger['text'])
                    event_type['trigger'] = trigger_temp
                    event_types.append(event_type)

                curr_loc = 0
                first_word_locs = []  # 每一个sentence在整个doc中的起始位置
                for sent in line["sentences"]:  # wiki的sentence被分成了四段
                    first_word_locs.append(curr_loc)
                    curr_loc += len(sent)
                sentences = line["sentences"]
                end_word_locs = list(np.cumsum([len(sent) for sent in sentences]))

                event_type = event['event_type']
                cut_text = full_text
                event_trigger = event['trigger']
                event_trigger['offset'] = 0

                if sent_length > W+1:  # 如果这个事件提及太长了就要进行切片,这里分两种情况,trigger在切片之后的前面一段还是后面一段
                    assert (0==1)

                event_args = list()
                for arg_info in event['arguments']:  # arg_info的数据格式 ：{'entity_id': 'scenario_en_kairos_65-T13', 'role': 'Victim', 'text': 'Terry Duffield'}
                    evt_arg = dict()
                    arg_entity = entity_dict[arg_info['entity_id']]  # 获得具体的每个论元的信息，主要是得到一些start,end等的基本信息
                    evt_arg['start'] = arg_entity['start']
                    evt_arg['end'] = arg_entity['end']
                    evt_arg['text'] = arg_info['text']
                    evt_arg['role'] = arg_info['role']
                    event_args.append(evt_arg)

                examples.append(Event(doc_key, None, cut_text, event_type, event_trigger, event_args,
                                      full_text, first_word_locs, sentences, event_types))

        logger.info("{} examples collected. {} dropped.".format(len(examples), self.invalid_arg_num))
        return examples

    def create_example(self, file_path):
        self.invalid_arg_num = 0
        if self.args.dataset_type=='ace_eeqa':
            lines = self._read_jsonlines(file_path)
            return self._create_example_ace(lines)
        elif self.args.dataset_type=='rams':
            lines = self._read_jsonlines(file_path)
            return self._create_example_rams(lines)
        elif self.args.dataset_type=='wikievent':
            lines = self._read_jsonlines(file_path)
            return self._create_example_wikievent(lines)
        elif self.args.dataset_type=='MLEE':
            lines = self._read_jsonlines(file_path)
            return self._create_example_mlee(lines)
        else:
            raise NotImplementedError()

    def convert_examples_to_features(self, examples):
        features = []
        for (example_idx, example) in enumerate(examples):
            sent = example.sent
            event_type = example.type
            event_args = example.args
            event_trigger = example.trigger['text']
            event_args_name = [arg['role'] for arg in event_args]
            enc_text = " ".join(sent)

            old_tok_to_char_index = []     # old tok: split by oneie
            old_tok_to_new_tok_index = []  # new tok: split by BART

            curr = 0
            for tok in sent:
                old_tok_to_char_index.append(curr)
                curr += len(tok)+1
            assert(len(old_tok_to_char_index)==len(sent))

            enc = self.tokenizer(enc_text)
            enc_input_ids, enc_mask_ids = enc["input_ids"], enc["attention_mask"]
            enc_tokens = self.tokenizer.convert_ids_to_tokens(enc_input_ids)
            while len(enc_input_ids) < self.args.max_enc_seq_length:
                enc_input_ids.append(self.tokenizer.pad_token_id)
                enc_mask_ids.append(self.args.pad_mask_token)

            for char_idx in old_tok_to_char_index:
                new_tok = enc.char_to_token(char_idx)
                old_tok_to_new_tok_index.append(new_tok)

            for arg in self.argument_dict[event_type.replace(':', '.')]:
                dec_text = 'Argument ' + arg + ' in ' + event_trigger + ' event ?' + " "

                dec = self.tokenizer(dec_text)
                dec_input_ids, dec_mask_ids = dec["input_ids"], dec["attention_mask"]
                dec_tokens = self.tokenizer.convert_ids_to_tokens(dec_input_ids)
                while len(dec_input_ids) < self.args.max_dec_seq_length:
                    dec_input_ids.append(self.tokenizer.pad_token_id)
                    dec_mask_ids.append(self.args.pad_mask_token)

                start_position, end_position, answer_text = None, None, None
                if arg in event_args_name:
                    arg_idx = event_args_name.index(arg)
                    event_arg_info = event_args[arg_idx]
                    answer_text = event_arg_info['text']
                    # index before BPE, plus 1 because having inserted start token
                    start_old, end_old = event_arg_info['start'], event_arg_info['end']
                    start_position = old_tok_to_new_tok_index[start_old]
                    end_position = old_tok_to_new_tok_index[end_old] if end_old<len(old_tok_to_new_tok_index) else old_tok_to_new_tok_index[-1]+1
                else:
                    start_position, end_position = 0, 0
                    answer_text = "__ No answer __"

                feature_idx = len(features)
                features.append(
                      InputFeatures(example_idx, feature_idx,
                                    enc_text, dec_text,
                                    enc_tokens, dec_tokens,
                                    old_tok_to_new_tok_index,
                                    event_type, event_trigger, arg,
                                    enc_input_ids, enc_mask_ids,
                                    dec_input_ids, dec_mask_ids,
                                    answer_text, start_position, end_position
                                )
                )
        return features

    def convert_features_to_dataset(self, features):

        all_enc_input_ids = torch.tensor([f.enc_input_ids for f in features], \
            dtype=torch.long).cuda()
        all_enc_mask_ids = torch.tensor([f.enc_mask_ids for f in features], \
            dtype=torch.long).cuda()
        all_dec_input_ids = torch.tensor([f.dec_input_ids for f in features], \
            dtype=torch.long).cuda()
        all_dec_mask_ids = torch.tensor([f.dec_mask_ids for f in features], \
            dtype=torch.long).cuda()

        all_start_positions = torch.tensor([f.start_position for f in features], \
            dtype=torch.long).cuda()
        all_end_positions = torch.tensor([f.end_position for f in features], \
            dtype=torch.long).cuda()
        all_example_idx = torch.tensor([f.example_id for f in features], \
            dtype=torch.long).cuda()
        all_feature_idx = torch.tensor([f.feature_id for f in features], \
            dtype=torch.long).cuda()

        dataset = TensorDataset(all_enc_input_ids, all_enc_mask_ids,
                                all_dec_input_ids, all_dec_mask_ids,
                                all_start_positions, all_end_positions,
                                all_example_idx, all_feature_idx,
                            )
        return dataset

    def generate_dataloader(self, set_type):
        assert (set_type in ['train', 'dev', 'test'])
        if set_type=='train':
            file_path = self.args.train_file
        elif set_type=='dev':
            file_path = self.args.dev_file
        else:
            file_path = self.args.test_file
        
        examples = self.create_example(file_path)
        if set_type=='train' and self.args.keep_ratio<1.0:
            sample_num = int(len(examples)*self.args.keep_ratio)
            examples = sample(examples, sample_num)
            logger.info("Few shot setting: keep ratio {}. Only {} training samples remained.".format(\
                self.args.keep_ratio, len(examples))
            )

        features = self.convert_examples_to_features(examples, self.args.role_name_mapping)
        dataset = self.convert_features_to_dataset(features)

        if set_type != 'train':
            dataset_sampler = SequentialSampler(dataset)
        else:
            dataset_sampler = RandomSampler(dataset)
        if self.collate_fn:
            dataloader = DataLoader(dataset, sampler=dataset_sampler, batch_size=self.args.batch_size, collate_fn=self.collate_fn)
        else:
            dataloader = DataLoader(dataset, sampler=dataset_sampler, batch_size=self.args.batch_size)
        return examples, features, dataloader, self.invalid_arg_num