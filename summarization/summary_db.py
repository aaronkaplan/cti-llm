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
We use postgresql as the database for this project.

"""

from datetime import datetime
from typing import List, Union

import psycopg
from psycopg.types.json import Jsonb



DSN="dbname=summarydb user=aaron"
CREATE_SQL = """
    CREATE TABLE summary (id SERIAL PRIMARY KEY, 
        url TEXT, 
        summary TEXT, 
        date DATE, 
        score FLOAT, 
        human_summary TEXT, 
        evaluator_reasoning TEXT);
"""


# Helper function to create the database in postgresql.


def create_summary_db() -> bool:
    """Create the summary database in postgresql."""
    try:
        conn = psycopg.connect(DSN)
        # Open a cursor to perform database operations
        with conn.cursor() as cur:
            # Execute a command: this creates a new table
            cur.execute(CREATE_SQL)
            print("Summary database created successfully")
            conn.commit()
        return True
    except Exception as e:
        print(f"Error creating summary database: {e}")
        return False


def check_if_summary_db_exists() -> bool:
    """Check if the summary database exists in postgresql."""
    try:
        db = psycopg.connect(DSN)
        cursor = db.cursor()
        cursor.execute("SELECT * FROM information_schema.tables WHERE table_name = 'summary'")
        if cursor.rowcount == 0:
            return False
        print("Summary database exists")
        return True
    except Exception as e:
        print(f"Error checking if summary database exists: {e}")
        return False
    
def delete_summary_table():
    """Drop the summary table from the database."""
    try:
        db = psycopg.connect(DSN)
        cursor = db.cursor()
        cursor.execute("DELETE FROM summary")
        db.commit()
        print("Summary table emptied successfully")
    except Exception as e:
        print(f"Error flushing summary table: {e}")


class SummaryDB:
    """Class for working with the summary database."""

    def __init__(self):
        """Initialize the SummaryDB class."""

        try:
            self.db = psycopg.connect(DSN)
        except Exception as e:
            print(f"Error connecting to summary database: {e}")
            raise e

    def store_summary(self, url: str, summary: str, score: float = None, human_summary: str = None,
                      evaluator_reasoning: str = None, date: datetime = datetime.today(),
                      llm: str = None, llm_response: dict = None) -> bool:
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
            "date": str(date),
            "score": score,
            "human_summary": human_summary,
            "evaluator_reasoning": evaluator_reasoning,
            "llm": llm,
            "llm_response": Jsonb(llm_response) if llm_response else None
        }
        try:
            cur = self.db.cursor()
            cur.execute("INSERT INTO summary (url, summary, date, score, human_summary, evaluator_reasoning, llm, llm_response) VALUES (%(url)s, %(summary)s, %(date)s, %(score)s, %(human_summary)s, %(evaluator_reasoning)s, %(llm)s, %(llm_response)s)", summary_data)
            self.db.commit()
        except Exception as e:
            print(f"Error storing summary: {e}")
            return False
        return True

    def get_summary(self, url: str) -> Union[None, dict]:
        """Get a summary from the database, given the url"""
        cur = self.db.cursor()
        results = cur.execute("SELECT * FROM summary WHERE url = %(url)s", {"url": url})
        if cur.rowcount == 0:
            return None
        else:
            summary = cur.fetchone()
            return summary

    def get_summary_by_score(self, score: float) -> List[dict]:
        """Get summaries from the database, given the score"""
        summaries = []
        cur = self.db.cursor()
        cur.execute("SELECT * FROM summary WHERE score >= %(score)s", {"score": score})
        for summary in cur.fetchall():
            summaries.append(summary)
        return summaries

    def get_all_summaries(self) -> List[dict]:
        """Get all summaries from the database."""
        all_summaries = []
        cur = self.db.cursor()
        cur.execute("SELECT * FROM summary")
        all_summaries = cur.fetchall()
        return all_summaries


if __name__ == "__main__":
    if not check_if_summary_db_exists():
        create_summary_db()
    summary_db = SummaryDB()
    summary_db.store_summary("https://www.bleepingcomputer.com/news/security/russian-apt29-hackers-stealthy-malware-undetected-for-years/",
                             "A summary of the article", 0.8, "A human generated summary of the article", "The AI summary is good because it captures the main points of the article.")
    print(summary_db.get_summary("https://www.bleepingcomputer.com/news/security/russian-apt29-hackers-stealthy-malware-undetected-for-years/"))

    print(40*"=" + " Get all summaries (score > 0.8) " + 40*"=")
    print(summary_db.get_summary_by_score(0.8))
    print(40*"=" + " Get all summaries " + 40*"=")
    print(summary_db.get_all_summaries())
    print(40*"=" + " Drop table" + 40*"=")
    delete_summary_table()

    print("Done")
