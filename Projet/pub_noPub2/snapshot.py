import cv2
import requests
import numpy as np
from requests.auth import HTTPDigestAuth

# Paramètres de la caméra IP
adresse_ip = '192.168.20.37'  # Adresse IP de votre caméra IP
port = 88  # Port par défaut pour la plupart des caméras IP
nom_utilisateur = 'dev_IA_P3'  # Nom d'utilisateur de la caméra
mot_de_passe = 'dev_IA_P3'  # Mot de passe de la caméra

# URL du flux vidéo de la caméra
url_flux_video = f'http://{adresse_ip}:{port}/cgi-bin/CGIProxy.fcgi?cmd=snapPicture2&usr={nom_utilisateur}&pwd={mot_de_passe}'

# Fonction pour enregistrer l'image capturée
def enregistrer_snapshot(url, filename):
    # Récupérer l'image du flux vidéo de la caméra
    response = requests.get(url, auth=HTTPDigestAuth(nom_utilisateur, mot_de_passe), stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print("Snapshot enregistré avec succès!")
    else:
        print("Impossible de récupérer l'image")

# Enregistrer le snapshot
enregistrer_snapshot(url_flux_video, 'snapshot.jpg')