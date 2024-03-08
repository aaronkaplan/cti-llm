"""Unit test for common/web.py"""

import unittest
from common.web import fetch_html_from_url_via_selenium


def test_fetch_html_from_url_via_selenium()):
    """Test the fetch_html_from_url_via_selenium function."""
    url = "https://www.bleepingcomputer.com/news/security/russian-apt29-hackers-stealthy-malware-undetected-for-years/"
    html = fetch_html_from_url_via_selenium(url)
    assert html is not None
    assert len(html) > 0