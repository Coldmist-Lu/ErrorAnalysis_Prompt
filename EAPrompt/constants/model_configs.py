"""
===============================================================================
LLM Configuration File
===============================================================================

This file defines model configuration settings for use in `inference.py`.

Each model is represented as an instance of the `OpenAIConfig` dataclass, 
which specifies the following key parameters:
    - base_url:       The endpoint for the model API or local inference server
    - api_key:        Authentication key for API access
    - model_name:     Name or path of the model to be used
    - temperature:    Sampling temperature for generation (default: 0)
    - max_tokens:     Maximum number of tokens to generate per request
    - request_timeout: Timeout for API requests in seconds
    - max_retry:      Maximum number of retry attempts for failed requests
    - retry_sleep:    Sleep time (in seconds) between retries

The `MODEL_CONFIGS` dictionary contains pre-defined configurations for multiple LLMs, including OpenAI and locally hosted models such as Llama 2 and Mixtral. 

These configurations can be imported and used directly by the inference script.
===============================================================================
"""

from dataclasses import dataclass

@dataclass
class OpenAIConfig:
    base_url: str
    api_key: str
    model_name: str
    temperature: float = 0
    max_tokens: int = 256
    request_timeout: int = 10
    max_retry: int = 5
    retry_sleep: int = 5


MODEL_CONFIGS: dict[str, OpenAIConfig] = {
    
    "GPT-3.5-Turbo": OpenAIConfig(
        model_name="gpt-3.5-turbo",
        api_key="enter/your/key",
        base_url="base_url",
    ),
    
    "GPT-4": OpenAIConfig(
        model_name="gpt-4-preview",
        api_key="enter/your/key",
        base_url="base_url",
    ),
    
    "Llama2-70b-Chat": OpenAIConfig(
        model_name="path/to/local/llama2_model",
        base_url="path/to/vllm/server",
        api_key="enter/your/key",
        temperature=0,
        max_tokens=256,
        request_timeout=40, # more inference time because of larger model
    ),
    
    "Mixtral-8x7b-Instruct": OpenAIConfig(
        model_name="path/to/local/mixtral_model",
        base_url="path/to/vllm/server",
        api_key="enter/your/key",
        temperature=0,
        max_tokens=256,
        request_timeout=40,
    ),
}