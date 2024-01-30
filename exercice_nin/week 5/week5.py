import spacy

nlp = spacy.load("en_core_web_sm")

import json
# https://www.kaggle.com/datasets/finalepoch/medical-ner
with open('Medical_NER.json', 'r') as f:
    data = json.load(f)


    data['examples'][0].keys()
    data['examples'][0]['content']
    data['examples'][0]['annotations'][0]

# Initialize an empty list to store the training data
training_data = []

# Iterate over each example in the provided data
for example in data['examples']:
    # Create a temporary dictionary to hold the text and entities for each example
    temp_dict = {
        'text': example['content'],  # Store the text of the example
        'entities': []  # Initialize an empty list to store entities
    }

    # Iterate over each annotation in the current example
    for annotation in example['annotations']:
        # Extract the start and end positions of the entity, and its label
        start = annotation['start']
        end = annotation['end']
        label = annotation['tag_name'].upper()  # Convert label to uppercase

        # Append the entity information as a tuple to the entities list
        temp_dict['entities'].append((start, end, label))

    # Add the prepared dictionary to the training data list
    training_data.append(temp_dict)

# Print the first entry of the formatted training data to verify the structure
print(training_data[0])

training_data[1]['entities']

# Import necessary libraries
from spacy.tokens import DocBin  # For efficient binary serialization of Doc objects
from tqdm import tqdm  # For displaying progress bars during long-running operations

# Load a new blank spaCy model for the English language
nlp = spacy.blank("en")

# Initialize a DocBin object
# DocBin is used for efficient binary serialization of spaCy's Doc objects
# It's particularly useful for creating training data for spaCy models
doc_bin = DocBin()

# Import necessary functions from spaCy
from spacy.util import filter_spans
from tqdm import tqdm

# Initialize the spaCy model
nlp = spacy.blank("en") # Create a blank English model

# Initialize the DocBin object for efficient storage of Doc objects
doc_bin = DocBin()

# Process each training example
for training_example in tqdm(training_data):
    # Extract text and entity labels from the training example
    text = training_example['text']
    labels = training_example['entities']

    # Create a Doc object from the text without running the full pipeline
    doc = nlp.make_doc(text)

    # Initialize an empty list to store entity spans
    ents = []

    # Iterate over the entities in the training example
    for start, end, label in labels:
        # Create a span for each entity
        span = doc.char_span(start, end, label=label, alignment_mode="contract")

        # If the span is valid, add it to the list of entities
        if span is None:
            print("Skipping entity")
        else:
            ents.append(span)

    # Filter overlapping spans to ensure each token is part of at most one entity
    filtered_ents = filter_spans(ents)

    # Assign the filtered entities to the document
    doc.ents = filtered_ents

    # Add the processed document to the DocBin
    doc_bin.add(doc)

# Save the DocBin with the processed documents to disk
doc_bin.to_disk("train.spacy")



