import requests
from requests.auth import HTTPDigestAuth
import time
import datetime
import shutil
import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from connexion_firebase import initialize_storage

# Charger le modèle une seule fois au début du programme
MODEL = None

def load_global_model():
    global MODEL
    if MODEL is None:
        MODEL = load_model('test_5.keras')

def capture_images(url_flux_video, nom_utilisateur, mot_de_passe, nb_images_par_salve, snapshot_folder, intervalle):
    images = []
    for i in range(nb_images_par_salve):
        response = requests.get(url_flux_video, auth=HTTPDigestAuth(nom_utilisateur, mot_de_passe), stream=True)
        if response.status_code == 200:
            img_array = np.array(bytearray(response.content), dtype=np.uint8)
            frame = cv2.imdecode(img_array, -1)
            height, width, _ = frame.shape
            top_right = frame[0:height//2, width//2:width]
            filename = f"snapshot_{i+1}.jpg"
            filepath = os.path.join(snapshot_folder, filename)
            cv2.imwrite(filepath, top_right)
            print(f"Snapshot {i+1}/{nb_images_par_salve} enregistré avec succès dans {snapshot_folder}!")
            image = cv2.imread(filepath)
            images.append(image)
            time.sleep(intervalle)  # Pause entre les captures d'images
        else:
            print("Impossible de récupérer l'image")
    return images

def predict_images(images):
    predictions = []
    for image in images:
        img_resized = cv2.resize(image, (100, 100))
        image_array = np.array(img_resized)
        image_array = np.expand_dims(image_array, axis=0)
        prediction = MODEL.predict(image_array)
        predictions.append(prediction)
    return predictions

def enregistrer_snapshot(adresse_ip, port, nom_utilisateur, mot_de_passe, duree_salve, nb_images_par_salve):
    load_global_model()  # Charger le modèle si ce n'est pas déjà fait
    start_time = time.time()  # Enregistrer le temps de début
    intervalle = duree_salve / nb_images_par_salve
    date_du_jour = datetime.date.today().strftime("%Y-%m-%d")
    now = datetime.datetime.now()
    timestamp_str = now.strftime("%Y-%m-%d_%H-%M-%S")
    snapshot_folder = os.path.join(os.getcwd(), 'snapshot', date_du_jour)

    if not os.path.exists(snapshot_folder):
        os.makedirs(snapshot_folder)

    url_flux_video = f'http://{adresse_ip}:{port}/cgi-bin/CGIProxy.fcgi?cmd=snapPicture2&usr={nom_utilisateur}&pwd={mot_de_passe}'
    images = capture_images(url_flux_video, nom_utilisateur, mot_de_passe, nb_images_par_salve, snapshot_folder, intervalle)
    predictions = predict_images(images)

    end_time = time.time()  # Enregistrer le temps de fin
    execution_time = end_time - start_time  # Calculer le temps total d'exécution de la fonction
    print(f"La fonction a mis {execution_time} secondes pour s'exécuter.")

    if os.path.exists(snapshot_folder):
        shutil.rmtree(snapshot_folder)
        print(f"Le dossier {snapshot_folder} a été supprimé avec succès !")
    else:
        print(f"Le dossier {snapshot_folder} n'existe pas.")

    print(f"Tous les snapshots ont été enregistrés avec succès dans {snapshot_folder}!")
    return images, predictions  # Retourner à la fois les images et les prédictions
