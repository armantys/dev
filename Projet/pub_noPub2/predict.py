import firebase_admin
from firebase_admin import credentials
from connexion_firebase import initialize_firestore, initialize_storage
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
            u'resultats': u'mappage'
        },
        u'moyenne_no_pub': mean_no_pub,
        u'moyenne_pub': mean_pub,
        u'referance_salve_storage': reference_salve_storage,
        u'version_acquisition': db.collection(u'BDD_pub_nopub').document(u'acquisition').id,
        u'version_application': db.collection(u'BDD_pub_nopub').document(u'application').id,
        u'version_model_IA': db.collection(u'BDD_pub_nopub').document(u'model_IA').id,
        u'timestamp': timestamp
    })
# Utiliser initialize_storage() où vous en avez besoin dans le code