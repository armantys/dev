import firebase_admin
from firebase_admin import credentials
from connexion_firebase import initialize_firestore, initialize_storage
from google.cloud import firestore
import datetime

db = initialize_firestore()
bucket = initialize_storage()
# Importer les autres modules nécessaires
from connexion_firebase import initialize_storage

def obtenir_pourcentages(predictions):
    pourcentages_pub = []
    pourcentages_nopub = []

    for prediction in predictions:
        pourcentage_pub = prediction[0][0] * 100
        pourcentage_nopub = prediction[0][1] * 100
        pourcentages_pub.append(pourcentage_pub)
        pourcentages_nopub.append(pourcentage_nopub)

    return pourcentages_pub, pourcentages_nopub


# Fonction pour récupérer la dernière version d'une collection
def get_latest_version_acquisition(collection_ref):
    acquisitions = collection_ref.order_by(u'hp_acquisition.timestamp', direction=firestore.Query.DESCENDING).limit(1).get()
    if acquisitions:
        return acquisitions[0].reference
    else:
        return None
    
# Fonction pour récupérer la dernière version d'une collection
def get_latest_version_application(collection_ref):
    application = collection_ref.order_by(u'timestamp', direction=firestore.Query.DESCENDING).limit(1).get()
    if application:
        return application[0].reference
    else:
        return None
    
# Fonction pour récupérer la dernière version d'une collection
def get_latest_version_model_IA(collection_ref):
    model_IA = collection_ref.order_by(u'timestamp', direction=firestore.Query.DESCENDING).limit(1).get()
    if model_IA:
        return model_IA[0].reference
    else:
        return None
    
# Référence à la collection "acquisition"
acquisition_collection_ref = db.collection(u'BDD_pub_nopub').document(u'acquisition').collection(u'historique')
application_collection_ref = db.collection(u'BDD_pub_nopub').document(u'application').collection(u'version')
model_IA_collection_ref = db.collection(u'BDD_pub_nopub').document(u'modele_IA').collection(u'version')
    
# Récupération de la dernière version
latest_acquisition_version = get_latest_version_acquisition(acquisition_collection_ref)
latest_application_version = get_latest_version_application(application_collection_ref)
latest_model_IA_version = get_latest_version_model_IA(model_IA_collection_ref)

def enregistrer_dans_firestore(pourcentages_pub, pourcentages_nopub, mean_pub, mean_no_pub, timestamp_str):
    # Référence au chemin d'accès de la salve dans le stockage
    reference_salve_storage = f"images_pub_no_pub/salves/{timestamp_str}"

    # Date et heure actuelles
    timestamp = datetime.datetime.now().strftime("%d %B %Y à %H:%M:%S UTC%z")

    doc_ref = db.collection(u'BDD_pub_nopub').document(u'log').collection(u'historiques').document()

    doc_ref.set({
        u'resultats': {
            u'predictions_no_pub_par_images': pourcentages_nopub,
            u'predictions_pub_par_images': pourcentages_pub,
        },
        u'moyenne_no_pub': mean_no_pub,
        u'moyenne_pub': mean_pub,
        u'referance_salve_storage': reference_salve_storage,
        u'version_acquisition': latest_acquisition_version,
        u'version_application': latest_application_version,
        u'version_model_IA': latest_model_IA_version,
        u'timestamp': timestamp
    })
# Utiliser initialize_storage() où vous en avez besoin dans le code