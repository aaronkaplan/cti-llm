# PIR Reports

This dataset contains open source CTI PDF documents and parsed outputs for use in both training (when tagged) and testing.

## Folder contents
Original PDFs are contained in the `original_pdfs` folder.

The parsed outputs are zipped up in `parsed_outputs.zip` so will need to be decompressed.

The `Generic_Intelligence_Requirements-Document_Reference.xlsx` breaks down the naming conventions of the PDFs. A description of what this means is provided in `PIR_Spreadsheet_Breakdown.mp4`.

The gathering, naming and intelligence requirements table and breakdown are the work of [Stewart Bertram](https://www.linkedin.com/in/stewartbertram/), Head of CTI at Elemendar 

## Data structure of the pickle files in `parsed_outputs.zip`

As these are pickle files, python is the obvious way to make use of these. Using Elemendar's parser the PDF contents are provided in an HTML-like structure, split in to:
1. Text - in order, broken down by sentence but those sentences are grouped in to paragraphs and potentially other tags (like headers and lists)
2. Images - background ones are ignored, and for this project I believe they can all be ignored. They are base64 encoded so can be embedded directly in to displays
3. Tables

All of the above are placed, as well as possible, in the order in which a person reading the PDF would read them. More detail on the precise structure is provided in this sample code.

```
import pickle

# example output
with open("parsed_outputs/9-d-1-0_Privacy_Affairs-Dark_Web_Price_Index.pdf.pkl", 'rb') as f:
    # extracted_from - always 'PIR_PDF' and can be ignored
    # tables - a list of lists containing the extracted tabular data (details below)
    # title - a string where we've used either metadata or our best guess from the opening text of the report title
    # created_at - can be ignored
    # blocks - how we represent the text, images, and where the tables sit (details below)
    # file_name - for easy access back to which PDF this data came from
    (extrated_from, tables, title, created_at, blocks, file_name) = pickle.load(f)

# table description
#   - first index is to get to a table; this is in order of where they are in the document
#   - second index is the row
#   - third index is the column, which then returns a strong
# example: first table, second row, second column
print(f"Table example: {tables[0][1][1]}")

# blocks description
# - this is a list of dictionaries, in order of how the text / images / tables appear within the PDF
# - tag - in this example there are only 3, but for blocks containing text there could be other html-style tags like headers or lists
#     - img - simply indicates that this is an image
#     - p - just like with html, indicates that (until you hit the next dictionary with a close_tag of 'p') the text you're getting is within a paragraph
#     - table - simply indicates that this is a table
#  - close_tag - html like, 
#  - src - for the work we're doing here you can probably ignore this, but it's binary data for the images (and where they are) within the PDF. Ignores backgrounds etc.
#  - sentence_idx - int, helps keep track of where in the document this sentence is
#  - table_idx - int, which table (within the tables list) is at this spot
#  - text - string, the most important one! All text is broken down to the sentence level, to bring paragraphs etc. together make use of tag and close_tag
# example of paragraph:

# grab a sample block that starts a paragraph
paragraph_blocks = []
start_paragraph_idx = None
for idx, block in enumerate(blocks):
    if idx > 10 and block['tag'] == "p" and block.get('close_tag') is None:
        start_paragraph_idx = idx
        paragraph_blocks.append(block)
        break

# now grab the blocks up until the paragraph closes
for idx, block in enumerate(blocks):
    if idx > start_paragraph_idx:
        if block.get('tag') is None:
            paragraph_blocks.append(block)
            if block.get('close_tag') == "p":
                break

paragraph_text = ""
for block in paragraph_blocks:
    paragraph_text += block.get("text")
    paragraph_text += ". "
print(f"Paragraph example: {paragraph_text}")
```

