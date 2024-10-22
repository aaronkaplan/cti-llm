""" This module contains functions for fetching HTML from the web and converting to text."""
from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

import nest_asyncio

from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document

import requests
import bs4


# for fetching URLs in parallel
nest_asyncio.apply()
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"


def fetch_html_from_url_via_requests(url: str, user_agent=DEFAULT_USER_AGENT) -> str:
    """ Use the requests library to fetch HTML from the URL. 
        Downloads the HTML content of a page that does not require JavaScript to render.

    Args:
        url (str): The URL of the webpage to download.
        user_agent (str, optional): The user-agent string to emulate. Defaults to a common Chrome UA.

    Returns:
        str: The HTML content of the webpage.
    """

    headers = {"user-agent": user_agent}
    html = requests.get(url, headers=headers, timeout=10).text
    return html


def get_text_from_html(html: str) -> str:
    """ Convert HTML to text using BeautifulSoup. """
    _soup = bs4.BeautifulSoup(html, 'html.parser')
    _text = _soup.get_text()
    return _text


def fetch_html_from_urls_via_langchain(urls: List[str], 
                                       user_agent=DEFAULT_USER_AGENT) -> List[Document]:
    """Use Langchain's document loaders to fetch HTML from the URL.

    Args:
        url List(str): The URLs of the webpages to download.
        user_agent (str, optional): The user-agent string to emulate. 
        Defaults to a common Chrome UA.
    
    Returns:
        a list of Document objects containing the (bs4 parsed) content of the webpage(s)
    """
    kwargs = {'verify':True, 'timeout':10, 'headers':{'user-agent': user_agent}}
    loader = WebBaseLoader(urls, verify_ssl=False, requests_per_second=20, requests_kwargs=kwargs)
    data = loader.load()
    return data


def fetch_html_from_url_via_selenium(url: str, user_agent=DEFAULT_USER_AGENT) -> str:
    """ Use Selenium to fetch HTML from the URL. 
        Downloads the HTML content of a page that requires JavaScript to render.

     Args:
        url (str): The URL of the webpage to download.
        user_agent (str, optional): The user-agent string to emulate. 
        Defaults to a common Chrome UA.

    Returns:
        str: The HTML content of the webpage.
    """

    # set up the Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument(f"user-agent={user_agent}")
    chrome_options.add_argument("--headless")  # Run in headless mode
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize the WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # fetch the URL
    try:
        driver.get(url)  # Navigate to the page
        html_content = driver.page_source  # Get the HTML content
        return html_content
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()  # Ensure the driver is quit properly
    return ""


def chop_empty_lines(_text: str) -> str:
    """ Remove empty lines from the text. """
    return "\n".join([line for line in _text.split("\n") if line.strip() != ""])
