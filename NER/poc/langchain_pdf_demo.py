from langchain_community.document_loaders import PyPDFLoader
from NER import cyner
import glob
import sqlalchemy as db
from sqlalchemy.dialects.postgresql import JSONB

engine = db.create_engine('sqlite:///ner_test_benchmark.sqlite')
connection = engine.connect()
metadata = db.MetaData()
table= db.Table('Student', metadata,
              db.Column('Id', db.Integer(),primary_key=True),
              db.Column('file_name', db.String(255), nullable=False),
              db.Column('ner_heuristics', db.JSON(), default="Math"),
              )

metadata.create_all(engine)
# use only heuristics
model_regex = cyner.CyNER(transformer_model=None,use_heuristic=True,flair_model=None,priority="H")

for pdf_report in glob.glob("../../datasets/*.pdf"):
    print(pdf_report)
    loader = PyPDFLoader(pdf_report)
    pages = loader.load_and_split()

    for document in pages:
        # this is a document
        print(f"Parsing page {document.metadata['page']}")

        entities = model_regex.get_entities(document.page_content)
        print(f"Found {len(entities)} entities")

    # now load the ground truth and see what was found!
    # TODO: load the stix file...

