import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
from datetime import datetime

def convert_datetime_to_string(data):
    for key, value in data.items():
        if isinstance(value, dict):
            convert_datetime_to_string(value)
        elif isinstance(value, datetime):
            data[key] = value.strftime('%Y-%m-%d %H:%M:%S')

# Téléchargez votre fichier de clé de compte de service depuis Firebase et placez-le dans votre répertoire de travail
cred = credentials.Certificate("cred.json")
firebase_admin.initialize_app(cred)

# Initialisez une instance de Firestore
db = firestore.client()

# Définissez le nom de la collection que vous souhaitez exporter
collection_name = "BDD_pub_nopub"

# Récupérez tous les documents de la collection spécifiée
docs = db.collection(collection_name).stream()

# Initialisez un dictionnaire pour stocker les données
data = {}

# Ajoutez les données de chaque document à votre dictionnaire
for doc in docs:
    data[doc.id] = doc.to_dict()

    # Si le document a des sous-collections, récupérez également leurs données
    collections = db.collection(collection_name).document(doc.id).collections()
    for col in collections:
        col_data = {}
        col_docs = col.stream()
        for col_doc in col_docs:
            col_data[col_doc.id] = col_doc.to_dict()
        data[doc.id][col.id] = col_data

# Exportez les données au format JSON avec indentation pour la lisibilité
with open('exported_data.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)

print("Exportation des données terminée avec succès !")