<h1 align="center">EAPrompt: Error Analysis Prompting Enables Human-Like Translation Evaluation in Large Language Models</h1>

<p align="center">
📄 <a href="https://aclanthology.org/2024.findings-acl.520.pdf"><b>Paper</b></a> |
📚 <a href="https://x.com/SiriusLu1/status/1823056809223168160"><b>Twitter/X</b></a>
</p>

<p align="center">
    <b>TL;DR</b>: We propose a new prompting method - "Error Analysis Prompting" for translation evaluation. By combining Chain-of-Thoughts and Error Analysis, this technique emulates human evaluation framework MQM and produces explainable and reliable MT evaluations.
</p>

**[2025-10]** 🔗 We release the updated [codebase](./EAPrompt) for easier implementation, and release [additional results](./results) to support the community.

**[2025-09]** 📝 We have *updated the README* to better highlight the main findings.  

**[2025-01]** 🎉 Our subsequent work: **MQM-APE**: *Toward High-Quality Error Annotation Predictors with Automatic Post-Editing in LLM Translation Evaluators* has been accepted to *COLING 2025*! [📄 Paper](https://aclanthology.org/2025.coling-main.374.pdf)

**[2024-08]** 🎉 Our paper has been accepted to *ACL 2024 Findings*!  
[📄 Paper](https://aclanthology.org/2024.findings-acl.520.pdf) · [🖼️ Poster](./sources/Poster-0805.pdf) 

This repository releases the implementation of our proposed approach, the test data, queries and responses of LLM used for replicating the study.

<h2 align="center">Abstract</h2>

Generative large language models (LLMs), e.g., ChatGPT, have demonstrated remarkable proficiency across several NLP tasks, such as machine translation, text summarization. Recent research ([Kocmi and Federmann, 2023](https://arxiv.org/pdf/2302.14520.pdf)) has shown that utilizing LLMs for assessing the quality of machine translation (MT) achieves state-of-the-art performance at the system level but *performs poorly at the segment level*. To further improve the performance of LLMs on MT quality assessment, we conduct an investigation into several prompting designs, and propose a new prompting method called **Error Analysis Prompting** (**EAPrompt**) by combining Chain-of-Thoughts ([Wei et al., 2022](https://arxiv.org/pdf/2201.11903.pdf)) and Error Analysis ([Lu et al., 2022](https://aclanthology.org/2023.acl-long.324.pdf)). This technique emulates the commonly accepted human evaluation framework - Multidimensional Quality Metrics ([MQM, Freitag et al. (2021)](https://aclanthology.org/2021.tacl-1.87.pdf)) and *produces explainable and reliable MT evaluations at both the system and segment level*. Experimental Results from WMT22 metrics shared
task validate the effectiveness of EAPrompt on various LLMs, with different structures. Further analysis confirms that EAPrompt effectively distinguishes major errors from minor ones, while also sharing a similar distribution of the number of errors with MQM. These findings highlight the potential of EAPrompt as a human-like evaluator prompting technique for MT evaluation.

<h2 align="center">Error Analysis Prompting</h2>

Error Analysis Prompting (EAPrompt) is **two-step strategy** for using LLMs to assess translation quality. The model is prompted to:

(i) identify major & minor errors, and

(ii) score the translations according to the severity of these errors.

> A comparative overview between **GEMBA Prompting** ([Kocmi and Federmann, 2023](https://arxiv.org/pdf/2302.14520.pdf)) and **Error Analysis Prompting** in assessing MT quality with LLMs:

<div align="center">
    <img width="80%" alt="image" src="https://github.com/Coldmist-Lu/ErrorAnalysis_Prompt/blob/main/sources/fig1_overview.png">
</div>

For the prompting setup, in **Step 1** (identifying errors), we adopt a *one-shot prompting* strategy. For each language pair, we use the same example to guide the model’s response in a consistent format. In **Step 2** (counting errors), we apply **direct prompting**, enabling the LLMs to count the number of errors. Finally, we compute the translation score by:

<div align="center">
    <img width="40%" alt="image" src="https://github.com/Coldmist-Lu/ErrorAnalysis_Prompt/blob/main/sources/postprocess.png">
</div>

where $n_{major}$ and $n_{minor}$ denotes the number of major and minor errors respectively, while $w_{major}$ and $w_{minor}$ represent the severity weight assigned to major and minor errors. we follow [Lu et al. (2023)](https://aclanthology.org/2023.acl-long.324.pdf) to adopt a flexible scoring approach by fixing the $w_{minor} = 1$ while treating $w_{major}$ as a latent variable within EAPrompt.

<h2 align="center">Data and Evaluations</h2>

We utilize the test set from the WMT22 shared tasks ([Freitag et al., 2022](https://aclanthology.org/2022.wmt-1.2.pdf)) in English-German (En-De), English-Russian (En-Ru), and Chinese-English (Zh-En) across different domains - conversational, e-commerce, news, and social. 

The task statistics are shown as follows:

| Datasets | Language Pair | No. of Segments | No. of Systems |
|---------|---------------|----------|---------|
| WMT22   | En-De         | 2037     | 17      |
|         | En-Ru         | 2037     | 17      |
|         | Zh-En         | 1875     | 20      |
| WMT22-Subset | Zh-En | 30 | 20 |

For the three LLMs (Llama2-70b-Chat, Mixtral-8x7b-Instruct, and GPT-3.5-Turbo), we evaluate a total of 106,758 segments drawn from 54 MT systems. For GPT-4, we restrict the evaluation to Chinese–English, using 30 randomly selected segments per MT system, for a total of 600 samples ("WMT22-Subset").

<h2 align="center">EAPrompt Implementation</h2>

The main implementation is provided in [./EAPrompt](./EAPrompt/).

**🧩 Requirements**

Since EAPrompt is a prompting-based technique, it does not require any additional dependencies.
The only necessary requirement is to have chat access to a large language model (LLM) — for instance:
the OpenAI API for GPT-series models (see the demo in [./EAPrompt/inference.py](./EAPrompt/inference.py)), or the Transformers library for open-access models.

**🗂️ Prompt Types**

All prompt types used in the study are provided for replication. We adopt a structured identifier format **\{STEP\}\_\{LANG\}\_\{DEMO\}\_\{IS_REF\}** to denote each prompt type:

- **STEP** — Indicates the prompting style:  
  - `"ERROR"` for error demonstration;  
  - `"SINGLESTEP"` for combining error and count responses into a single step.

- **LANG** — Represents the language pair in uppercase (e.g., `"ENDE"` for English–German), since contextual examples differ across language pairs.

- **DEMO** — Specifies the demonstration granularity:  
  - `"DETAILED"` for full demonstration;  
  - `"ITEMIZED"` for stepwise, itemized demonstration.

- **IS_REF** — Defines whether the prompt uses reference translation:  
  - `"SRC"` for **reference-free** evaluation (source only);  
  - `"REF"` for **reference-based** evaluation.

> Note: For the counting step, we use a simple identifier `"COUNT"`. No additional keywords are required.

According to our ablation experiments, we recommend using the prompt type **ERROR\_\{LANG\}\_ITEMIZED\_\{IS_REF\}** as the default configuration, For example: `ERROR_ENDE_ITEMIZED_SRC`

**🚀 Generating Queries & Responses**

To evaluate a list of translation segments, you can directly use the method `generate_queries_batch` from the EAPrompt class to obtain the corresponding prompts.

For large-scale evaluation across multiple MT systems, we provide two example scripts for batch processing:

* [./EAPrompt/queries_generate.py](./EAPrompt/queries_generate.py) — for generating queries in batch.
* [./EAPrompt/responses_generate.py](./EAPrompt/responses_generate.py) — for generating and collecting model responses.

These scripts demonstrate the complete workflow for evaluating entire datasets efficiently.

<h2 align="center">Results and Findings</h2>

The querys and responses of the LLMs can be found in "[results](./results/)".

1. **EAPrompt significantly enhances the performance of LLMs at the system level**. Notably, prompting *GPT-3.5-Turbo* with EAPrompt outperforms all other metrics and prompting strategies, establishing a new state-of-the-art.

2. **EAPrompt surpasses GEMBA in 8 out of 9 test scenarios** across various language models and language pairs at the segment level.

3. **EAPrompt’s strong performance remain consistent even in reference-less settings**, highlighting its suitability for quality estimation tasks.

   > Performance of metrics using pairwise accuracy (%) at the system level and pairwise accuracy with tie calibration (%) at the segment level:

<div align="center">
    <img width="80%" alt="image" src="https://github.com/Coldmist-Lu/ErrorAnalysis_Prompt/blob/main/sources/main_results.png">
</div>

4. When designing prompts, we recommend the EAPrompt variant featuring a **2-step separated prompting approach and itemized error demonstrations**.

    > Performance comparison with variants of prompts for EAPrompt.

<div align="center">
    <img width="80%" alt="image" src="https://github.com/Coldmist-Lu/ErrorAnalysis_Prompt/blob/main/sources/prompt_variants.png">
</div>


5. EAPrompt adeptly distinguishes major errors from minor ones, closely **aligning its error distribution with MQM**.

   > Distribution of identified error counts across LLMs and human evaluation:

<div align="center">
    <img width="80%" alt="image" src="https://github.com/Coldmist-Lu/ErrorAnalysis_Prompt/blob/main/sources/error_dist.png">
</div>

6. We provide an alternate approach of counting errors by leveraging **Regular Expressions, further optimizing the inference costs**.

Please refer to our [arXiv preprint](https://arxiv.org/pdf/2303.13809.pdf) or [ACL Paper](https://aclanthology.org/2024.findings-acl.520.pdf) for more details.

<h2 align="center">Citation</h2>
If you find this work helpful, please consider citing as follows:  

```ruby
@article{Lu2023EAPrompt,
  title={Error Analysis Prompting Enables Human-Like Translation Evaluation in Large Language Models},
  author={Lu, Qingyu and Qiu, Baopu and Ding, Liang and Zhang, Kanjian and Kocmi, Tom and Tao, Dacheng},
  journal={arXiv preprint},
  url={https://arxiv.org/pdf/2303.13809.pdf},
  year={2023}
}
```

