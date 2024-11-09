import copy
import json
import os

import torch
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForCausalLM
from utils import parse_res, ensemble_pred_res, list_merge
from preprocess import get_pre_instruct
from LLM_wrapper import generate_response


def prompt_generation(res, data_type, args):
    TEMPLATE_Role_Name, TEMPLATE_Demo, disappear_type = get_pre_instruct(data_type)

    sentence = res["sent"]
    event_type = res['type']
    event_trigger = res['event']['trigger']
    event_occur = res['event']['occur_event']
    if data_type == 'WikiEvent':
        if event_type == 'Contact.RequestCommand.Meet':
            event_type = 'Contact.RequestCommand.Unspecified'
        if event_type in disappear_type:
            event_type = 'Contact.RequestCommand.Unspecified'
    all_role = ''
    for i, role in enumerate(TEMPLATE_Role_Name[event_type]):
        all_role += role
        if i < len(TEMPLATE_Role_Name[event_type])-1:
            all_role += ', '

    if args.occur and not args.structure and data_type in ['RAMS', 'WikiEvent', 'MLEE']:
        input = "1 - The trigger word '{}' marked with <t> triggers a {} event " \
                "and all trigger words that trigger other events are marked by <T>.\n".format(event_trigger['word'], event_type)
    elif args.structure and not args.occur and data_type in ['RAMS', 'WikiEvent', 'MLEE']:
        input = "1 - The trigger word '{}' marked with <t> triggers a {} event. " \
                "Additionally, you need to pay close attention to the sentence marked by <s> in the document.\n".format(event_trigger['word'], event_type)
    elif args.structure and args.occur and data_type in ['RAMS', 'WikiEvent', 'MLEE']:
        input = "1 - The trigger word '{}' marked with <t> triggers a {} event and all trigger words that trigger other events are marked by <T>. " \
                "Additionally, you need to pay close attention to the sentence marked by <s> in the document.\n".format(event_trigger['word'], event_type)
    else:
        input = "1 - The trigger word '{}' marked with <t> triggers a {} event. \n".format(event_trigger['word'],event_type)
    input += "2 - The event '{}' corresponds to the list of roles: ".format(event_type)
    input += "{}. \n".format(all_role)
    input += "3 - Please output the role names and their corresponding arguments in JSON format.\n"
    demo = TEMPLATE_Demo[event_type]
    input += "4 - I will give you an example as follows: \n{}.\n\n".format(demo)
    if data_type in ['RAMS', 'WikiEvent', 'MLEE']:
        input += "Document: <doc> {} <doc>\n\n".format(sentence)
    else:
        input += "Sentence: <sent> {} <sent>\n\n".format(sentence)

    output = None
    return input, output


def sample_demonstration(data_type):
    if data_type in ['RAMS', 'WikiEvent']:
        demo_prompt = [
            {
                "role": "system",
                "content": "You will perform event argument extraction tasks in the news domain. "
                           "Please follow the steps below to identify the arguments corresponding to the given roles in the document marked by <doc>. "
                           "If a role does not have a corresponding argument, strictly output None. "
                           "In step 4, I will provide you with an example marked by <eg>."
            }
        ]
    elif data_type == 'GENEVA':
        demo_prompt = [
            {
                "role": "system",
                "content": "You will perform event argument extraction tasks. "
                           "Please follow the steps below to identify the arguments corresponding to the given roles in the sentence marked by <sent>. "
                           "If a role does not have a corresponding argument, strictly output None. "
                           "In step 4, I will provide you with an example marked by <eg>."
            }
        ]
    elif data_type == 'MLEE':
        demo_prompt = [
            {
                "role": "system",
                "content": "You will perform event argument extraction tasks in the medical domain. "
                           "Please follow the steps below to identify the arguments corresponding to the given roles in the document marked by <doc>. "
                           "If a role does not have a corresponding argument, strictly output None. "
                           "In step 4, I will provide you with an example marked by <eg>."
            }
        ]
    elif data_type == 'ACE':
        # demo_prompt = [
        #     {
        #         "role": "system",  # system角色用于描述任务，例如这里就将其描述为一个做选择题的任务
        #         "content": "You will perform event argument extraction tasks. "
        #                    "Please follow the steps below to identify the arguments corresponding to the given roles in the sentence marked by <sent>. "
        #                    "If a role does not have a corresponding argument, strictly output None. "
        #                    "In step 4, I will provide you with an example marked by <eg>."
        #     }
        # ]
        demo_prompt = [
            {
                "role": "system",
                "content": "You will perform event argument extraction tasks in the news domain. "
                           "Please follow the steps below to identify the arguments corresponding to the roles in the sentence delimited by <sent>. "
                           "If a role does not have a corresponding argument, strictly output None. "
                           "In step 4, I will provide you with an example marked by <eg>."
            }
        ]
    else:
        raise NotImplementedError(f"Unexpected Dataset {data_type}")
    return demo_prompt


def sample_output(batch_res, data_type):
    TEMPLATE_Role_Name, TEMPLATE_Demo, disappear_type = get_pre_instruct(data_type)
    demo_prompt = []
    for res in batch_res:
        args = copy.deepcopy(res['gt_words'])
        for arg in args:
            arg_words = args[arg]
            word = ''
            for i, arg_word in enumerate(arg_words):
                word += arg_word
                if i < len(arg_words) - 1:
                    word += ', '
            args[arg] = word
        event_type = res['type']

        if data_type == 'WikiEvent':
            if event_type == 'Contact.RequestCommand.Meet':
                event_type = 'Contact.RequestCommand.Unspecified'
            if event_type in disappear_type:
                event_type = 'Contact.RequestCommand.Unspecified'

        for arg in TEMPLATE_Role_Name[event_type]:
            if arg not in args:
                args[arg] = None
        args = json.dumps(args, ensure_ascii=False)
        output = {
            "role": "output",
            "content": args
        }
        demo_prompt.append(output)

    return demo_prompt

def rerank(
    args,    
    res_list,
    res_list_train,
):
    if not args.model_name.startswith('gpt'):
        tokenizer = AutoTokenizer.from_pretrained(args.model_name)
        model = AutoModelForCausalLM.from_pretrained(
            args.model_name,
            device_map="auto",
            torch_dtype=torch.float16,
        )
    
    raw_res_list, prompt_list, raw_res_list_train, prompt_list_train = list(), list(), list(), list()
    repeated_rerank_res_list=res_list_train
    for curr in tqdm(range(0, len(repeated_rerank_res_list), args.batch_size)):
        batch_rerank_list = repeated_rerank_res_list[curr:(curr+args.batch_size)]
        batch_demo_list = sample_demonstration(args.data_type)
        batch_prompt = [
            batch_demo_list + [
                {"role": "user", "content": prompt_generation(res, args.data_type, args)[0]}
            ] for res in batch_rerank_list
        ]
        output = sample_output(batch_rerank_list, args.data_type)

        for index, prompt in enumerate(batch_prompt):
            prompt.append(output[index])
        prompt_list_train.extend(batch_prompt)

    prompt_list_train_output = []
    for prompt in prompt_list_train:
        final_data = {}
        assert (prompt[0]['role'] == 'system' and prompt[1]['role'] == 'user' and prompt[2]['role'] == 'output')
        final_data['instruction'] = prompt[0]['content']
        final_data['input'] = prompt[1]['content']
        final_data['output'] = prompt[2]['content']
        prompt_list_train_output.append(final_data)


    with open(os.path.join('./datasets/RAMS/', "cs-new.json"), 'w', encoding='utf-8') as f:
        json.dump(prompt_list_train_output, f, ensure_ascii=False)
    assert (0==1)
