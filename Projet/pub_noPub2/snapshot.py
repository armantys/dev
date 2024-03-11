import requests
from requests.auth import HTTPDigestAuth
from predict import obtenir_pourcentages
import time
import datetime
import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model


def enregistrer_snapshot(adresse_ip, port, nom_utilisateur, mot_de_passe, duree_salve, nb_images_par_salve):
    # Chargez votre modèle
    model = load_model('test_5.keras')
    intervalle = duree_salve / nb_images_par_salve
    images = []
    predictions = []  # Ajouter une liste pour stocker les prédictions
    # Créer le chemin complet du dossier avec la date actuelle
    date_du_jour = datetime.date.today().strftime("%Y-%m-%d")
    snapshot_folder = os.path.join(os.getcwd(), 'snapshot', date_du_jour)
    
    # Assurez-vous que le répertoire datedujour existe. S'il n'existe pas, créez-le.
    if not os.path.exists(snapshot_folder):
        os.makedirs(snapshot_folder)

    # URL du flux vidéo de la caméra
    url_flux_video = f'http://{adresse_ip}:{port}/cgi-bin/CGIProxy.fcgi?cmd=snapPicture2&usr={nom_utilisateur}&pwd={mot_de_passe}'

    # Boucle pour enregistrer chaque snapshot
    for i in range(nb_images_par_salve):
        # Récupérer l'image du flux vidéo de la caméra
        response = requests.get(url_flux_video, auth=HTTPDigestAuth(nom_utilisateur, mot_de_passe), stream=True)
        if response.status_code == 200:
            img_array = np.array(bytearray(response.content), dtype=np.uint8)
            frame = cv2.imdecode(img_array, -1)

            # Découper l'image en deux parties : haut gauche et haut droite
            height, width, _ = frame.shape
            top_right = frame[0:height//2, width//2:width]

            # Redimensionner l'image
            resized_img = cv2.resize(top_right, (100, 100))

            # Enregistrer l'image recadrée et redimensionnée
            filename = f"snapshot_{i+1}.jpg"  # Utilisation de l'index pour générer un nom de fichier unique
            filepath = os.path.join(snapshot_folder, filename)
            cv2.imwrite(filepath, resized_img)
            print(f"Snapshot {i+1}/{nb_images_par_salve} enregistré avec succès dans {snapshot_folder}!")

            # Charger l'image
            image = cv2.imread(filepath)
            images.append(image)  # Ajouter l'image à la liste des images

            # Prédire les probabilités
            prediction = model.predict(np.array(resized_img).reshape(-1, 100, 100, 3))
            # Ajouter la prédiction à la liste
            predictions.append(prediction)

        else:
            print("Impossible de récupérer l'image")
        time.sleep(intervalle)
        
    print(f"Tous les snapshots ont été enregistrés avec succès dans {snapshot_folder}!")
    return images, predictions  # Retourner à la fois les images et les prédictions
