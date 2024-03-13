""" Class using langchain as an abstraction layer to interface with multiple LLM
models.  The class provides methods to summarize, generate, complete, classify,
search, chat, question, answer, and summarize files using the language model.
The class uses the langchain_community package to interface with the language
model.  """

import os

from typing import List

from pprint import pprint

from langchain import hub
# from langchain.schema.output_parser import StrOutputParser
from langchain_core.output_parsers import JsonOutputParser
# for caching
from langchain.globals import set_llm_cache
from langchain.cache import SQLiteCache
# for LLM models
from langchain_openai import ChatOpenAI
from langchain_openai import AzureChatOpenAI 
from langchain_anthropic import ChatAnthropic
# And finally document loaders
from langchain_community.document_loaders import PyPDFLoader

from common.web import fetch_html_from_urls_via_langchain
from common.logger import logger

from summarization.summary_db import SummaryDB


class Summarizer:
    """ Class using language model to summarize text. """
    temperature = 0.2
    model = ""

    def __init__(self, llm_provider: str = "openai"):
        """ Initialize the Summarizer class. """
        set_llm_cache(SQLiteCache(database_path=".langchain.db"))


        self.llm_provider = llm_provider
        if llm_provider == "openai":
            self.model = "gpt-4-0125-preview"
            self.api_key = os.getenv("OPENAI_API_KEY")
        elif llm_provider == "anthropic":
            self.model = "claude-3-sonnet-20240229"
            self.model = "claude-3-opus-20240229"
            self.api_key = os.getenv("ANTHROPIC_API_KEY")
        elif llm_provider == "azure":
            self.model = os.getenv("ENGINE")
            self.api_key = os.getenv("OPENAI_API_KEY")
            self.api_version = os.getenv("OPENAI_API_VERSION")
            self.azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
            self.api_type = os.getenv("OPENAI_API_TYPE")
        else:
            raise ValueError(f"Invalid LLM provider: {llm_provider}")
        try:
            if self.llm_provider == "openai":
                self.llm = ChatOpenAI(openai_api_key=self.api_key, model=self.model)
            elif self.llm_provider == "anthropic":
                self.llm = ChatAnthropic(temperature=self.temperature,
                                         anthropic_api_key=self.api_key,
                                         model_name=self.model)
            elif self.llm_provider == "azure":
                self.llm = AzureChatOpenAI(azure_endpoint=self.azure_endpoint,
                                       openai_api_key=self.api_key,
                                       api_version=self.api_version,
                                       temperature=0.0, max_retries=1, timeout=60)

            # see https://smith.langchain.com/hub/aaronkaplan/cti-llm
            self.prompt = hub.pull("aaronkaplan/cti-llm")
            self.output_parser =  JsonOutputParser()            # StrOutputParser()
            self.chain = self.prompt | self.llm  | self.output_parser
        except Exception as e:
            print(f"Summarizer class: Error: {e}")
            raise e

    def summarize_text(self, _text: str) -> str:
        """ Summarize the text using the language model. """
        return self.chain.invoke({"context": _text})

    def summarize_urls(self, urls: List[str]) -> List[dict]:
        """ Summarize a list of URLs using the language model.

        Args:
            urls: List of URLs to summarize.

        Returns:
           List of summaries as Dict.
        """
        results = []
        try:
            docs = fetch_html_from_urls_via_langchain(urls)
            for doc in docs:
                result = self.chain.invoke({"context": doc})
                print(120*"=")
                print(f"summarize_url: type(result): '{type(result)}'")
                print(f"summarize_urls: len(result): '{len(result)}'")
                print(120*"=")
                results.append(result)
            return results
        except Exception as e:
            print(f"Error: {e}")
            return "Error: Unable to fetch URL."

    def summarize_file(self, file_path: str) -> str:
        """ Summarize the file using the language model. """
        try:
            with open(file_path, "r", encoding='utf-8') as file:
                text = file.read()
                return self.chain.invoke({"context": text})
        except Exception as e:
            print(f"Error: {e}")
            return "Error: Unable to read file."

    def summarize_pdf(self, file_path: str) -> str:
        """ Summarize the PDF file using the language model. """
        try:
            loader = PyPDFLoader(file_path)
            text = loader.load()
            return self.chain.invoke({"context": text})
        except Exception as e:
            print(f"Error: {e}")
            return "Error: Unable to read PDF file."


class Orchestrator:
    """ Class to fetch and store summaries in the database. """
    def __init__(self, llm_provider: str = "openai"):
        """ Initialize the FetchAndStoreSummaries class. """
        self.summarizer = Summarizer(llm_provider=llm_provider)

    def fetch_and_store_summary(self, urls: List[str]) -> None:     # noqa:
        """ Fetch and store the summary in the database. """
        responses = self.summarizer.summarize_urls(urls)
        pprint(f"fetch_and_store_summary: summaries: '{responses}'")
        db = SummaryDB()
        for url, response in zip(urls, responses):
            print(80*"=")
            print(f"Storing summary for {url}")
            print(f"Type of response: {type(response)}")
            pprint(response)
            summary = '\n'.join(response['summary']) if 'summary' in response else ''
            print(80*"=")
            db.store_summary(url=url, summary=response['summary'],
                             llm=self.summarizer.model, llm_response=response)


if __name__ == "__main__":
    logger.info("Starting the summarizer...")

    summarizer = Summarizer(llm_provider="anthropic")
    # summarizer = Summarizer(llm_provider="azure")
    """
    import requests
    URL = "https://www.bleepingcomputer.com/news/security/russian-apt29-hackers-stealthy-malware-undetected-for-years/" # sample CTI rpoert
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    headers = {"user-agent": USER_AGENT}
    html = requests.get(URL, headers=headers, timeout=10).text
    # html = fetch_html_from_url_via_selenium(URL)
    text = get_text_from_html(html)

    # cleanup
    text = chop_empty_lines(text)

    print(f"About to summarize {URL}")
    print(f"text: {text[:800]}")
    print(summarizer.summarize_text(text))
    """
    # print(summarizer.summarize_file("sample.txt"))
    print(80*"=")
    print("About to summarize a PDF file...")
    print(summarizer.summarize_pdf("test_data/sample.pdf"))

    # print(80*"=")
    # print("About to summarize a URL...")
    # print(summarizer.summarize_url("https://www.bleepingcomputer.com/news/security/russian-apt29-hackers-stealthy-malware-undetected-for-years/"))

    print(80*"=")
    print("Fetching multiple URLs and storing the summaries in the database...")
    orchestrator = Orchestrator(llm_provider="anthropic")
    # read urls.txt , remove the newline character and store in a list
    with open("summarization/test_data/urls.txt", "r") as file:
        urls = file.readlines()
        urls = [url.strip() for url in urls]
        pprint(urls)
        orchestrator.fetch_and_store_summary(urls)
