# EAPrompt: ErrorAnalysis Prompt for MT Evaluation in LLMs

<b>Error Analysis Prompting Enables Human-Like Translation Evaluation in Large Language Models</b>. ([Arxiv](https://arxiv.org/pdf/2303.13809.pdf) · [ACL Paper](https://aclanthology.org/2024.findings-acl.520.pdf))

**TL;DR:** We propose a new prompting method - "Error Analysis Prompting" for translation evaluation. By combining Chain-of-Thoughts and Error Analysis, this technique emulates human evaluation framework MQM and produces explainable and reliable MT evaluations.

**[2025-09]** 📝 We have *updated the README* to better highlight the main findings.  
We are also revising the codebase for easier implementation, and will release additional results soon to support more reliable comparisons with subsequent works.

**[2025-01]** 🎉 Our subsequent work: **MQM-APE**: *Toward High-Quality Error Annotation Predictors with Automatic Post-Editing in LLM Translation Evaluators* has been accepted to *COLING 2025*! [📄 Paper](https://aclanthology.org/2025.coling-main.374.pdf)

**[2024-08]** 🎉 Our paper has been accepted to *ACL 2024 Findings*!  
[📄 Paper](https://aclanthology.org/2024.findings-acl.520.pdf) · [🖼️ Poster](./sources/Poster-0805.pdf) 

This repository releases the test sets, scores, and prompting approach used for replicating the study.

## Abstract

Generative large language models (LLMs), e.g., ChatGPT, have demonstrated remarkable proficiency across several NLP tasks, such as machine translation, text summarization. Recent research ([Kocmi and Federmann, 2023](https://arxiv.org/pdf/2302.14520.pdf)) has shown that utilizing LLMs for assessing the quality of machine translation (MT) achieves state-of-the-art performance at the system level but *performs poorly at the segment level*. To further improve the performance of LLMs on MT quality assessment, we conduct an investigation into several prompting designs, and propose a new prompting method called **Error Analysis Prompting** (**EAPrompt**) by combining Chain-of-Thoughts ([Wei et al., 2022](https://arxiv.org/pdf/2201.11903.pdf)) and Error Analysis ([Lu et al., 2022](https://aclanthology.org/2023.acl-long.324.pdf)). This technique emulates the commonly accepted human evaluation framework - Multidimensional Quality Metrics ([MQM, Freitag et al. (2021)](https://aclanthology.org/2021.tacl-1.87.pdf)) and *produces explainable and reliable MT evaluations at both the system and segment level*. Experimental Results from WMT22 metrics shared
task validate the effectiveness of EAPrompt on various LLMs, with different structures. Further analysis confirms that EAPrompt effectively distinguishes major errors from minor ones, while also sharing a similar distribution of the number of errors with MQM. These findings highlight the potential of EAPrompt as a human-like evaluator prompting technique for MT evaluation.

## Error Analysis Prompting

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

<!-- ! Optimal value are provided in ? -->

<!-- ! Detailed implementation can be obtained in ? -->

## Data and Evaluations

We utilize the test set from the WMT22 shared tasks ([Freitag et al., 2022](https://aclanthology.org/2022.wmt-1.2.pdf)) in English-German (En-De), English-Russian (En-Ru), and Chinese-English (Zh-En) across different domains - conversational, e-commerce, news, and social. 

The task statistics are shown as follows:

| Datasets | Language Pair | No. of Segments | No. of Systems |
|---------|---------------|----------|---------|
| WMT22   | En-De         | 2037     | 17      |
|         | En-Ru         | 2037     | 17      |
|         | Zh-En         | 1875     | 20      |
| WMT22-Subset | Zh-En | 30 | 20 |

For the three LLMs (Llama2-70b-Chat, Mixtral-8x7b-Instruct, and GPT-3.5-Turbo), we evaluate a total of 106,758 segments drawn from 54 MT systems. For GPT-4, we restrict the evaluation to Chinese–English, using 30 randomly selected segments per MT system, for a total of 600 samples ("WMT22-Subset").

<!-- ! The response of the LLMs can be found in "[./data](./data/)". -->

<!-- ! The evaluation scores are available in "[./data](./data/)", with a format consistent with the metric scores in [MTME](https://github.com/google-research/mt-metrics-eval). -->

## Results and Findings

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

  <!-- > !how to do so? -->

Please refer to our [arXiv preprint](https://arxiv.org/pdf/2303.13809.pdf) or [ACL Paper](https://aclanthology.org/2024.findings-acl.520.pdf) for more details.

## Citation
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

