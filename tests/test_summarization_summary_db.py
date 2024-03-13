"""Unit test for summarization/summary_db.py"""

import pytest
from summarization.summary_db import SummaryDB
from datetime import datetime
from redis import Redis


def test_summary_db_store_summary():
    """Test the store_summary function."""
    summary_db = SummaryDB()
    url = "https://www.bleepingcomputer.com/news/security/russian-apt29-hackers-stealthy-malware-undetected-for-years/"
    summary = "A summary of the article"
    score = 0.8
    human_summary = "A human generated summary of the article"
    evaluator_reasoning = "The AI summary is good because it captures the main points of the article."
    date = datetime.today()
    assert summary_db.store_summary(url, summary, score, human_summary, evaluator_reasoning, date) is True