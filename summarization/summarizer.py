""" Class using langchain as an abstraction layer to interface with multiple LLM
models.  The class provides methods to summarize, generate, complete, classify,
search, chat, question, answer, and summarize files using the language model.
The class uses the langchain_community package to interface with the language
model.  """

import os
import bs4
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser

from langchain_community.document_loaders import PyPDFLoader


class Summarizer:
    """ Class using language model to summarize text. """

    def __init__(self):
        """ Initialize the Summarizer class. """
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = "gpt-4-0125-preview"

        try:
            self.llm = ChatOpenAI(openai_api_key=self.api_key, model=self.model)
            # see https://smith.langchain.com/hub/aaronkaplan/cti-llm
            self.prompt = hub.pull("aaronkaplan/cti-llm")
            self.output_parser = StrOutputParser()
            self.chain = self.prompt | self.llm   # | self.output_parser
        except Exception as e:
            print(f"Error: {e}")
            raise e

    def summarize_text(self, _text: str) -> str:
        """ Summarize the text using the language model. """
        return self.chain.invoke({"context": _text})

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


def get_text_from_html(html: str) -> str:
    """ Convert HTML to text using BeautifulSoup. """
    _soup = bs4.BeautifulSoup(html, 'html.parser')
    _text = _soup.get_text()
    return _text


def chop_empty_lines(_text: str) -> str:
    """ Remove empty lines from the text. """
    return "\n".join([line for line in _text.split("\n") if line.strip() != ""])


if __name__ == "__main__":
    summarizer = Summarizer()
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
    print(summarizer.summarize_pdf("test_data/sample.pdf"))
