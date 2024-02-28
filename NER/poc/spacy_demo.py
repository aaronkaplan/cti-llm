import spacy
from spacy.matcher import Matcher
import re

# Load spaCy model
nlp = spacy.load("en_core_web_sm")  # Ensure you have the model installed

# Initialize the Matcher
matcher = Matcher(nlp.vocab)

# Define patterns
patterns = {
    "IPV4_ADDRESS": [{"TEXT": {"REGEX": r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"}}],
    # IPv6 addresses are complex and may need a more sophisticated pattern
    "DOMAIN": [{"TEXT": {"REGEX": r"([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}"}}],
    "URL": [{"TEXT": {"REGEX": r"(https?://)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*/?"}}],
    "EMAIL_ADDRESS": [{"TEXT": {"REGEX": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"}}],
    "MD5_HASH": [{"TEXT": {"REGEX": r"\b[a-f0-9]{32}\b"}}],
    "SHA1_HASH": [{"TEXT": {"REGEX": r"\b[a-f0-9]{40}\b"}}],
    # SHA256, FILE_PATH, and others can be added similarly
    "CVE_ID": [{"TEXT": {"REGEX": r"CVE-\d{4}-\d{4,}"}}],
    # This matches to often, could be a problem later:
    "PORT_NUMBER": [{"TEXT": {"REGEX": r"\b\d{1,5}\b"}}],
    # REGISTRY_KEY pattern might need customization based on the specifics
}

# Add patterns to the matcher
for tag_name, pattern in patterns.items():
    matcher.add(tag_name, [pattern])

# Example text to test the matcher
text = "The server at 192.168.1.1 responded with error code 404. Contact admin@example.com for details."

# Process the text
doc = nlp(text)

# Apply the matcher
matches = matcher(doc)

# Display results
for match_id, start, end in matches:
    string_id = nlp.vocab.strings[match_id]  # Get string representation
    span = doc[start:end]  # The matched span
    print(f"{string_id}: {span.text}")
