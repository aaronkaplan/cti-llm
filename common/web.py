""" This module contains functions for fetching HTML from the web and converting to text."""

"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
"""


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import bs4


def get_text_from_html(html: str) -> str:
    """ Convert HTML to text using BeautifulSoup. """
    _soup = bs4.BeautifulSoup(html, 'html.parser')
    _text = _soup.get_text()
    return _text


def fetch_html_from_url_via_selenium(url: str) -> str:
    """ Use Selenium to fetch HTML from the URL. """

    # set up the Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # set up the Chrome service
    service = Service("chromedriver")

    # create the Chrome driver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # fetch the URL
    driver.get(url)

    # wait for the page to load
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    except TimeoutException:
        print("Timed out waiting for page to load")
        return None

    # get the HTML
    html = driver.page_source

    # close the driver
    driver.quit()

    return html
