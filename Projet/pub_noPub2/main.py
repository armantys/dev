import datetime
import os
import time
import connexion_firebase
from snapshot import enregistrer_snapshot
from predict import obtenir_pourcentages
import cv2
import tensorflow as tf
from train import predict_images, load_or_train_model

latest_acquisition = connexion_firebase.get_latest_acquisition()
latest_application = connexion_firebase.get_latest_application()
latest_model_IA = connexion_firebase.get_latest_model_IA()
date_du_jour = datetime.date.today().strftime("%Y-%m-%d")

print("Dernière acquisition:", latest_acquisition)
print("Dernière application:", latest_application)
print("Dernier modèle IA:", latest_model_IA)

snapshot_folder = os.path.join(os.getcwd(), 'snapshot')

# Assurez-vous que le répertoire datedujour existe. S'il n'existe pas, créez-le.
if not os.path.exists(snapshot_folder):
    os.makedirs(snapshot_folder)

filename_prefix = os.path.join(snapshot_folder, 'snapshot')

def main():
    global snapshot_folder
    model = load_or_train_model()

    if model:
        latest_acquisition = connexion_firebase.get_latest_acquisition()

        if latest_acquisition:
            duree_salve, nb_images = latest_acquisition

            adresse_ip = '192.168.20.37'
            port = 88
            nom_utilisateur = 'dev_IA_P3'
            mot_de_passe = 'dev_IA_P3'

            # Appeler la fonction pour capturer et enregistrer les images
            images, predictions = enregistrer_snapshot(adresse_ip, port, nom_utilisateur, mot_de_passe, duree_salve, nb_images)

            # Effectuer des opérations sur les images, telles que la prédiction
            print("Prédictions:", predictions)

            # Appel de la fonction pour obtenir les pourcentages
            pourcentages_pub, pourcentages_nopub = obtenir_pourcentages(predictions)

            pourcentages_pub_list = []
            pourcentages_nopub_list = []

            for i, (pourcentage_pub, pourcentage_nopub) in enumerate(zip(pourcentages_pub, pourcentages_nopub), 1):
                print(f"Pourcentage de chance que ce soit une publicité pour l'image {i}: {pourcentage_pub}")
                print(f"Pourcentage de chance que ce ne soit pas une publicité pour l'image {i}: {pourcentage_nopub}")
                pourcentages_pub_list.append(pourcentage_pub)
                pourcentages_nopub_list.append(pourcentage_nopub)

            print("Pourcentages de chance que ce soit une publicité :", pourcentages_pub_list)
            print("Pourcentages de chance que ce ne soit pas une publicité :", pourcentages_nopub_list)

        else:
            print("Aucune acquisition trouvée dans la base de données.")
    else:
        print("Impossible de continuer car le modèle n'a pas été chargé avec succès.")


if __name__ == "__main__":
    main()
