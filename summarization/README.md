# Summarization use-case

Summarization of CTI texts is a typical use-case for CTI teams: creating threat landscape reports, quarterly or monthly reports etc. all require us to summarize relevant information while highlighting specific things which are relevant for the organization.
While the latter will probably still for some time need human editing and corrections, the former - pure summarization of vast amounts of CTI reports, blog posts and bulletins - is a use-case where NLP / AI can shine.
Summarization can usually be done in an automatic fashion with mere human oversight.

# How to evaluate your CTI report summarization model?

If you plan to create your own CTI report summarization AI model (or fine tune an existing one), or if you merely want to compare existing models, you will naturally arrive at the problem of how to compare the quality of summarizations.
And this is anything but trivial. After all, one summarization might be written in a different style, with different words and differently structured from another one, but both might be equally "good".

## Existing metrics for comparing summaries

Here, we follow [Human-like Summarization Evaluation with ChatGPT](https://arxiv.org/pdf/2304.02554.pdf), Mingqi Gao et. al.
By following their paper, we attempt to create an LLM summarization evaluator via GPT-3.5/GPT-4. 

The paper nicely states the problem this way:
> Evaluating text summarization, like other text generation tasks, is a challenging problem. While human evaluation is considered the gold standard, it is expensive and time-consuming. As a result, *automatic evaluation metrics* play a crucial role. 
> 

But first, let's talk about these existing *automatic evaluation metrics* to compare summaries.
(Also, [this blog]() post does an excellent job at explaining the existing metrics)

### Automatic evaluation metrics
#### ROUGE (Lin, 2004)
Link: https://aclanthology.org/W04-1013.pdf

Recall-Oriented Understudy for Gisting Evaluation (ROUGE) is a set of simple methods for automatically calculating the quality of a summarization *in comparison to a reference summary* by measuring the overlapping units (n-grams, word sequences, word pairs).

The obvious downside to ROUGE is that it does not compare *semantics* in summaries. 

#### BLEU

#### METEOR

#### BERTScore

#### BERTScore

#### FactCC and  DAE

### Human/manual evaluation metrics

#### Likert scale scoring

#### Pairwise comparison

#### Pyramid

#### Binary factuality evaluation

#### Quiz
(Ben Strickson)

@Ben please add a one paragraph description 

## Comparing existing methods

(tables below taken from https://github.com/aaronkaplan/cti-llm/blob/main/summarization)
### Metric summary

![Method summary table](https://miro.medium.com/v2/resize:fit:875/1*jz4IUkjnuNfvA-0s4rSD9g.png)

### Metric usage by use case

![Metric usage by use case table](https://miro.medium.com/v2/resize:fit:875/1*cPTpGu8D9MuSIr_2We1eVQ.png)
