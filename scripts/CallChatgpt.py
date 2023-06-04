import openai
import json
import argparse
import backoff  # for exponential backoff
from tqdm import tqdm


OPENAI_MODEL_ENDPOINTS = {
    'chat_completions': 'gpt-4, gpt-4-0314, gpt-4-32k, gpt-4-32k-0314, gpt-3.5-turbo, gpt-3.5-turbo-0301'.split(', '),
    'text_completions': 'text-davinci-003, text-davinci-002, text-curie-001, text-babbage-001, text-ada-001'.split(', ')
}


def read_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f'Saved to {path}.')
    return


def read_txt(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    return lines


@backoff.on_exception(backoff.expo, openai.error.RateLimitError)
def chat_completions_with_backoff(**kwargs):
    return openai.ChatCompletion.create(**kwargs)

@backoff.on_exception(backoff.expo, openai.error.RateLimitError)
def text_completions_with_backoff(**kwargs):
    return openai.Completion.create(**kwargs)


def main():
    
    parser = argparse.ArgumentParser('Command-line script to use EA prompting')
    parser.add_argument('-m', '--model', type=str, required=True,
                        help='model endpoint')
    parser.add_argument('-k', '--key', type=str, required=True,
                        help='api key')
    parser.add_argument('-p', '--path', type=str, required=True, 
                        help='prompt path')
    parser.add_argument('-t', '--temperature', type=float, default=0,
                        help='temperature')
    parser.add_argument('-o', '--output', type=str, default='response.json',
                        help='response path')
    args = parser.parse_args()
    
    openai.api_key = args.key
    prompts = read_json(args.path)

    responses = []

    if args.model.startswith('gpt-'):
        assert args.model in OPENAI_MODEL_ENDPOINTS['chat_completions'], "please check openai model endpoint name!"
        # call chatcompletion api:
        for prompt in tqdm(prompts, desc=f"Call {args.model}"):
            response = chat_completions_with_backoff(
                model=args.model,
                messages=prompt,
                temperature=args.temperature,
            )
            responses.append(response["choices"][0]["message"]["content"])

    elif args.model.startswith('text-'):
        assert args.model in OPENAI_MODEL_ENDPOINTS['text_completions'], "please check openai model endpoint name!"
        # call text completion api:
        for prompt in tqdm(prompts, desc=f"Call {args.model}"):
            response = text_completions_with_backoff(
                model=args.model,
                prompt=prompt,
                temperature=args.temperature,
                max_tokens=300,
            )
            responses.append(response["choices"][0]["text"])

    else:
        raise AssertionError("please check openai model endpoint name!")

    save_json(responses, args.output)


if __name__ == '__main__':
    main()


# example:
# python CallChatgpt.py -m gpt-3.5-turbo -p ./test/messages_error.json -t 0 -o ./test/responses_error.json -k <api.key>
# python CallChatgpt.py -m gpt-3.5-turbo -p ./test/messages_score.json -t 0 -o ./test/responses_score.json -k <api.key>