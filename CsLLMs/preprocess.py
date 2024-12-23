import csv
import json

import numpy as np

from parameters_finance import TEMPLATE_FINANCE_Event, TEMPLATE_FINANCE_Role_Name, TEMPLATE_FINANCE_Role, TEMPLATE_FINANCE_Demo
from parameters_ace import TEMPLATE_ACE_Role, TEMPLATE_ACE_Event, TEMPLATE_ACE_Demo
from parameters_wikievent import TEMPLATE_WikiEvents_Event, TEMPLATE_WikiEvents_All, TEMPLATE_WikiEvents_Event_Full,TEMPLATE_WikiEvents_Event_Demo
from parameters_rams import TEMPLATE_RAMS_Role_Name, TEMPLATE_RAMS_Event_Full, TEMPLATE_RAMS_Event_Demo
from parameters_mlee import TEMPLATE_MLEE_Role_Name, TEMPLATE_MLEE_Event_Full, TEMPLATE_MLEE_Event_Demo
from parameters_geneva import TEMPLATE_GENEVA_Role_Name, TEMPLATE_GENEVA_Event_Demo

def get_pre_instruct(data_type):
    disappear_type = []
    if data_type=='FINANCE':
        TEMPLATE_Event = TEMPLATE_FINANCE_Event
        TEMPLATE_Role = TEMPLATE_FINANCE_Role
        TEMPLATE_Role_Name = TEMPLATE_FINANCE_Role_Name
        TEMPLATE_Demo = TEMPLATE_FINANCE_Demo

    elif data_type=='ACE':
        TEMPLATE_Event_All = TEMPLATE_ACE_Event
        TEMPLATE_Event = {}
        for event in TEMPLATE_Event_All:
            TEMPLATE_Event[event] = TEMPLATE_Event_All[event]['event description']
        TEMPLATE_Role = TEMPLATE_ACE_Role
        TEMPLATE_Role_Name = {}
        for event in TEMPLATE_Event_All:
            TEMPLATE_Role_Name[event] = TEMPLATE_Event_All[event]['valid roles']
        TEMPLATE_Demo = TEMPLATE_ACE_Demo

    elif data_type=='WikiEvent':
        TEMPLATE_Event_All = TEMPLATE_WikiEvents_All
        TEMPLATE_Event = TEMPLATE_WikiEvents_Event_Full
        TEMPLATE_Role = None
        TEMPLATE_Role_Name = {}
        for event in TEMPLATE_Event_All:
            TEMPLATE_Role_Name[event] = TEMPLATE_Event_All[event]['roles']
        TEMPLATE_Demo = TEMPLATE_WikiEvents_Event_Demo
        for type in TEMPLATE_Role_Name:
            if type not in TEMPLATE_Demo:
                disappear_type.append(type)
    elif data_type=='RAMS':
        TEMPLATE_Role = TEMPLATE_RAMS_Role_Name
        TEMPLATE_Role_Name = {}
        for event in TEMPLATE_Role:
            TEMPLATE_Role_Name[event] = []
            for role in TEMPLATE_Role[event]:
                TEMPLATE_Role_Name[event].append(role)
        TEMPLATE_Demo = TEMPLATE_RAMS_Event_Demo
    elif data_type=='MLEE':
        TEMPLATE_Role = TEMPLATE_MLEE_Role_Name
        TEMPLATE_Role_Name = {}
        for event in TEMPLATE_Role:
            TEMPLATE_Role_Name[event] = []
            for role in TEMPLATE_Role[event]:
                TEMPLATE_Role_Name[event].append(role)
        TEMPLATE_Demo = TEMPLATE_MLEE_Event_Demo
    elif data_type=='GENEVA':
        TEMPLATE_Role_Name = TEMPLATE_GENEVA_Role_Name
        TEMPLATE_Demo = TEMPLATE_GENEVA_Event_Demo

    else:
        raise NotImplementedError(f"Unexpected Dataset {data_type}")

    return TEMPLATE_Role_Name, TEMPLATE_Demo, disappear_type

