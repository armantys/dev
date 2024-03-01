import cv2
import requests
import numpy as np
from requests.auth import HTTPDigestAuth
import tensorflow as tf
from tensorflow.keras.preprocessing import image

# Charger le modèle pré-entraîné
model = tf.keras.models.load_model('test_5.keras')

# Paramètres de la caméra Foscam
adresse_ip = '192.168.20.37'  # Adresse IP de votre caméra Foscam
port = 88  # Port par défaut pour la plupart des caméras Foscam
nom_utilisateur = 'dev_IA_P3'  # Nom d'utilisateur de la caméra
mot_de_passe = 'dev_IA_P3'  # Mot de passe de la caméra

# URL du flux vidéo de la caméra
url_flux_video = f'http://{adresse_ip}:{port}/cgi-bin/CGIProxy.fcgi?cmd=snapPicture2&usr={nom_utilisateur}&pwd={mot_de_passe}'

# Fonction pour afficher le texte sur l'image
def afficher_texte(image, texte, position=(10, 30), couleur=(0, 255, 0), taille=1):
    cv2.putText(image, texte, position, cv2.FONT_HERSHEY_SIMPLEX, taille, couleur, 2)

# Déclarations des variables globales pour stocker les coordonnées des boîtes englobantes
top_left_box = (400, 80)
top_right_box = (1380, 80)

# Fonction de callback pour capturer les événements de souris
def mouse_callback(event, x, y, flags, param):
    global top_left_box, top_right_box

    if event == cv2.EVENT_LBUTTONDOWN:
        # Vérifier si le clic est dans la zone de la boîte englobante du haut gauche
        if x < 100 and y < 100:
            top_left_box = (x, y)
        # Vérifier si le clic est dans la zone de la boîte englobante du haut droit
        elif x > width//2 and y < 100:
            top_right_box = (x, y)

# Installer le gestionnaire d'événements de la souris
cv2.namedWindow('Flux vidéo de la caméra Foscam')
cv2.setMouseCallback('Flux vidéo de la caméra Foscam', mouse_callback)

while True:
    # Récupérer une image du flux vidéo de la caméra
    reponse = requests.get(url_flux_video, auth=HTTPDigestAuth(nom_utilisateur, mot_de_passe), stream=True)
    img_array = np.array(bytearray(reponse.content), dtype=np.uint8)
    frame = cv2.imdecode(img_array, -1)

    # Découper l'image en deux parties : haut gauche et haut droite
    height, width, _ = frame.shape
    top_left = frame[0:height//2, 0:width//2]
    top_right = frame[0:height//2, width//2:width]

    # Redimensionner les images pour l'entrée du modèle
    input_shape = (100, 100, 3)
    top_left_resized = cv2.resize(top_left, (input_shape[0], input_shape[1]))
    top_right_resized = cv2.resize(top_right, (input_shape[0], input_shape[1]))

    # Convertir les images en tableaux numpy
    top_left_array = np.expand_dims(top_left_resized, axis=0)
    top_right_array = np.expand_dims(top_right_resized, axis=0)

    # Normalisation des images
    top_left_array = top_left_array / 255.0
    top_right_array = top_right_array / 255.0

    # Effectuer les prédictions pour les deux parties de l'image
    prediction_top_left = model.predict(top_left_array)
    prediction_top_right = model.predict(top_right_array)

    # Calculer le pourcentage de certitude de la prédiction
    pourcentage_top_left = prediction_top_left[0][0] * 100
    pourcentage_top_right = prediction_top_right[0][0] * 100

    # Interpréter les prédictions et afficher le résultat sur l'image
    texte_top_left = f"No Pub ({pourcentage_top_left:.2f}%)" if prediction_top_left[0][0] > 0.7 else f"Pub ({pourcentage_top_left:.2f}%)"
    couleur_top_left = (0, 255, 0) if prediction_top_left[0][0] > 0.7 else (0, 0, 255)
    texte_top_right = f"No Pub ({pourcentage_top_right:.2f}%)" if prediction_top_right[0][0] > 0.7 else f"Pub ({pourcentage_top_right:.2f}%)"
    couleur_top_right = (0, 255, 0) if prediction_top_right[0][0] > 0.7 else (0, 0, 255)

    # Dessiner la boîte englobante autour des coordonnées déclarées
    cv2.rectangle(frame, top_left_box, (top_left_box[0] + 100, top_left_box[1] + 100), couleur_top_left, 2)
    cv2.rectangle(frame, top_right_box, (top_right_box[0] + 100, top_right_box[1] + 100), couleur_top_right, 2)

    # Afficher les résultats sur l'image en temps réel
    afficher_texte(frame, texte_top_left, position=(10, 30), couleur=couleur_top_left)
    afficher_texte(frame, texte_top_right, position=(width//2 + 10, 30), couleur=couleur_top_right)

    # Afficher la trame en temps réel
    cv2.imshow('Flux vidéo de la caméra Foscam', frame)

    # Quitter la boucle si la touche 'q' est enfoncée
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Fermer la fenêtre et libérer les ressources
cv2.destroyAllWindows()