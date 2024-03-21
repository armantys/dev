import firebase_admin 
from firebase_admin import credentials, firestore, storage

def initialize_firestore():
    try:
        app = firebase_admin.get_app()
    except ValueError:
        cred = credentials.Certificate("cred.json")
        app = firebase_admin.initialize_app(cred, {
            'storageBucket': 'pubnopub-7fc03.appspot.com'
        })
    return firestore.client(app=app)

def initialize_storage():
    try:
        app = firebase_admin.get_app()
    except ValueError:
        cred = credentials.Certificate("cred.json")
        app = firebase_admin.initialize_app(cred, {
            'storageBucket': 'pubnopub-7fc03.appspot.com'
        })
    return storage.bucket(app=app)

def get_latest_acquisition():
    db = initialize_firestore()
    bdd_ref = db.collection("BDD_pub_nopub")
    acquisition_ref = bdd_ref.document("acquisition").collection("historique")
    docs_refacquisition = acquisition_ref.order_by('hp_acquisition.timestamp', direction=firestore.Query.DESCENDING).limit(1)
    docsaquisition = docs_refacquisition.stream()
    latest_acquisition = None
    for doc in docsaquisition:
        latest_acquisition = doc.to_dict()
        duree_salves = latest_acquisition['hp_acquisition']['duree_salves']
        nb_images = latest_acquisition['hp_acquisition']['nb_images']
        # Afficher les valeurs des champs
        print("duree_salves:", duree_salves)
        print("nb_images:", nb_images)
    return duree_salves, nb_images

def get_latest_application():
    db = initialize_firestore()
    bdd_ref = db.collection("BDD_pub_nopub")
    application_ref = bdd_ref.document("application").collection("version")
    docs_refapplication = application_ref.order_by('timestamp', direction=firestore.Query.DESCENDING).limit(1)
    docsapplication = docs_refapplication.stream()
    latest_application = None
    for doc in docsapplication:
        latest_application = doc.to_dict()
    return latest_application

def get_latest_model_IA():
    db = initialize_firestore()
    bdd_ref = db.collection("BDD_pub_nopub")
    model_IA_ref = bdd_ref.document("modele_IA").collection("version")
    docs_refmodel_IA = model_IA_ref.order_by('timestamp', direction=firestore.Query.DESCENDING).limit(1)
    docs_refmodel_IA = docs_refmodel_IA.stream()
    latest_model_IA = None
    for doc in docs_refmodel_IA:
        latest_model_IA = doc.to_dict()
    return latest_model_IA