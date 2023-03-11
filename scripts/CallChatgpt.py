import openai
import json
import argparse
import backoff  # for exponential backoff
from tqdm import tqdm


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
def completions_with_backoff(**kwargs):
    return openai.ChatCompletion.create(**kwargs)


def main():
    
    parser = argparse.ArgumentParser('Command-line script to use EA prompting')
    parser.add_argument('-k', type=str, required=True,
                        help='api key') 
    parser.add_argument('-m', type=str, required=True, 
                        help='message path')
    parser.add_argument('-t', type=float, default=0,
                        help='temperature')
    parser.add_argument('-o', type=str, default='response.json',
                        help='response path')
    args = parser.parse_args()
    
    openai.api_key = args.k
    messages = read_json(args.m)

    responses = []

    for message in tqdm(messages, desc='Call ChatGPT'):
        response = completions_with_backoff(
            model = "gpt-3.5-turbo",
            messages=message,
            temperature=args.t,
        )
        responses.append(response["choices"][0]["message"]["content"])
    save_json(responses, args.o)


if __name__ == '__main__':
    main()


# example: (replace 'api_key' with your own API key)
# python CallChatGPT.py -m ./test/messages_error.json -t 0 -o ./test/responses_error.json -k api_key
# python CallChatGPT.py -m ./test/messages_score.json -t 0 -o ./test/responses_score.json -k api_key