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


def rerank(
    args,    
    res_list,
    res_list_train,
):
    if not args.model_name.startswith('gpt'):
        if '3.1' in args.model_name:
            tokenizer = AutoTokenizer.from_pretrained(args.model_name)
            model = AutoModelForCausalLM.from_pretrained(
                args.model_name,
                model=args.model_name,
                model_kwargs={"torch_dtype": torch.bfloat16},
                device_map="auto",
            )
        else:
            tokenizer = AutoTokenizer.from_pretrained(args.model_name)
            model = AutoModelForCausalLM.from_pretrained(
                args.model_name,
                device_map="auto",
                torch_dtype=torch.float16,
            )
    
    raw_res_list, prompt_list, raw_res_list_train = list(), list(), list()
    repeated_rerank_res_list=res_list
    for curr in tqdm(range(0, len(repeated_rerank_res_list), args.batch_size)):
        batch_rerank_list = repeated_rerank_res_list[curr:(curr+args.batch_size)]
        batch_demo_list = sample_demonstration(args.data_type)
        batch_prompt = [
            batch_demo_list + [
                {"role": "user", "content": prompt_generation(res, args.data_type, args)[0]}
            ] for res in batch_rerank_list
        ]
        prompt_list.extend(batch_prompt)
        batch_response = generate_response(
            model_or_model_name=model if not args.model_name.startswith('gpt') else args.model_name,
            tokenizer=tokenizer if not args.model_name.startswith('gpt') else None,
            batch_prompt=batch_prompt,
            temperature=args.temperature,
            max_tokens=1024,
            stop='\n',
            device=args.device
        )
        raw_res_list.extend(batch_response)
        break

    merged_prompt_list = list_merge(prompt_list, 1)
    raw_res_list, _ = ensemble_pred_res(raw_res_list, 1, task="RE")
    rerank_gt_list, rerank_pred_list, output_list = list(), list(), list()
    for raw_res, res, prompt in zip(raw_res_list, res_list, merged_prompt_list):
        id, event, content, pred = res["id"], res["event"], res["sent"], res['pred_words']
        gt = res['gt_words']
        try:
            pred = parse_res(raw_res, args.data_type)
        except:
            pred = None
        res['pred_words'] = pred
        rerank_gt_list.append(gt)
        rerank_pred_list.append(pred)
        output = {
            "sent": content,
            "event": event,
            'first_word_locs': res['first_word_locs'],
            'end_word_locs': res['end_word_locs'],
            'role_name': res['role_name']
        }
        output_list.append(output)
    return rerank_gt_list, rerank_pred_list, output_list