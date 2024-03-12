"""Classes for working with the summary database.

The summary database is a redis eatabase that stores the summaries for CTI reports.
It can store summaries for text, URLs, files, and PDFs.

The DB contains the following information:
- URL or reference to the original document
- AI generated summary of the document
- Date of the summary
- (optional) human generated summary of the same document
- score of the AI summary: floating point number between 0 and 1. 0 = bad, 1 = good
- human evaluators' reasoning why the AI summary is good or bad (optional)

The database is used to store the summaries and to retrieve them for further processing.
We use pythons' redis package to interface with the database.

"""

from datetime import datetime
from typing import List, Union

from redis import Redis


class SummaryDB:
    """Class for working with the summary database."""

    def __init__(self):
        """Initialize the SummaryDB class."""

        self.db = Redis(host="localhost", port=6379, db=0)

    def store_summary(self, url: str, summary: str, score: float, human_summary: str = None,
                        evaluator_reasoning: str = None,  date: datetime = datetime.today()) -> bool:
            """Store a summary in the database.
    
            Args:
                url: URL or reference to the original document
                summary: AI generated summary of the document
                date: Date of the summary
                score: score of the AI summary: floating point number between 0 and 1. 0 = bad, 1 = good
                human_summary: (optional) human generated summary of the same document
                evaluator_reasoning: human evaluators' reasoning why the AI summary is good or bad (optional)
            Returns:
                bool: True if the summary was stored successfully, False otherwise
            """
            summary_data = {
                "url": url,
                "summary": summary,
                "date": date,
                "score": score,
                "human_summary": human_summary,
                "evaluator_reasoning": evaluator_reasoning
            }
            self.db.hmset(url, summary_data)
        
    def get_summary(self, url: str) -> Union[None, dict]:
        """Get a summary from the database, given the url"""
        summary = self.db.hgetall(url)
        if summary:
            return summary
        else:
            return None

    def get_summary_by_score(self, score: float) -> List[dict]:
        """Get summaries from the database, given the score"""
        summaries = []
        for key in self.db.keys():
            summary = self.db.hgetall(key)
            if summary["score"] >= score:
                summaries.append(summary)
        return summaries

    def get_all_summaries(self) -> List[dict]:
        """Get all summaries from the database."""
        all_summaries = []
        for key in self.db.keys():
            summary = self.db.hgetall(key)
            all_summaries.append(summary)
        return all_summaries
    

