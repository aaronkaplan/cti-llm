from langchain_community.document_loaders import PyPDFLoader
from NER import cyner
import glob

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


