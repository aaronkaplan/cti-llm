import re

def find_substring_positions_spacy_format(text, substrings_with_labels):
    # Initialize an empty list to hold all the entities
    entities = []
    
    # Iterate over the category and substrings in the input
    for label, substrings in substrings_with_labels.items():
        # Create a regex pattern for each category
        pattern = '|'.join(re.escape(substring) for substring in substrings)
        
        # Use re.finditer to find all occurrences of the substrings
        matches = re.finditer(pattern, text)
        
        # Add found entities with their start, end positions, and the category label
        for match in matches:
            entities.append((match.start(), match.end(), label))
    
    # Sort entities by their start position
    entities.sort(key=lambda x: x[0])
    
    # Wrap in spaCy's expected training data format
    training_data = (text, {"entities": entities})
    
    return training_data

# Example usage
text = "NY is a city, LA is another, and something happened in March 2023."
substrings_with_labels = {"LOC": ["NY", "LA"], "DATE": ["March 2023"]}
spacy_training_data = find_substring_positions_spacy_format(text, substrings_with_labels)

print(spacy_training_data)
