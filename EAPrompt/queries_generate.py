"""
===============================================================================
Batch Query Generation for Translation Evaluation (EAPrompt)
===============================================================================

This script automates the batch generation of translation evaluation queries 
using the **EAPrompt** framework. It constructs OpenAI-style prompt messages 
for each translation system output under a given dataset and language pair.

------------------------------------------------------------------------------
Workflow Overview
------------------------------------------------------------------------------
1. **Input Data**
   - Source, reference, and system translation files are loaded from the 
     specified dataset directory (e.g., `wmt22/zhen`).
   - File paths are constructed dynamically based on `lang_pair` and dataset name.

2. **Prompt Construction**
   - An `EAPrompt` object is initialized with a specific `prompt_type`
     (e.g., `"ERROR_ZHEN_ITEMIZED_SRC"` or `"ERROR_ZHEN_ITEMIZED_REF"`).
   - Each input triple (`src`, `tgt`, `ref`) is formatted into evaluation prompts 
     according to the prompt context templates defined in `constants.context`.

3. **Batch Processing**
   - The script iterates through each system output file in the target folder,
     generates evaluation queries for all segments, and stores them as JSON files.
   - Each output file includes both the original input data and the generated
     message sequence for downstream inference.

4. **Output**
   - Results are saved to `./results/queries/<lang_pair>/<prompt_type>/`
     with filenames corresponding to each translation system (e.g., `Online-A.json`).

------------------------------------------------------------------------------
Notes
------------------------------------------------------------------------------
- Ensure all source, reference, and translation files have the same length.
- For reference-free prompts, set `prompt_type` to a `_SRC` variant.
- Generated query JSON files are used directly by the inference engine
  for LLM-based translation evaluation.

===============================================================================
"""

import os
import os.path as osp

from eaprompt import EAPrompt

from utils import (
    save_json, 
    readlines_txt
)

# Parameters (edit if needed)
data_folder = "./EAPrompt/wmt22/" # release version
dataset, lang_pair = 'wmt22', 'zhen'
prompt_type = f"ERROR_{lang_pair.upper()}_ITEMIZED_SRC"
output_folder = f"./results/queries/{lang_pair}/{prompt_type}"

# locate data paths
src_lang, tgt_lang = lang_pair[:2], lang_pair[2:]
srcs_path = osp.join(data_folder, f"{dataset}/{dataset}.{lang_pair}.src.{src_lang}")
refs_path = osp.join(data_folder, f"{dataset}/{dataset}.{lang_pair}.ref.{tgt_lang}")
tgts_folder = osp.join(data_folder, f"{dataset}/{dataset}.{lang_pair}.sys.{tgt_lang}")

# create EAPrompt object
EAP = EAPrompt(prompt_type=prompt_type)

# create output folder
os.makedirs(output_folder, exist_ok=True)

# generate error queries for each system
for file in os.listdir(tgts_folder):
    
    system = ".".join(file.split('.')[2:-1]) # extract system name, such as "Online-A"
    
    # read files
    srcs = readlines_txt(srcs_path)
    refs = readlines_txt(refs_path)
    tgts = readlines_txt(osp.join(tgts_folder, file))
    assert len(srcs) == len(refs) == len(tgts), f"Length mismatch: srcs({len(srcs)}), refs({len(refs)}), tgts({len(tgts)})"
    
    # transform into inputs
    if "REF" in prompt_type:
        eval_inputs = [{
            "src": _src,
            "tgt": _tgt,
            "ref": _ref
        } for _src, _tgt, _ref in zip(srcs, tgts, refs)]
    else:
        eval_inputs = [{
            "src": _src,
            "tgt": _tgt,
        } for _src, _tgt, _ref in zip(srcs, tgts, refs)]
    
    # generate queries
    queries = EAP.generate_queries_batch(eval_inputs)
    
    # attach queries message with input
    results = [{
        "inputs": _eval_inputs,
        "query": _query
    } for _eval_inputs, _query in zip(eval_inputs, queries)]
    
    # save
    save_json(results, osp.join(output_folder, f"{system}.json"))