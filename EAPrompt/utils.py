"""
===============================================================================
Utility functions for file I/O, text handling, and prompt type parsing.
===============================================================================

Includes:
- JSON and text read/write helpers (`read_json`, `save_json`, `readlines_txt`, etc.)
- Response truncation via keyword-based cutoff (`truncate_response`)
- Prompt type parsing for EAPrompt configuration (`parse_type`)

Designed for lightweight, reusable data processing in EAPrompt pipelines.
"""

import json

def truncate_response(response: str, truncate_list: list[str], start_truncation_len: int) -> str:
    """
    response: the raw response requires truncating.
    truncate_list: a list of truncation keywords.
    start_truncation_len: the minimum length of truncation
    
    return: response after truncation.
    """
    for keyword in truncate_list:
        if len(response) <= start_truncation_len:
            response = response
        else:
            response = response[:start_truncation_len] + response[start_truncation_len:].split(keyword)[0]
    return response

def read_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f'Saved to {path}.')
    return

def readlines_txt(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    return lines

def read_txt(path):
    with open(path, 'r', encoding='utf-8') as f:
        file = f.read()
    return file

def savelines_txt(file, path):
    with open(path, 'w') as f:
        f.writelines(file)
    print(f'Saved to {path}.')
    return

def parse_type(type_configs, prompt_type_str: str):
    """parse prompt type str into a dict = {"STEP": "xx", "LANG": "xx", ...} according to PROMPT_TYPE_CONFIGS."""

    keys = list(type_configs.keys())
    parts = prompt_type_str.split("_")

    if len(parts) != len(keys):
        return False, None
    
    parsed = {}
    for key, part in zip(keys, parts):
        if part not in type_configs[key]:
            return False, None
        parsed[key] = part
    
    return True, parsed