def _read_roles(role_path):
    template_dict = {}  # 角色名:模板格式的字典，例如'personnel.endposition.quitretire_employee':'to be continue'
    role_dict = {}  # 事件类型:角色表格式的字典，例如：'personnel.endposition.quitretire':['employee', 'place', 'placeofemployment']'
    # "description_*"的文件里面放的是各个事件类型包括的角色
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
            # event_type_arg是事件类型_角色名
            # 在读取文件时，其实这里的template都是'to be continue'，也就是说，这里的template_dict字典里面存放的都是{事件类型_角色名:'to be continue'}
            # eg:{'personnel.endposition.quitretire_employee': 'to be continue'}
            event_type_arg, template = line
            template_dict[event_type_arg] = template

            event_type, arg = event_type_arg.split('_')
            # 判断事件-角色表role_dict里面是否有当前事件类型，没有就添加
            if event_type not in role_dict:
                role_dict[event_type] = []
            # 在事件-角色表role_dict的键（事件类型）对应的值（事件类型对应的角色列表）添加相对应的事件类型
            role_dict[event_type].append(arg)

    return template_dict, role_dict

def get_res_list(res_path, args, filter_no_prob=False, dataset_type=None, train=False):



    if dataset_type == 'Finance':
        with open(res_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        for i in range(len(lines)):
            lines[i] = json.loads(lines[i].strip())
        event_lines = []

        if train:
            lines = lines[0]
            for type in lines:
                for line in lines[type]:
                    id = line['event_list'][0]['id']
                    events = line['event_list']
                    content = line['sent']
                    event_types = []
                    for event in events:
                        event_types.append(event['event_type'])

                    for i, event in enumerate(events):
                        event_line = {}
                        event_line['id'] = id
                        event_new = {}
                        event_new['occur_event'] = event_types
                        event_new['text'] = event['text']
                        event_new['start'] = event['start']
                        event_new['end'] = event['end']
                        event_new['type'] = event['event_type']
                        event_new['args'] = event['args']
                        event_line['event'] = event_new

                        event_line['gt'] = event['args']
                        event_line['gt_words'] = {}
                        event_line['pred_words'] = {}
                        # 只保留gt_words
                        for arg in event['args']:
                            argument = event['args'][arg]
                            words = []
                            for ar in argument:
                                words.append(ar['word'])
                            event_line['gt_words'][arg] = words

                        # add special token
                        event_token = content.split()
                        event_line['sent'] = ''
                        for i, token in enumerate(event_token):
                            if i == event['start']:
                                event_line['sent'] += '<t>'
                                event_line['sent'] += token
                            elif i == event['end'] - 1:
                                event_line['sent'] += token
                                event_line['sent'] += '<t>'
                            else:
                                event_line['sent'] += token

                        event_lines.append(event_line)
        else:
            for line in lines:
                id = line['id']
                content = line['content']
                events = line['events']

                event_types = []
                for event in events:
                    event_types.append(event['type'])

                if len(events) == 0:
                    continue

                for i, event in enumerate(events):
                    event_line = {}
                    event_line['id'] = id + '_{}_event'.format(i)
                    event['occur_event'] = event_types
                    event['text'] = event['trigger']['word']
                    event['start'] = event['trigger']['span'][0]
                    event['end'] = event['trigger']['span'][1]
                    event_line['event'] = event

                    event_line['gt'] = event['args']
                    event_line['gt_words'] = {}
                    event_line['pred_words'] = {}
                    # 只保留gt_words
                    for arg in event['args']:
                        argument = event['args'][arg]
                        words = []
                        for ar in argument:
                            words.append(ar['word'])
                        event_line['gt_words'][arg] = words

                    # add special token, 这里的start和end是左闭右开
                    event_token = list(content)
                    event_line['sent'] = ''
                    for i, token in enumerate(event_token):
                        if i == event['start']:
                            event_line['sent'] += '<t>'
                            event_line['sent'] += token
                        elif i == event['end']-1:
                            event_line['sent'] += token
                            event_line['sent'] += '<t>'
                        else:
                            event_line['sent'] += token

                    event_lines.append(event_line)
        return event_lines

    if dataset_type == 'ACE':
        template_dict, argument_dict = _read_roles('prompt/description_ace.csv')
        event_lines=[]
        with open(res_path) as f:
            lines = f.readlines()
        for i in range(len(lines)):
            lines[i] = json.loads(lines[i].strip())

        for line in lines:
            if not line['event']:
                continue

            events = line['event']
            offset = line['s_start']
            text = line['sentence']
            event_types = []
            for event in events:
                event_types.append(event[0][1])

            for i, event in enumerate(events):
                event_line = {}
                event_line['id'] = i
                event_info = {}
                event_info['occur_event'] = event_types

                event_type = event[0][1]
                event_info['type'] = event_type

                # trigger
                event_trigger = dict()
                start = event[0][0] - offset; end = start+1
                event_trigger['span'] = [start,end]
                word = " ".join(text[start:end])
                event_trigger['word'] = word
                event_info['trigger'] = event_trigger
                event_info['start'] = start
                event_info['end'] = end
                event_info['text'] = word

                # args
                args = dict()
                for arg_info in event[1:]:
                    arg = dict()
                    start = arg_info[0]-offset; end = arg_info[1]-offset+1
                    role = arg_info[2]
                    arg['span'] = [start,end]
                    arg['word'] = " ".join(text[start:end])
                    if role not in args:
                        args[role] = [arg]
                    else:
                        args[role].append(arg)
                event_info['args'] = args

                # sent ，这里的start和end是左闭右闭
                sent = []
                for i, token in enumerate(text):
                    if i == event_trigger['span'][0]:
                        sent.append('<t>')
                        sent.append(token)
                    elif i == event_trigger['span'][1]:
                        sent.append('<t>')
                        sent.append(token)
                    else:
                        sent.append(token)
                event_line['sent'] = ' '.join(sent)

                # gt_words
                event_line['gt_words'] = {}
                for arg in args:
                    argument = args[arg]
                    words = []
                    for ar in argument:
                        words.append(ar['word'])
                    event_line['gt_words'][arg] = words

                event_line['gt'] = args
                event_line['type'] = event_type
                event_line['pred_words'] = {}
                event_line['event'] = event_info
                event_line['first_word_locs'] = []
                event_line['end_word_locs'] = []
                event_line['role_name'] =argument_dict[event_type]

                event_lines.append(event_line)

        return event_lines

    if dataset_type == 'WikiEvent':
        template_dict, argument_dict = _read_roles('prompt/description_wikievent.csv')
        event_lines = []
        with open(res_path) as f:
            lines = f.readlines()
        for i in range(len(lines)):
            lines[i] = json.loads(lines[i].strip())

        for line in lines:
            if not line['event_mentions']:
                continue
            events = line['event_mentions']
            text = line['tokens']
            doc_key = line["doc_id"]

            # occur
            event_types = []
            occur_triggers = []
            for event in events:
                event_types.append(event['event_type'])
                occur_triggers.append(event['trigger'])
            trigger_start = []
            trigger_end = []
            for trigger_se in occur_triggers:
                trigger_start.append(trigger_se['start'])
                trigger_end.append(trigger_se['end'])

            # structure
            sentences = line['sentences']
            text_tmp = []
            first_word_locs = []
            end_word_locs = list(np.cumsum([len(sent) for sent in sentences]))
            for sent in sentences:
                first_word_locs.append(len(text_tmp))
                text_tmp += sent

            for i, event in enumerate(events):
                event_line = {}
                event_line['id'] = doc_key+'_event_{}'.format(i)
                event_info = {}
                event_info['occur_event'] = event_types
                event_type = event['event_type']

                # trigger
                event_trigger = event['trigger']
                trigger = {}
                trigger['span'] = [event_trigger['start'], event_trigger['end']]
                trigger['word'] = event_trigger['text']
                trigger['sent_idx'] = event_trigger['sent_idx']
                event_info['trigger'] = trigger
                event_info['start'] = event_trigger['start']
                event_info['end'] = event_trigger['end']
                event_info['word'] = event_trigger['text']

                # args
                event_args = {}
                for arg_info in event['arguments']:  # arg_info的数据格式 ：{'entity_id': 'scenario_en_kairos_65-T13', 'role': 'Victim', 'text': 'Terry Duffield'}
                    evt_arg = dict()
                    evt_arg['span'] = [arg_info['start'], arg_info['end']]
                    evt_arg['word'] = arg_info['text']
                    role = arg_info['role']
                    if role not in event_args:
                        event_args[role] = [evt_arg]
                    else:
                        event_args[role].append(evt_arg)
                event_info['args'] = event_args

                # sent ，这里的start和end是左闭右闭 trigger mark
                sent = []
                for i, token in enumerate(text):
                    if i == trigger['span'][0]:
                        sent.append('<t>')
                        sent.append(token)
                    elif i == trigger['span'][1]:
                        sent.append('<t>')
                        sent.append(token)
                    else:
                        sent.append(token)
                event_line['sent'] = ' '.join(sent)

                # only structure
                trigger_sent = [first_word_locs[event_trigger['sent_idx']], end_word_locs[event_trigger['sent_idx']]]
                if args.structure and not args.occur:
                    sent = []
                    for i, token in enumerate(text):
                        if i == trigger_sent[0]:
                            sent.append('<s>')
                        elif i == trigger_sent[1]:
                            sent.append('<s>')
                        if i == trigger['span'][0]:
                            sent.append('<t>')
                        elif i == trigger['span'][1]:
                            sent.append('<t>')
                        sent.append(token)
                    event_line['sent'] = ' '.join(sent)

                # only occur
                if args.occur and not args.structure:
                    sent = []
                    for i, token in enumerate(text):
                        if i == trigger['span'][0]:
                            sent.append('<t>')
                        elif i == trigger['span'][1]:
                            sent.append('<t>')
                        elif i in trigger_start and i != trigger['span'][0] and i != trigger['span'][1]:
                            sent.append('<T>')
                        elif i in trigger_end and i != trigger['span'][0] and i != trigger['span'][1]:
                            sent.append('<T>')
                        sent.append(token)
                    event_line['sent'] = ' '.join(sent)

                # both occur and structure
                if args.occur and args.structure:
                    sent = []
                    for i, token in enumerate(text):
                        if i == trigger_sent[0]:
                            sent.append('<s>')
                        elif i == trigger_sent[1]:
                            sent.append('<s>')
                        if i == trigger['span'][0]:
                            sent.append('<t>')
                        elif i == trigger['span'][1]:
                            sent.append('<t>')
                        elif i in trigger_start and i != trigger['span'][0] and i != trigger['span'][1]:
                            sent.append('<T>')
                        elif i in trigger_end and i != trigger['span'][0] and i != trigger['span'][1]:
                            sent.append('<T>')
                        sent.append(token)
                    event_line['sent'] = ' '.join(sent)

                # gt_words
                event_line['gt_words'] = {}
                for arg in event_args:
                    argument = event_args[arg]
                    words = []
                    for ar in argument:
                        words.append(ar['word'])
                    event_line['gt_words'][arg] = words

                event_line['gt'] = event_args
                event_line['type'] = event_type
                event_line['pred_words'] = {}
                event_line['event'] = event_info
                event_line['first_word_locs'] = first_word_locs
                event_line['end_word_locs'] = end_word_locs
                event_line['role_name'] =argument_dict[event_type]

                event_lines.append(event_line)
        return event_lines

    if dataset_type == 'RAMS':
        template_dict, argument_dict = _read_roles('prompt/description_rams.csv')

        event_lines = []
        with open(res_path) as f:
            lines = f.readlines()
        for i in range(len(lines)):
            lines[i] = json.loads(lines[i].strip())

        for line in lines:
            if not line['events']:
                continue
            events = line['events']
            text = line['context']
            doc_key = line["id"]

            # occur
            event_types = []
            occur_triggers = []
            for event in events:
                event_types.append(event['event_type'])
                occur_triggers.append(event['trigger'])
            trigger_start = []
            trigger_end = []
            for trigger_se in occur_triggers:
                trigger_start.append(trigger_se[0])
                trigger_end.append(trigger_se[1])

            # structure
            sentences = line['sents']
            text_tmp = []
            first_word_locs = []
            end_word_locs = list(np.cumsum([len(sent) for sent in sentences]))
            for sent in sentences:
                first_word_locs.append(len(text_tmp))
                text_tmp += sent

            for i, event in enumerate(events):
                event_line = {}
                event_line['id'] = doc_key + '_event_{}'.format(i)
                event_info = {}
                event_info['occur_event'] = event_types
                event_type = event['event_type']

                # trigger
                event_trigger = event['trigger']
                trigger = {}
                trigger['span'] = [event_trigger[0], event_trigger[1]]
                trigger['word'] = event_trigger[2]
                for num, sent_start in enumerate(first_word_locs):
                    if event_trigger[0] >= sent_start and event_trigger[1] <= end_word_locs[num]:
                        trigger['sent_idx'] = num
                event_info['trigger'] = trigger
                event_info['start'] = event_trigger[0]
                event_info['end'] = event_trigger[1]
                event_info['word'] = event_trigger[2]

                # args
                event_args = {}
                for arg_info in event['args']:
                    evt_arg = dict()
                    evt_arg['span'] = [arg_info[0], arg_info[1]]
                    evt_arg['word'] = arg_info[2]
                    role = arg_info[3]
                    if role not in event_args:
                        event_args[role] = [evt_arg]
                    else:
                        event_args[role].append(evt_arg)
                event_info['args'] = event_args

                # sent ，这里的start和end是左闭右闭
                sent = []
                for i, token in enumerate(text):
                    if i == trigger['span'][0]:
                        sent.append('<t>')
                        sent.append(token)
                    elif i == trigger['span'][1]:
                        sent.append('<t>')
                        sent.append(token)
                    else:
                        sent.append(token)
                event_line['sent'] = ' '.join(sent)

                # only structure
                trigger_sent = [first_word_locs[trigger['sent_idx']], end_word_locs[trigger['sent_idx']]]
                if args.structure and not args.occur:
                    sent = []
                    for i, token in enumerate(text):
                        if i == trigger_sent[0]:
                            sent.append('<s>')
                        elif i == trigger_sent[1]:
                            sent.append('<s>')
                        if i == trigger['span'][0]:
                            sent.append('<t>')
                        elif i == trigger['span'][1]:
                            sent.append('<t>')
                        sent.append(token)
                    event_line['sent'] = ' '.join(sent)

                # only occur
                if args.occur and not args.structure:
                    sent = []
                    for i, token in enumerate(text):
                        if i == trigger['span'][0]:
                            sent.append('<t>')
                        elif i == trigger['span'][1]:
                            sent.append('<t>')
                        elif i in trigger_start and i != trigger['span'][0] and i != trigger['span'][1]:
                            sent.append('<T>')
                        elif i in trigger_end and i != trigger['span'][0] and i != trigger['span'][1]:
                            sent.append('<T>')
                        sent.append(token)
                    event_line['sent'] = ' '.join(sent)

                # both occur and structure
                if args.occur and args.structure:
                    sent = []
                    for i, token in enumerate(text):
                        if i == trigger_sent[0]:
                            sent.append('<s>')
                        elif i == trigger_sent[1]:
                            sent.append('<s>')
                        if i == trigger['span'][0]:
                            sent.append('<t>')
                        elif i == trigger['span'][1]:
                            sent.append('<t>')
                        if i in trigger_start and i != trigger['span'][0]:
                            sent.append('<T>')
                        if i in trigger_end and i != trigger['span'][1]:
                            sent.append('<T>')
                        sent.append(token)
                    event_line['sent'] = ' '.join(sent)

                # gt_words
                event_line['gt_words'] = {}
                for arg in event_args:
                    argument = event_args[arg]
                    words = []
                    for ar in argument:
                        words.append(ar['word'])
                    event_line['gt_words'][arg] = words

                event_line['gt'] = event_args
                event_line['type'] = event_type
                event_line['pred_words'] = {}
                event_line['event'] = event_info
                event_line['first_word_locs'] = first_word_locs
                event_line['end_word_locs'] = end_word_locs
                event_line['role_name'] =argument_dict[event_type]

                event_lines.append(event_line)

        return event_lines

    if dataset_type == 'MLEE':
        template_dict, argument_dict = _read_roles('prompt/MLEE_role_name_mapping.json')
        event_lines = []
        with open(res_path) as f:
            lines = f.readlines()
        for i in range(len(lines)):
            lines[i] = json.loads(lines[i].strip())

        for line in lines:
            if not line['events']:
                continue
            events = line['events']
            text = line['context']
            doc_key = line["id"]

            # occur
            event_types = []
            occur_triggers = []
            for event in events:
                event_types.append(event['event_type'])
                occur_triggers.append(event['trigger'])
            trigger_start = []
            trigger_end = []
            for trigger_se in occur_triggers:
                trigger_start.append(trigger_se[0])
                trigger_end.append(trigger_se[1])

            # structure
            sentences = line['sents']
            text_tmp = []
            first_word_locs = []
            end_word_locs = list(np.cumsum([len(sent) for sent in sentences]))
            for sent in sentences:
                first_word_locs.append(len(text_tmp))
                text_tmp += sent

            for i, event in enumerate(events):
                event_line = {}
                event_line['id'] = doc_key + '_event_{}'.format(i)
                event_info = {}
                event_info['occur_event'] = event_types
                event_type = event['event_type']

                # trigger
                event_trigger = event['trigger']
                trigger = {}
                trigger['span'] = [event_trigger[0], event_trigger[1]]
                trigger['word'] = event_trigger[2]
                # event_trigger['text'] = " ".join(context[event_trigger['start']:event_trigger['end']])
                for num, sent_start in enumerate(first_word_locs):
                    if event_trigger[0] >= sent_start and event_trigger[1] <= end_word_locs[num]:
                        trigger['sent_idx'] = num
                event_info['trigger'] = trigger
                event_info['start'] = event_trigger[0]
                event_info['end'] = event_trigger[1]
                event_info['word'] = event_trigger[2]

                # args
                event_args = {}
                for arg_info in event['args']:
                    evt_arg = dict()
                    evt_arg['span'] = [arg_info[0], arg_info[1]]
                    evt_arg['word'] = arg_info[2]
                    role = arg_info[3]
                    if role not in event_args:
                        event_args[role] = [evt_arg]
                    else:
                        event_args[role].append(evt_arg)
                event_info['args'] = event_args

                # sent ，这里的start和end是左闭右闭
                sent = []
                for i, token in enumerate(text):
                    if i == trigger['span'][0]:
                        sent.append('<t>')
                        sent.append(token)
                    elif i == trigger['span'][1]:
                        sent.append('<t>')
                        sent.append(token)
                    else:
                        sent.append(token)
                event_line['sent'] = ' '.join(sent)

                # only structure
                trigger_sent = [first_word_locs[trigger['sent_idx']], end_word_locs[trigger['sent_idx']]]
                if args.structure and not args.occur:
                    sent = []
                    for i, token in enumerate(text):
                        if i == trigger_sent[0]:
                            sent.append('<s>')
                        elif i == trigger_sent[1]:
                            sent.append('<s>')
                        if i == trigger['span'][0]:
                            sent.append('<t>')
                        elif i == trigger['span'][1]:
                            sent.append('<t>')
                        sent.append(token)
                    event_line['sent'] = ' '.join(sent)

                # only occur
                if args.occur and not args.structure:
                    sent = []
                    for i, token in enumerate(text):
                        if i == trigger['span'][0]:
                            sent.append('<t>')
                        elif i == trigger['span'][1]:
                            sent.append('<t>')
                        if i in trigger_start and i != trigger['span'][0]:
                            sent.append('<T>')
                        if i in trigger_end and i != trigger['span'][1]:
                            sent.append('<T>')
                        sent.append(token)
                    event_line['sent'] = ' '.join(sent)

                # both occur and structure
                if args.occur and args.structure:
                    sent = []
                    for i, token in enumerate(text):
                        if i == trigger_sent[0]:
                            sent.append('<s>')
                        elif i == trigger_sent[1]:
                            sent.append('<s>')
                        if i == trigger['span'][0]:
                            sent.append('<t>')
                        elif i == trigger['span'][1]:
                            sent.append('<t>')
                        if i in trigger_start and i != trigger['span'][0]:
                            sent.append('<T>')
                        if i in trigger_end and i != trigger['span'][1]:
                            sent.append('<T>')
                        sent.append(token)
                    event_line['sent'] = ' '.join(sent)

                # gt_words
                event_line['gt_words'] = {}
                for arg in event_args:
                    argument = event_args[arg]
                    words = []
                    for ar in argument:
                        words.append(ar['word'])
                    event_line['gt_words'][arg] = words

                event_line['gt'] = event_args
                event_line['type'] = event_type
                event_line['pred_words'] = {}
                event_line['event'] = event_info
                event_line['first_word_locs'] = first_word_locs
                event_line['end_word_locs'] = end_word_locs
                event_line['role_name'] =argument_dict[event_type]

                event_lines.append(event_line)

        return event_lines

    if dataset_type == 'GENEVA':
        from parameters_geneva import TEMPLATE_GENEVA_Role_Name
        argument_dict = TEMPLATE_GENEVA_Role_Name
        event_lines = []
        with open(res_path) as f:
            lines = f.readlines()
        for i in range(len(lines)):
            lines[i] = json.loads(lines[i].strip())

        for line in lines:
            if not line['event_mentions']:
                continue
            events = line['event_mentions']
            text = line['tokens']
            doc_key = line["wnd_id"]

            event_types = []
            for event in events:
                event_types.append(event['event_type'])

            for i, event in enumerate(events):
                event_line = {}
                event_line['id'] = doc_key + '_event_{}'.format(i)
                event_info = {}
                event_info['occur_event'] = event_types
                event_type = event['event_type']

                # trigger
                event_trigger = event['trigger']
                trigger = {}
                trigger['span'] = [event_trigger['start'], event_trigger['end']]
                trigger['word'] = event_trigger['text']
                event_info['trigger'] = trigger
                event_info['start'] = event_trigger['start']
                event_info['end'] = event_trigger['end']
                event_info['word'] = event_trigger['text']

                # args
                event_args = {}
                for arg_info in event['arguments']:
                    evt_arg = dict()
                    # evt_arg['span'] = [arg_info[0], arg_info[1]]
                    evt_arg['word'] = arg_info['text']
                    role = arg_info['role']
                    if role not in event_args:
                        event_args[role] = [evt_arg]
                    else:
                        event_args[role].append(evt_arg)
                event_info['args'] = event_args

                # sent ，这里的start和end是左闭右闭
                sent = []
                for i, token in enumerate(text):
                    if i == trigger['span'][0]:
                        sent.append('<t>')
                        sent.append(token)
                    elif i == trigger['span'][1]:
                        sent.append('<t>')
                        sent.append(token)
                    else:
                        sent.append(token)
                event_line['sent'] = ' '.join(sent)

                # gt_words
                event_line['gt_words'] = {}
                for arg in event_args:
                    argument = event_args[arg]
                    words = []
                    for ar in argument:
                        words.append(ar['word'])
                    event_line['gt_words'][arg] = words

                event_line['gt'] = event_args
                event_line['type'] = event_type
                event_line['pred_words'] = {}
                event_line['event'] = event_info
                event_line['first_word_locs'] = []
                event_line['end_word_locs'] = []
                event_line['role_name'] =argument_dict[event_type]

                event_lines.append(event_line)

        return event_lines

    else:
        raise NotImplementedError(f"Unexpected Dataset {dataset_type}")
