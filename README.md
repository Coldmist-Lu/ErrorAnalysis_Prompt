# ErrorAnalysis Prompt for MT Evaluation in ChatGPT

<b>Error Analysis Prompting Enables Human-Like Translation Evaluation in Large Language Models: A Case Study on ChatGPT</b>. ([Full report](https://arxiv.org/pdf/2303.13809.pdf))

This repository releases the testsets and the scores evaluated by text-davinci-003 and [ChatGPT](https://chat.openai.com/chat),  for the replication of the study.

## Abstract

Generative large language models (LLMs), e.g., ChatGPT, have demonstrated remarkable proficiency across several NLP tasks such as machine translation, question answering, text summarization, and natural language understanding. Recent research ([Kocmi and Federmann, 2023](https://arxiv.org/pdf/2302.14520.pdf)) has shown that utilizing ChatGPT for assessing the quality of machine translation (MT) achieves state-of-the-art performance at the system level but *performs poorly at the segment level*. To further improve the performance of LLMs on MT quality assessment, we conducted an investigation into several prompting methods. Our results indicate that by combining Chain-of-Thoughts ([Wei et al., 2022](https://arxiv.org/pdf/2201.11903.pdf)) and Error Analysis ([Lu et al., 2022](https://arxiv.org/pdf/2212.10179.pdf)), a new prompting method called **Error Analysis Prompting**, LLMs like ChatGPT can *generate human-like MT evaluations at both the system and segment level*. Additionally, we discovered some limitations of ChatGPT as an MT evaluator, such as unstable scoring and biases when provided with multiple translations in a single query. Our findings aim to provide a preliminary experience for appropriately evaluating translation quality on ChatGPT while offering a variety of tricks in designing prompts for in-context learning. 
We anticipate that this report will shed new light on advancing the field of translation evaluation with LLMs by enhancing both accuracy and reliability of metrics.

## Data and Evaluations

For each language pair, we divide the segments from WMT20 testset into four groups based on the number of tokens they contain (15-24, 25-34, 35-44, 45-54). We randomly sample 10 segments from each group and form a new dataset containing 40 segments. We utilize Multidimentional Quality Metric (MQM) as human evaluation. The test data and its corresponding evaluation scores can be obtained in "[./data](./data/)".

The task statistics are shown as follows:

<div align="center">
    <img width="80%" alt="image" src="https://github.com/Coldmist-Lu/ErrorAnalysis_Prompt/blob/main/sources/testset.png">
</div>

## An overview of Error Analysis Prompting

An overview of our error analysis prompting. Detailed prompt contexts can be obtained in "[./prompts](./prompts/)".

<div align="center">
    <img width="80%" alt="image" src="https://github.com/Coldmist-Lu/ErrorAnalysis_Prompt/blob/main/sources/overview.png">
</div>



## Results and Findings

1. :slightly_smiling_face: Our EA Prompting outperforms standard prompting at the segment level, achieving human-like evaluations at both the system level and segment level.

   > System & Segment level performance on our testset:

<div align="center">
    <img width="80%" alt="image" src="https://github.com/Coldmist-Lu/ErrorAnalysis_Prompt/blob/main/sources/result.png">
</div>



2. :thinking: When designing prompts, itemized responses are better than lengthy and detailed explanations of errors. Moreover, splitting the instruction into two identifying errors and scoring translation can improve evaluation stability.

   > An comparison on different prompt designs, and their prompt contexts:

<div align="center">
    <img width="85%" alt="image" src="https://github.com/Coldmist-Lu/ErrorAnalysis_Prompt/blob/main/sources/promptcompare.png">
</div>
<div align="center">
    <img width="75%" alt="image" src="https://github.com/Coldmist-Lu/ErrorAnalysis_Prompt/blob/main/sources/promptcontext.png">
</div>




3. :neutral_face: The boosted performance from EA prompting is observed in the zero-shot scenario on text-davinci-003 rather than in the few-shot scenario, which indicates that we need to adjust our settings when utilizing other GPT models.
4. :exclamation: Despite its good performance, we show that ChatGPT is NOT a stable evaluator and may score the same translation differently.

<div align="center">
    <img width="25%" alt="image" src="https://github.com/Coldmist-Lu/ErrorAnalysis_Prompt/blob/main/sources/unstable.png">
</div>

5. :exclamation: It is NOT advisable to combine multiple translations into a single query input, as ChatGPT has a preference for former translations. 

<div align="center">
    <img width="100%" alt="image" src="https://github.com/Coldmist-Lu/ErrorAnalysis_Prompt/blob/main/sources/input%20bias.png">
</div>

Please refer to our full [report](https://github.com/Coldmist-Lu/ErrorAnalysis_Prompt/blob/main/sources/report.pdf) & [arXiv preprint](https://arxiv.org/pdf/2303.13809.pdf) for more details.

## Citation
If you find this work helpful, please consider citing as follows:  

```ruby
@article{Lu2023EAPrompt,
  title={Error Analysis Prompting Enables Human-Like Translation Evaluation in Large Language Models: A Case Study on ChatGPT},
  author={Lu, Qingyu and Qiu, Baopu and Ding, Liang and Xie, Liping and Tao, Dacheng},
  journal={arXiv preprint},
  url={https://arxiv.org/pdf/2303.13809.pdf},
  year={2023}
}
```

