import datetime
import os
import time
import connexion_firebase
from google.cloud import storage
from Récupérer_les_images_pour_le_projet_PubNo_Pub.snapshot import enregistrer_snapshot,obtenir_timestamp_str
from predict import obtenir_pourcentages, enregistrer_dans_firestore
import cv2
import tensorflow as tf
import numpy as np
from train import load_or_train_model


while True:
    latest_acquisition = connexion_firebase.get_latest_acquisition()
    latest_application = connexion_firebase.get_latest_application()
    latest_model_IA = connexion_firebase.get_latest_model_IA()
    date_du_jour = datetime.date.today().strftime("%Y-%m-%d")

    print("Dernière acquisition:", latest_acquisition)
    print("Dernière application:", latest_application)
    print("Dernier modèle IA:", latest_model_IA)

    snapshot_folder = os.path.join(os.getcwd(), 'snapshot')

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

                images, predictions, timestamp_str = enregistrer_snapshot(adresse_ip, port, nom_utilisateur, mot_de_passe, duree_salve, nb_images)

                print("Prédictions:", predictions)

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

                mean_pub = np.mean(pourcentages_pub)
                mean_no_pub = np.mean(pourcentages_nopub)

                print("Moyenne des probabilités de pub :", mean_pub)
                print("Moyenne des probabilités de no pub :", mean_no_pub)


                timestamp_str = obtenir_timestamp_str()
                enregistrer_dans_firestore(pourcentages_pub_list, pourcentages_nopub_list, mean_pub, mean_no_pub, timestamp_str)
            else:
                print("Aucune acquisition trouvée dans la base de données.")
        else:
            print("Impossible de continuer car le modèle n'a pas été chargé avec succès.")


    if __name__ == "__main__":
        main()