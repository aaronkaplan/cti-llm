# Overview

This repo contains the code for the presentation of our talk on how to use LLMs for [CTI](https://en.wikipedia.org/wiki/Cyber_threat_intelligence) purposes.

# Use-cases for LLMs in CTI

In general, there are a couple of use-cases for LLMs in CTI. 
The most important use cases are:

1) *UC 1*: [Summarization](summarization) of free text CTI 
2) *UC 2*: [NER](NER)  (Name Entity Recognition)
3) *UC 3*: Q&A  (Answering questions on CTI texts via RAG)
4) *UC 4*: TTP Tagging (extract the TTPs from the text)
5) *UC 5*: Graph relationship extraction: extract the graph of who did what with with tools against whom etc... (the "w" questions). 


Please note that UC 5 can help the other use-cases. If you have the graph of the relationships in a texth, then answering questions (UC 3) becomes easier.

Each use-case has its own subdirectory, please go to the individual subdirs and check their README files.


# Dataset attribution

The STIX reports are pulled from the following sources:
* Palo Alto UNIT42 [github](https://github.com/pan-unit42)
* CISA advisories [website](https://www.cisa.gov/news-events/cybersecurity-advisories?)