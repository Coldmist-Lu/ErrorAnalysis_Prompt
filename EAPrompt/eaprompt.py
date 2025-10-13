"""
===============================================================================
EAPrompt Class Implementation
===============================================================================

This module implements the EAPrompt class, which is designed to construct prompt messages (single or batch) in the OpenAI ChatCompletion-style format for translation error analysis and evaluation.

The EAPrompt system merges example contexts, instructions, and evaluation inputs according to a defined prompt type, allowing systematic construction of prompts for multi-lingual translation assessment.

------------------------------------------------------------------------------
Structure Overview
------------------------------------------------------------------------------
1. **CONTEXT_VAR_MAP**  
   Dynamically loads all uppercase constants (example and instruction strings)
   from `constants.context`.

2. **PROMPT_TYPE_CONFIGS**  
   Defines the valid components for prompt type parsing:
       - STEP: "ERROR" or "SINGLESTEP"
       - LANG: language pair (e.g., "ENDE", "ENRU", "ZHEN")
       - DEMO: demonstration type ("DETAILED" or "ITEMIZED")
       - IS_REF: whether reference translation is used ("SRC" or "REF")

3. **EAPrompt Class**
   - `generate_query(eval_input)`:
       Generates a single formatted query for one evaluation sample.
   - `generate_queries_batch(eval_inputs)`:
       Generates multiple queries for batch evaluation.
   - Internal helpers `_set_prompt_error` and `_set_prompt_count`:
       Build prompts for specific evaluation modes.

===============================================================================
"""

import constants.context

from utils import parse_type

CONTEXT_VAR_MAP = {k: v for k, v in vars(constants.context).items() if k.isupper()} # loading context string variables

PROMPT_TYPE_CONFIGS = {
    "STEP": ["ERROR", "SINGLESTEP"], # "COUNT" is not included here; it is handled separately in the "set_prompt_count" function.
    "LANG": ["ENDE", "ENRU", "ZHEN"], # language pair
    "DEMO": ["DETAILED", "ITEMIZED"], # type of error demonstration
    "IS_REF": ["SRC", "REF"], # reference-free (SRC) or reference-based (REF)
}

class EAPrompt:
    def __init__(self, prompt_type: str="ERROR_ZHEN_ITEMIZED_REF") -> None:    
        self.prompt_type = prompt_type
        
    def set_prompt_type(self, prompt_type: str) -> None:
        self.prompt_type = prompt_type
        
    def generate_query(self, eval_input) -> list[dict[str, str]]:
        
        """
        Generate single query. 
        Input can be in dictionary format (e.g. {"src": "xxx", "ref": "xxx", "tgt": "xxx"}) or error_text.

        Returns:
            query in Openai API format.
        """
        
        if "COUNT" in self.prompt_type:
            return self._set_prompt_count(eval_input)
        else:
            return self._set_prompt_error(self.prompt_type, eval_input)
        
    def generate_queries_batch(self, eval_inputs) -> list[list[dict[str, str]]]:
        """
        Generate queries from a list of eval_inputs.
        Return messages in batch.
        """
        return [self.generate_query(_eval_input) for _eval_input in eval_inputs]
    
    def _set_prompt_error(self, prompt_type: str, eval_input: dict[str, str]) -> list[dict[str, str]]:
    
        """
        Merge the prompt context according to the given prompt_type.
        "COUNT" is not included here; it is handled separately in the "set_prompt_count" function.
        
        prompt_type: 
            prompt_type should be in the following format: "{STEP}_{LANG}_{DEMO}_{IS_REF}". 
            For example, "ERROR_ZHEN_ITEMIZED_REF".
        
        eval_input: {
            "src": "xxx",
            "tgt": "xxx", # the segment of translation to be evaluated.
            "ref": "xxx" = None, # the reference translation
        }
        """
        
        if "COUNT" in prompt_type:
            assert ValueError("Type 'COUNT' is not included in this function!")
            return
                
        is_valid, prompt_info = parse_type(type_configs=PROMPT_TYPE_CONFIGS, prompt_type_str=prompt_type)
        
        if is_valid is False:
            assert ValueError(f"Prompt type {prompt_type} is not valid!")
            return
        
        _step, _lang, _demo, _is_ref = prompt_info["STEP"], prompt_info["LANG"], prompt_info["DEMO"], prompt_info["IS_REF"]
        
        if _step == "ERROR":
            
            example_user_part1 = CONTEXT_VAR_MAP[f"EXAMPLE_{_lang}_{_is_ref}"].strip()
            example_user_part2 = CONTEXT_VAR_MAP[f"INSTRUCTION_ERROR_{_is_ref}"].strip()
            example_assistant = CONTEXT_VAR_MAP[f"EXAMPLE_ERROR_{_demo}_{_lang}"].strip()
            user_part1 = CONTEXT_VAR_MAP[f"EVALUATION_INPUT_{_is_ref}"].format(**eval_input).strip()
            user_part2 = CONTEXT_VAR_MAP[f"INSTRUCTION_ERROR_{_is_ref}"].strip()
            
            return [
                {"role": "user", "content": example_user_part1 + "\n" + example_user_part2},
                {"role": "assistant", "content": example_assistant},
                {"role": "user", "content": user_part1 + "\n" + user_part2},
            ]
            
        elif _step == "SINGLESTEP": # combine identifying and counting errors
            
            example_user_part1 = CONTEXT_VAR_MAP[f"EXAMPLE_{_lang}_{_is_ref}"].strip()
            example_user_part2 = CONTEXT_VAR_MAP[f"INSTRUCTION_SINGLESTEP_{_is_ref}"].strip()
            example_assistant_part1 = CONTEXT_VAR_MAP[f"EXAMPLE_ERROR_{_demo}_{_lang}"].strip()
            example_assistant_part2 = CONTEXT_VAR_MAP[f"EXAMPLE_COUNT_{_lang}"].strip()
            user_part1 = CONTEXT_VAR_MAP[f"EVALUATION_INPUT_{_is_ref}"].format(**eval_input).strip()
            user_part2 = CONTEXT_VAR_MAP[f"INSTRUCTION_SINGLESTEP_{_is_ref}"].strip()
            
            return [
                {"role": "user", "content": example_user_part1 + "\n" + example_user_part2},
                {"role": "assistant", "content": example_assistant_part1 + "\n" + example_assistant_part2},
                {"role": "user", "content": user_part1 + "\n" + user_part2},
            ]
            
    def _set_prompt_count(self, error_text: str) -> list[dict[str, str]]:
    
        return [
            {"role": "user", "content": f"{error_text}\n{CONTEXT_VAR_MAP['INSTRUCTION_COUNT']}"}
        ]

if __name__ == '__main__':
    
    eval_input_batch = [
        {"src": "你好!", "tgt": "Hello!", "ref": "Hello!"},
        {"src": "我爱你", "tgt": "I love you", "ref": "I love you"}
    ]

    # Initialize the EAPrompt object, assuming we are testing in "ERROR" mode
    EAP = EAPrompt(prompt_type="ERROR_ZHEN_ITEMIZED_REF")

    # Test a single input
    single_result = EAP.generate_query(eval_input_batch[0])
    print("Single query result:\n", single_result)

    # Test batch input
    batch_result = EAP.generate_queries_batch(eval_input_batch)
    print("\nBatch query result:")
    for r in batch_result:
        print(r)