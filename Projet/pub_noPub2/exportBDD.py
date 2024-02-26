import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json

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

print(data)

print("Exportation des données terminée avec succès !")