import firebase_admin 
from firebase_admin import credentials,firestore, db



cred = credentials.Certificate("cred.json")
firebase_admin.initialize_app(cred)

# Récupérer une référence à la base de données Firestore
db = firestore.client()

# Récupérer une référence à la collection "BDD_pub_nopub"
bdd_ref = db.collection("BDD_pub_nopub")

# Récupérer une référence à la sous-collection "acquisition"
acquisition_ref = bdd_ref.document("acquisition").collection("historique")
# Récupérer une référence à la sous-collection "application"
application_ref = bdd_ref.document("application").collection("version")
# Récupérer une référence à la sous-collection "Model IA"
model_IA_ref = bdd_ref.document("modele_IA").collection("version")

# Récupérer une référence à la sous-collection avec un ID aléatoire
docs_refacquisition = acquisition_ref.order_by('hp_acquisition.timestamp', direction=firestore.Query.DESCENDING).limit(1)
docs_refapplication = application_ref.order_by('timestamp', direction=firestore.Query.DESCENDING).limit(1)
docs_refmodel_IA = model_IA_ref.order_by('timestamp', direction=firestore.Query.DESCENDING).limit(1)

# Récupérer le dernier document de la sous-collection
docsaquisition = docs_refacquisition.stream()
docsapplication = docs_refapplication.stream()
docs_refmodel_IA = docs_refmodel_IA.stream()

# Vérifier s'il y a des documents à afficher
if docsaquisition:
    for doc in docsaquisition:
        print(doc.id, doc.to_dict())
        doc_dict = doc.to_dict()
        # Accéder aux valeurs des champs "duree_salves" et "nb_images" dans le mappage "hp_acquisition"
        duree_salves = doc_dict['hp_acquisition']['duree_salves']
        nb_images = doc_dict['hp_acquisition']['nb_images']
        # Afficher les valeurs des champs
        print("duree_salves:", duree_salves)
        print("nb_images:", nb_images)
else:
    print("Aucun document trouvé")

    # Vérifier s'il y a des documents à afficher
if docsapplication:
    for doc in docsapplication:
        print(doc.id, doc.to_dict())
else:
    print("Aucun document trouvé")

        # Vérifier s'il y a des documents à afficher
if docs_refmodel_IA:
    for doc in docs_refmodel_IA:
        print(doc.id, doc.to_dict())
        doc_dict = doc.to_dict()
        seuil_decision = doc_dict['seuil_decision']
        print("seuil de decision : ", seuil_decision)
else:
    print("Aucun document trouvé")