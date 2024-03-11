from NER import cyner

# use only heuristics
model_regex = cyner.CyNER(transformer_model=None,use_heuristic=True,flair_model=None,priority="H")


# Example text to test the matcher
text = "The server at 192.168.1.1 responded with error code 404. Contact admin@example.com for details."

entities = model_regex.get_entities(text)

for e in entities:
    print(e)
