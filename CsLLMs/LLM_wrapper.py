import backoff
import openai
import asyncio
from openai import OpenAI

client = OpenAI(
    api_key='',  # 100 new
    base_url="https://api.chatanywhere.tech/v1"
)


def completions_with_backoff(**kwargs):
    return client.chat.completions.create(**kwargs)


async def dispatch_openai_requests(messages_list, model, temperature):
    """Dispatches requests to OpenAI API asynchronously.
    
    Args:
        messages_list: List of messages to be sent to OpenAI ChatCompletion API.
        model: OpenAI model to use.
        temperature: Temperature to use for the model.
        max_tokens: Maximum number of tokens to generate.
        top_p: Top p to use for the model.
    Returns:
        List of responses from OpenAI API.
    """
    async_responses = [
        completions_with_backoff(
            model=model,
            messages=x,
            temperature=temperature,
        )for x in messages_list
    ]
    return async_responses

def generate_response(
    model_or_model_name, 
    batch_prompt, 
    temperature=0.7, 
    stop='\n', 
    max_tokens=128,
    tokenizer=None, 
    device="cuda"
):
    if isinstance(model_or_model_name, str):
        model_name = model_or_model_name
        response = asyncio.run(
            dispatch_openai_requests(
                model=model_name,
                messages_list=batch_prompt,
                temperature=temperature,
            )
        )
        response = [
            x.choices[0].message.content for x in response
        ]  # 官方文档中为：response.choices[0].message['content']
        return response

    else:
        model = model_or_model_name
        # `temperature` has to be a strictly positive float
        if temperature<=0.0:
            do_sample = False
            temperature += 0.1
        if stop=='\n':
            stop_word_id = tokenizer.convert_tokens_to_ids('<0x0A>')    # '\n'
        else:
            stop_word_id = None
    
        batch_response = list()
        for prompt in batch_prompt:
            inputs = "\n".join([e["content"] for e in prompt])+"\n"
            a = inputs
            inputs = tokenizer(inputs, return_tensors="pt")
            input_ids_length = inputs.input_ids.size(1)
            # while True:
            generate_ids = model.generate(
                inputs.input_ids.to(device),
                max_new_tokens=max_tokens,  # 生成的最大令牌数
                do_sample=do_sample,
                temperature=temperature,
                eos_token_id=stop_word_id,
                pad_token_id=tokenizer.pad_token_id if tokenizer.pad_token_id else 0,
                early_stopping=True
            )
            response = tokenizer.batch_decode(generate_ids[:, input_ids_length:], skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
            if stop in response:
                response = response.split(stop)[0]
            batch_response.append(response.rstrip('\n'))

        return batch_response
