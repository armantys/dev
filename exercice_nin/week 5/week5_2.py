# Import necessary functions from spaCy
from spacy.util import filter_spans
from tqdm import tqdm
import spacy
from spacy.tokens import DocBin
import json  # Ajout de l'importation du module json
 
# # Load spaCy model
# nlp = spacy.blank("en")
 
# # Create a DocBin to store the processed documents
# doc_bin = DocBin()
 
# # Read the JSON data from the file
# with open("TASTEset.json", "r", encoding="utf-8") as file:
#     data = json.load(file)
 
# # Process each training example
# for training_example in tqdm(data):
#     # Extract text and entity labels from the training example
#     text = training_example[0]
#     labels = training_example[1]["entities"]
 
#     # Create a Doc object from the text without running the full pipeline
#     doc = nlp.make_doc(text)
 
#     # Initialize an empty list to store entity spans
#     ents = []
 
#     # Iterate over the entities in the training example
#     for start, end, label in labels:
#         # Create a span for each entity
#         span = doc.char_span(start, end, label=label, alignment_mode="contract")
 
#         # If the span is valid, add it to the list of entities
#         if span is None:
#             print("Skipping entity")
#         else:
#             ents.append(span)
 
#     # Filter overlapping spans to ensure each token is part of at most one entity
#     filtered_ents = filter_spans(ents)
 
#     # Assign the filtered entities to the document
#     doc.ents = filtered_ents
 
#     # Add the processed document to the DocBin
#     doc_bin.add(doc)
 
# # Save the DocBin with the processed documents to disk
# doc_bin.to_disk("train.spacy")


nlp_ner = spacy.load("model-best")

# Intitalize the colours for the NER

colors = {"QUANTITY": "#F67DE3", "FOOD": "#7DF6D9", "PHYSICAL_QUALITY":"#a6e22d", "PROCESS":"#D8D623", "UNIT":"#EE87D3"}
options = {"colors": colors}

doc = nlp_ner("""STEP 1
Mix 500g strong white flour, 2 tsp salt and a 7g sachet of fast-action yeast in a large bowl.

STEP 2
Make a well in the centre, then add 3 tbsp olive oil and 300ml water, and mix well. If the dough seems a little stiff, add another 1-2 tbsp water and mix well.

STEP 3
Tip onto a lightly floured work surface and knead for around 10 mins.

STEP 4
Once the dough is satin-smooth, place it in a lightly oiled bowl and cover with cling film. Leave to rise for 1 hour until doubled in size or place in the fridge overnight.

STEP 5
Line a baking tray with baking parchment. Knock back the dough (punch the air out and pull the dough in on itself) then gently mould the dough into a ball.

STEP 6
Place it on the baking parchment to prove for a further hour until doubled in size.

STEP 7
Heat oven to 220C/fan 200C/gas 7.

STEP 8
Dust the loaf with some extra flour and cut a cross about 6cm long into the top of the loaf with a sharp knife.

STEP 9
Bake for 25-30 mins until golden brown and the loaf sounds hollow when tapped underneath.""")

spacy.displacy.render(doc, style="ent", options= options, jupyter=True)