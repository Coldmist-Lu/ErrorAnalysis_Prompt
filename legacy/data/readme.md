# Data Format
For zhen.csv, each instance consists of 14 items:

* **id**: the id of this instance in our testset.
* **testset_segid**: the id of the segment in this instance in our testset.
* **global_segid**: the id of the segment in this instance in original WMT20 testset.
* **source**: the source text in this instance.
* **reference**: the reference translation in this instance.
* **system**: the system name of the candidate translation in this instance.
* **translation**: the candidate translation in this instance.
* **mqm_avg_score**: the mqm score of the translation in this instance from human evaluation using MQM.
* **score_textdavinci003_standard**: the score of the translation in this instance from text-davinci-003 using standard prompting.
* **score_textdavinci003_EA_zeroshot**: the score of the translation in this instance from text-davinci-003 using zero-shot error analysis prompting.
* **score_textdavinci003_EA**: the score of the translation in this instance from text-davinci-003 using in-context error analysis prompting.
* **score_ChatGPT_standard**: the score of the translation in this instance from ChatGPT using standard prompting.
* **score_ChatGPT_EA_zeroshot**: the score of the translation in this instance from ChatGPT using zero-shot error analysis prompting.
* **score_ChatGPT_EA**: the score of the translation in this instance from ChatGPT using in-context error analysis prompting.



For ende.csv, each instance consists of 10 items:

* **id**: the id of this instance in our testset.
* **testset_segid**: the id of the segment in this instance in our testset.
* **global_segid**: the id of the segment in this instance in original WMT20 testset.
* **source**: the source text in this instance.
* **reference**: the reference translation in this instance.
* **system**: the system name of the candidate translation in this instance.
* **translation**: the candidate translation in this instance.
* **mqm_avg_score**: the mqm score of the translation in this instance from human evaluation using MQM.
* **score_textdavinci003_EA**: the score of the translation in this instance from text-davinci-003 using in-context error analysis prompting.
* **score_ChatGPT_EA**: the score of the translation in this instance from ChatGPT using in-context error analysis prompting.
