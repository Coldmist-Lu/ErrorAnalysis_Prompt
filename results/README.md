# Results

We provide the responses of LLMs generated using Error Analysis Prompting in the following files for further study and reference.

## Queries

**📥 Download**

The query files (~1.7 GB) can be downloaded from this [link](https://drive.google.com/file/d/124jlFXzjgECKVGG7FAxA2zp2Gq_yTS0I/view?usp=sharing).

**📂 Folder Structure**

```
queries/
    └── <language_pair>/                # e.g., ende
        └── <prompt_type>/              # e.g., ERROR_ENDE_ITEMIZED_REF
            └── <system_name>.json      # e.g., bleu_bestmbr.json
```

**📄 JSON Format**

Each JSON file contains several testing samples, formatted as follows:

```json
{
    "inputs": {
        "srcs": "<source segment>",
        "tgt": "<target segment>",
        "ref": "<reference translation (if applicable)>"
    },
    "query": [
        // a list of messages performing error analysis in the OpenAI Chat format
    ]
}
```

Researchers can directly use the messages under "query" as prompts when testing or comparing different LLM-based evaluators.

## Responses

**📥 Download**

The response files (~4.5 GB) can be downloaded from this [link](https://drive.google.com/file/d/1I_juOKze9BoraByWnBk-yc_S9-a_D_4M/view?usp=sharing).

**📂 Folder Structure**

```
responses/
    └── <language_pair>/                # e.g., ende
        └── <model_name>/               # e.g., gpt-3.5-turbo
            └── <prompt_type>/          # e.g., ERROR_ENDE_ITEMIZED_REF
                └── <system_name>.json  # e.g., bleu_bestmbr.json
```

**📄 JSON Format**

Each JSON file contains the LLM’s corresponding outputs for the given queries, formatted as follows:

```json
{
    "inputs": {
        "srcs": "<source segment>",
        "tgt": "<target segment>",
        "ref": "<reference translation (if applicable)>"
    },
    "query": [
        // a list of messages performing error analysis in the OpenAI Chat format
    ],
    "error_response": "<model response providing error demonstration>",
    "count_response": "<model response reporting the number of major and minor errors>",
    "singlestep_response": "<combined response for SINGLESTEP-xx type prompts, containing both error and count outputs>"
}
```

These files are provided for future analysis and comparison within this study.
> Please note that for zh–en, the GPT-4 responses include only **30 samples** per system.
The segment IDs corresponding to these samples can be found in **[gpt_random_sent_ids.json](./results/gpt_random_sent_ids.json)**.