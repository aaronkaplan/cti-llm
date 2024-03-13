"""Unit test for common/web.py"""

import pytest
from common.web import get_text_from_html, fetch_html_from_url_via_requests,\
        fetch_html_from_urls_via_langchain, chop_empty_lines



# test cases for fetch_html_from_url_via_selenium
#def test_fetch_html_from_url_via_selenium():
#    """Test the fetch_html_from_url_via_selenium function."""
#    url = "https://www.bleepingcomputer.com/news/security/russian-apt29-hackers-stealthy-malware-undetected-for-years/"
#    html = fetch_html_from_url_via_selenium(url)
#    assert html is not None
#    assert len(html) > 0

# Test cases for get_text_from_html
def test_get_text_from_html_valid_input():
    """ Test case with valid HTML input"""
    html = '<html><body><h1>Hello</h1><p>World!</p></body></html>'
    expected_output = 'HelloWorld!'
    assert get_text_from_html(html) == expected_output

def test_get_text_from_html_empty_input():
    """ Test case with empty HTML input """
    html = ''
    expected_output = ''
    assert get_text_from_html(html) == expected_output

def test_get_text_from_html_invalid_html():
    """ Test case with invalid HTML input"""
    html = '<html><body><h1>Hello</h1><p>World!</p></body>'  # Missing closing </html> tag
    expected_output = 'HelloWorld!'
    assert get_text_from_html(html) == expected_output
    # only if strict mode is on
    # with pytest.raises(bs4.FeatureNotFound):
    #    get_text_from_html(html)

def test_get_text_from_html_non_string_input():
    """ Test case with non-string input"""
    html = 123
    with pytest.raises(TypeError):
        get_text_from_html(html)

def test_get_text_from_html_none_input():
    """ Test case with None input"""
    html = None
    with pytest.raises(TypeError):
        get_text_from_html(html)


# Test cases for fetch_html_from_url_via_requests
def test_fetch_html_from_url_via_requests(mocker):
    """ Mock the requests.get function"""
    mock_get = mocker.patch('requests.get')
    mock_response = mocker.Mock()
    mock_response.text = '<html><body>Test HTML</body></html>'
    mock_get.return_value = mock_response

    # Define the test URL and user agent
    test_url = 'https://example.com'
    test_user_agent = 'TestUserAgent'

    # Call the function with the test URL and user agent
    html = fetch_html_from_url_via_requests(test_url, test_user_agent)

    # Assert that the requests.get function was called with the correct arguments
    mock_get.assert_called_once_with(test_url, headers={'user-agent': test_user_agent}, timeout=10)

    # Assert that the function returns the expected HTML
    assert html == '<html><body>Test HTML</body></html>'


# Test cases for fetch_html_from_url_via_langchain
def test_fetch_html_from_url_via_langchain():
    """ Mock the WebBaseLoader.load function"""

    # Define the test URL and user agent
    test_url = 'https://example.com'
    _test_user_agent = 'TestUserAgent'

    # Call the function with the test URL and user agent
    docs = fetch_html_from_urls_via_langchain(test_url)
    text = str(docs)


    # Assert that the function returns the expected HTML
    assert 'Example Domain' in text

# Test cases for chop_empty_lines
def test_chop_empty_lines_valid_input():
    """ Test case with valid input"""
    input_text = 'Hello\n\nWorld!\n'
    expected_output = 'Hello\nWorld!'

    assert chop_empty_lines(input_text) == expected_output
