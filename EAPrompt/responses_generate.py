"""
===============================================================================
Response Generation Pipeline for EAPrompt Evaluation
===============================================================================

This script executes the second stage of the **EAPrompt** evaluation framework, 
performing model inference to generate translation error analysis responses.

It reads pre-generated prompt queries (from `results/queries/...`), sends them 
to the specified LLM through the `InferenceEngine`, and saves the resulting 
model responses for downstream evaluation.

------------------------------------------------------------------------------
Workflow Overview
------------------------------------------------------------------------------
1. **Input Setup**
   - `lang_pair` defines the translation language pair (e.g., "ende", "zhen").
   - `prompt_type` specifies the evaluation configuration 
     (e.g., "ERROR_ZHEN_ITEMIZED_REF" or "ERROR_ZHEN_SINGLESTEP_REF").
   - `model_name` must match one of the model identifiers defined in 
     `constants.model_configs`.
   - Input queries are read from `./results/queries/<lang_pair>/<prompt_type>/`.

2. **Inference**
   - Initializes an `InferenceEngine` for the selected model.
   - If using a two-step evaluation (error + count), a separate 
     `EAPrompt(prompt_type="COUNT")` is used to construct count queries.
   - For each system file, runs inference on all queries via `infer_batch()`.

3. **Response Generation**
   - For SINGLESTEP mode:
       → Stores model outputs in `"singlestep_response"`.
   - For two-step mode:
       → Generates count queries from the error responses and stores both
         `"error_response"` and `"count_response"` fields.

4. **Output**
   - Saves all annotated responses to  
     `./results/responses/<lang_pair>/<model_name>/<prompt_type>/`
     using the same filenames as the input query JSONs.

------------------------------------------------------------------------------
Notes
------------------------------------------------------------------------------
- Make sure the model configuration in `constants/model_configs.py`
  correctly defines API key, base URL, and model path.
- Ensure query files are generated beforehand using the batch query script.
- This script supports both single-step and two-step evaluation modes.

===============================================================================
"""

import os
from inference import InferenceEngine
from eaprompt import EAPrompt
from utils import read_json, save_json

#### Parameters

lang_pair = 'ende'
prompt_type = f"ERROR_{lang_pair.upper()}_ITEMIZED_REF"
model_name = "/model/name/in/config"
queries_folder = f"./results/queries/{lang_pair}/{prompt_type}/" # release version
responses_folder = f"./results/responses/{lang_pair}/{model_name}/{prompt_type}"
os.makedirs(responses_folder, exist_ok=True)

#### Response Generation Pipeline

generator = InferenceEngine(model_name=model_name)

EAP = EAPrompt(prompt_type="COUNT") # use when two-step querying

for file_name in os.listdir(queries_folder):
    
    print(f"MT system name: {file_name}")
    
    queries_file = read_json(os.path.join(queries_folder, file_name))
    queries = [_query_dict["query"] for _query_dict in queries_file]
    responses = generator.infer_batch(queries)
    
    if "SINGLESTEP" in prompt_type: # single step querying
        for _query_dict, _response in zip(queries_file, responses):
            _query_dict["singlestep_response"] = _response
            
    else:
        count_queries = EAP.generate_queries_batch(responses)
        print("Generating Count Responses:")
        count_responses = generator.infer_batch(count_queries)
        
        for _query_dict, _response, _count_response in zip(queries_file, responses, count_responses):
            _query_dict["error_response"] = _response
            _query_dict["count_response"] = _count_response
            
    save_json(queries_file, os.path.join(responses_folder, file_name))