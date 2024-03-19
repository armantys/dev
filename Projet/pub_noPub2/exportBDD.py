import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from connexion_firebase import initialize_firestore
import json
from datetime import datetime

def custom_json_serializer(obj):
    """
    Fonction pour sérialiser les objets datetime en chaînes de caractères
    et convertir les DocumentReference en leur ID.
    """
    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S.%f')
    elif isinstance(obj, firestore.DocumentReference):
        return obj.id  # Convertir DocumentReference en ID du document référencé
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')

def export_collection(collection_ref, data):
    """
    Fonction récursive pour exporter une collection et ses sous-collections.
    """
    docs = collection_ref.stream()
    for doc in docs:
        data[doc.id] = doc.to_dict()
        subcollections = doc.reference.collections()
        for subcollection in subcollections:
            data[doc.id][subcollection.id] = {}
            export_collection(subcollection, data[doc.id][subcollection.id])

# Initialisez Firestore
db = initialize_firestore()

# Récupérez une référence à la racine de la base de données
root_ref = db.collection('BDD_pub_nopub')

# Initialisez un dictionnaire pour stocker les données exportées
exported_data = {}

# Exportez la racine et ses sous-collections récursivement
export_collection(root_ref, exported_data)

# Écrivez les données dans un fichier JSON en utilisant la sérialisation personnalisée
with open("exported_data.json", "w") as json_file:
    json.dump(exported_data, json_file, indent=4, default=custom_json_serializer)

print("Export completed successfully!")