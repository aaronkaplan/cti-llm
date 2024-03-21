from langchain_community.document_loaders import PyPDFLoader

import glob
import sqlalchemy as db
from sqlalchemy.dialects.postgresql import JSONB,JSON
from sqlalchemy import Column, Integer, String, DateTime
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
import datetime as dt
class Base(DeclarativeBase):
    pass

class Report(Base):
    __tablename__ = "report"
    id = Column(Integer, primary_key=True)
    ts = Column(DateTime, default=dt.datetime.now())
    filename = Column(String)
    ner_config = Column(JSON)

engine = db.create_engine('sqlite:///ner_test_benchmark.sqlite')

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

import cyner
# use only heuristics
model_regex = cyner.CyNER(transformer_model=None,use_heuristic=True,flair_model=None,priority="H")

from sqlalchemy.orm import Session

with Session(engine) as session:
    for pdf_report in glob.glob("../../datasets/*.pdf"):
        print(pdf_report)
        loader = PyPDFLoader(pdf_report)
        pages = loader.load_and_split()

        for document in pages:
            # this is a document
            print(f"Parsing page {document.metadata['page']}")

            entities = model_regex.get_entities(document.page_content)
            print(f"Found {len(entities)} entities")

            r = Report(filename=pdf_report,ner_config={})

            session.add(r)
    session.commit()

    # see how many reports
    result = session.query(Report).count()
    print("Total reports %d" % result)


