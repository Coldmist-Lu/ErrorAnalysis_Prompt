"""
===============================================================================
Inference Engine for GPT and Other LLMs
===============================================================================

This module defines the `InferenceEngine` class for unified inference across multiple Large Language Models (LLMs), including OpenAI and locally hosted models.

It provides a batch-based API for sending chat-style prompts (formatted in the OpenAI message schema) and retrieving corresponding model responses with built-in retry, timeout, and progress visualization.

------------------------------------------------------------------------------
Key Features
------------------------------------------------------------------------------
1. **Model Configuration**
   - Uses configuration objects defined in `constants.model_configs`
     via the `OpenAIConfig` dataclass.
   - Supports both OpenAI API endpoints and custom local inference servers.

2. **Batch Inference**
   - `infer_batch(queries_list)`: accepts a list of conversations (each a list of 
     message dictionaries) and returns the model responses in order.
   - Automatically retries failed requests up to a user-defined limit (`max_retry`),
     with configurable sleep intervals (`retry_sleep`).

3. **Robustness and Monitoring**
   - Includes timeout handling per request.
   - Displays progress via `tqdm` progress bars.
   - Logs and gracefully handles transient connection or rate-limit errors.

===============================================================================
"""

import time

from openai import OpenAI
from tqdm import tqdm
from constants.model_configs import OpenAIConfig, MODEL_CONFIGS

class InferenceEngine:

    def __init__(self, 
                 model_name: str) -> None:
        
        self.model_name = model_name
        self.cfg: OpenAIConfig = MODEL_CONFIGS[self.model_name]
        
        self.client = OpenAI(
            api_key=self.cfg.api_key,
            base_url=self.cfg.base_url,
            timeout=self.cfg.request_timeout,
        )
            

    def infer_batch(
        self,
        queries_list: list[list[dict[str, str]]]):
        
        """
        Batch inference:
        - messages_list: each element is either a conversation (list of messages) 
        or a single user string
        - Returns: the model response (string) for each conversation
        """
        
        outputs = []

        for query_message in tqdm(queries_list, desc="LLM Inference"):
            retry_count = 0
            while True:
                try:
                    response = self.client.chat.completions.create(
                        model=self.cfg.model_name,
                        messages=query_message,
                        temperature=self.cfg.temperature,
                        max_tokens=self.cfg.max_tokens
                    )

                    break
                
                except Exception as e:
                    print(e)
                    print("retry.")
                    retry_count += 1
                    if retry_count >= self.cfg.max_retry:
                        raise RuntimeError(f"Request failed after {self.cfg.max_retry} retries: {e}")
                    time.sleep(self.cfg.retry_sleep)

            outputs.append(response.choices[0].message.content)

        return outputs


if __name__ == "__main__":
    
    test_messages_list = [
        [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"}
        ],
        [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "I love you!"}
        ]
    ]
    
    engine = InferenceEngine(model_name="/model/name/in/config")
    
    responses = engine.infer_batch(test_messages_list)
    
    print(responses)