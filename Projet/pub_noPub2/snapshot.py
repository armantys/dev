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
from model import predict_advertisement


def obtenir_timestamp_str():
    return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


# Initialisation du stockage Firebase
bucket = initialize_storage()

# Charger le modèle une seule fois au début du programme
MODEL = None



def apply_gamma_correction(image, gamma=1.0):
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, table)

def capture_images(url_flux_video, nom_utilisateur, mot_de_passe, nb_images_par_salve, snapshot_folder, intervalle, timestamp_str):
    images = []
    for i in range(nb_images_par_salve):
        response = requests.get(url_flux_video, auth=HTTPDigestAuth(nom_utilisateur, mot_de_passe), stream=True)
        if response.status_code == 200:
            img_array = np.array(bytearray(response.content), dtype=np.uint8)
            frame = cv2.imdecode(img_array, -1)
            # Appliquer une correction gamma à l'image capturée
            corrected_image = apply_gamma_correction(frame, gamma=0.7)  # Ajuster le paramètre gamma selon vos besoins
            # Spécifier les coordonnées de la région d'intérêt manuellement (xmin, ymin, xmax, ymax)
            roi = corrected_image[170:270, 1230:1330]
            cropped_image = cv2.resize(roi, (100, 100))  # Recadrer l'image en 100x100 pixels
            filename = f"snapshot_{i+1}.jpg"
            filepath = os.path.join(snapshot_folder, filename)
            cv2.imwrite(filepath, cropped_image)
            print(f"Snapshot {i+1}/{nb_images_par_salve} enregistré avec succès dans {snapshot_folder}!")
            image = cv2.imread(filepath)
            images.append(image)
            upload_to_storage(filepath, filename, timestamp_str)  # Enregistrer l'image dans Firebase Storage avec timestamp_str
            time.sleep(intervalle)  # Pause entre les captures d'images
        else:
            print("Impossible de récupérer l'image")
    return images

def upload_to_storage(filepath, filename, timestamp_str):
    blob = bucket.blob(f"images_pub_no_pub/salves/{timestamp_str}/{filename}")
    blob.upload_from_filename(filepath)
    print(f"Image {filename} enregistrée dans Firebase Storage.")

def predict_images(images):
    predictions = []
    for image in images:
        prob_advertisement, prob_no_advertisement = predict_advertisement(image)
        predictions.append([float(prob_advertisement), float(prob_no_advertisement)])
    return predictions

def enregistrer_snapshot(adresse_ip, port, nom_utilisateur, mot_de_passe, duree_salve, nb_images_par_salve):
    start_time = time.time()  # Enregistrer le temps de début
    intervalle = int(duree_salve) / int(nb_images_par_salve)
    date_du_jour = datetime.date.today().strftime("%Y-%m-%d")
    now = datetime.datetime.now()
    timestamp_str = now.strftime("%Y-%m-%d_%H-%M-%S")
    snapshot_folder = os.path.join(os.getcwd(), 'snapshot', date_du_jour)

    if not os.path.exists(snapshot_folder):
        os.makedirs(snapshot_folder)

    url_flux_video = f'http://{adresse_ip}:{port}/cgi-bin/CGIProxy.fcgi?cmd=snapPicture2&usr={nom_utilisateur}&pwd={mot_de_passe}'
    images = capture_images(url_flux_video, nom_utilisateur, mot_de_passe, int(nb_images_par_salve), snapshot_folder, intervalle, timestamp_str)
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

    return images, predictions, timestamp_str  # Retourner à la fois les images, les prédictions et le timestamp
