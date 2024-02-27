Sumission-Text for FIRST
=========================


## Abstract
LLMs turn out to be highly practical for summarising and extracting information from unstructured Cyber Threat Intelligence (CTI) reports. However, most models were not trained specifically for understanding CTI. We will present a custom LLM, fine-tuned for CTI purposes. But of course, that only makes sense with a CTI text benchmark dataset. Creating these two systems is a challenging journey. Set-backs guaranteed. We will share our findings. Comes with batteries and MISP-integration.

## Details

Many CTI practitioners and companies experimented with LLMs for extracting information from unstructured CTI reports in the last year. Often, the dream is to automate the analyst's job to correctly identify, copy & paste TTPs, threat actors and relationships from the report and to convert it into STIX.

Alas, off-the-shelf LLMs often fail at this task (GPT-4-turbo being already pretty good at the submission time). But there is another caveat: the requirements for IT security often demand that data remains on-premise or at least in a virtual server which is fully and only under the control of the organisation's IT team. For that we need local LLMs (as opposed to cloud bases SaaS/FaaS solutions such as openai.com's API). But how to achieve good results with local LLMs ? Can we beat openai?


To address the CTI text summarisation and information extraction problem, we

1. propose an open source CTI LLM benchmark dataset which can be used to compare different LLMs and prompts
2. a fine-tuned custom CTI LLM model ("neuroCTI") and
3. evaluate it (as well as other LLMs) against the benchmark dataset and
4. finally, integrate the LLM into MISP

The model will be made freely available for local deployments.

## Takeaways

The talk will give the audience

- an overview of the problem space,
- the challenges we faced,
- a mind-set how to approach custom LLM training
- the design of the benchmark dataset,
- an understanding of the challenges of fine-tuning a local LLM and its' limits
- an understanding on how to use our local CTI LLM ("neuroCTI")
- an understanding on how to integrate CTI LLMs into your CTI workflow, particularly into MISP.
