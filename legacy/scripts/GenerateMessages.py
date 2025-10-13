import json
import os
import argparse


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
    

class EAPrompting:
    def __init__(self, lang_pair, model, use_qe=False, prompt_path = './prompts/'):
        self.lang_pair = lang_pair
        self.model = model
        self.qe = use_qe
        with open(os.path.join(prompt_path, f'prompt_context_{self.lang_pair}.txt'), 'r', encoding='utf-8') as f:
            prompt = f.read()
        self.prompts = self.adjust_prompt(prompt).split('\n\n')


    def adjust_prompt(self, prompt):
        if self.qe:
            # delete reference information & identifiers
            while True:
                try:
                    start_idx = prompt.index('<REF>')
                    end_idx = prompt.index('</REF>') + 6
                    prompt = prompt[:start_idx] + prompt[end_idx:]
                except ValueError:
                    break
        else:
            # delete reference identifiers
            prompt = prompt.replace('<REF>', '').replace('</REF>', '')
                
        return prompt


    def generate_chat_completion_error(self, src, tgt, ref=None):
        # generate message for models like gpt-3.5-turbo or gpt-4
        if self.qe:
            return [
                {"role": "system", "name": "example_user", "content": self.prompts[0]},
                {"role": "system", "name": "example_assistant", "content": self.prompts[1]},
                {"role": "user", "content": 'Source: ' + src + '\nTranslation: ' + tgt + '\n' + self.prompts[2]},
            ]
        else:
            return [
                {"role": "system", "name": "example_user", "content": self.prompts[0]},
                {"role": "system", "name": "example_assistant", "content": self.prompts[1]},
                {"role": "user", "content": 'Source: ' + src + '\nReference: ' + ref + '\nTranslation: ' + tgt + '\n' + self.prompts[2]},
            ]
    
    
    def generate_completion_error(self, src, tgt, ref=None):
        # generate message for models like text-davinci-003 or text-davinci-002
        if self.qe:
            return f"{self.prompts[0]}\n\n{self.prompts[1]}\n\nSource: {src}\nTranslation: {tgt}\n{self.prompts[2]}"
        else:
            return f"{self.prompts[0]}\n\n{self.prompts[1]}\n\nSource: {src}\nReference: {ref}\nTranslation: {tgt}\n{self.prompts[2]}"

    
    def create_messages_error(self, srcs, tgts, refs=None):
        # generate messages for identifying errors
        messages_list = []
        refs = [None] * len(srcs) if self.qe else refs
        assert len(srcs) == len(tgts) == len(refs), 'The lines of sources, targets, (and references) are not equal!'

        for src, tgt, ref in zip(srcs, tgts, refs):
            if self.model.startswith('gpt-'):
                messages_list.append(self.generate_chat_completion_error(src, tgt, ref))
            elif self.model.startswith('text-'):
                messages_list.append(self.generate_completion_error(src, tgt, ref))
                
        return messages_list


    def create_messages_score(self, errors):
        # generate messages for scoring (or counting the number of major/minor errors)
        messages_list = []
        for error_content in errors:
            if self.model.startswith('gpt-'):
                messages_list.append([
                    {"role": "user", "content": error_content + '\n' + self.prompts[3]},
                ])
            elif self.model.startswith('text-'):
                messages_list.append(error_content + '\n' + self.prompts[3])
          
        return messages_list


def main():
    
    parser = argparse.ArgumentParser('Command-line script to use EA prompting')
    parser.add_argument('-l', '--lang', type=str, default='zhen', 
                        help='language pair - zhen, ende, enru')
    parser.add_argument('-q', '--query', type=str, default='error',
                        help='query type - error or score')
    parser.add_argument('-o', '--output', type=str, default='messages.json',
                        help='output path')
    parser.add_argument('-m', '--model', type=str, default='gpt-3.5-turbo',
                        help='the model endpoint used for evaluation')
    parser.add_argument('--ref', type=str, default='',
                        help='reference path')
    parser.add_argument('--src', type=str, default='',
                        help='source text path')
    parser.add_argument('--tgt', type=str, default='',
                        help='translation to be evaluated path')
    parser.add_argument('--err', type=str, default='',
                        help='response of errors information')
    parser.add_argument('--qe', action='store_true', default=False, 
                        help='use reference-less evaluation (quality estimation)')

    args = parser.parse_args()
    
    assert args.lang in ['zhen', 'ende', 'enru'], 'Please provide a language pair in zhen, ende, or enru. '
    assert args.query in ['error', 'score'], 'Please provide a query instruction using "error" or "score". '
    
    # ensure model in openai api list
    if args.model.startswith('gpt-'):
        assert args.model in OPENAI_MODEL_ENDPOINTS['chat_completions'], "please check openai model endpoint name!"
    elif args.model.startswith('text-'):
        assert args.model in OPENAI_MODEL_ENDPOINTS['text_completions'], "please check openai model endpoint name!"
    else:
        raise AssertionError("please check openai model endpoint name!")

    EAP = EAPrompting(lang_pair=args.lang, model=args.model, use_qe=args.qe)
    if args.query == 'error': # generate error instruction
        srcs = read_txt(args.src)
        tgts = read_txt(args.tgt)

        if args.qe:
            messages = EAP.create_messages_error(srcs, tgts)
        else:
            refs = read_txt(args.ref)
            messages = EAP.create_messages_error(srcs, tgts, refs)
    else: # generate score instruction
        errors = read_json(args.err)
        messages = EAP.create_messages_score(errors)

    save_json(messages, args.output)


if __name__ == '__main__':
    main()


# example:
# python GenerateMessages.py -l zhen -q error -o ./test/messages_error.json --src ./test/src_zhen.txt --tgt ./test/tgt_zhen.txt --qe
# python GenerateMessages.py -q score -o ./test/messages_score.json --err ./test/responses_error.json