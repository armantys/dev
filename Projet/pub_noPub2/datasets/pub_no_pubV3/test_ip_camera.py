import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras

# Charger le modèle CNN Keras entraîné
model_cnn = keras.models.load_model('test_2.keras')

# Définir la taille du carré
square_size = 100
square_color = (0, 0, 255)  # Rouge (en format BGR) par défaut
square_thickness = 2  # Épaisseur des bords rouges du carré

# Position initiale du carré
x, y = 100, 100

# Définir la zone de vérification (carré) sur la vidéo
def draw_square(frame, x, y, size, color, thickness):
    cv2.rectangle(frame, (x, y), (x + size, y + size), color, thickness)

# Utiliser les informations du profil pour configurer la connexion à la caméra IP
username = "dev_IA_P3"  # Utilisez votre nom d'utilisateur
password = "dev_IA_P3"  # Utilisez votre mot de passe
camera_ip_address = "192.168.20.37"  # Utilisez votre adresse IP de caméra
port = 88  # Utilisez le port de la caméra

# Construire l'URL du flux RTSP de la caméra IP en utilisant les informations du profil
url = f'rtsp://{username}:{password}@{camera_ip_address}:{port}/videoMain'

# Utiliser VideoCapture pour lire le flux
cap = cv2.VideoCapture(url)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    if ret:
        # Dessiner le carré avec des bords rouges
        draw_square(frame, x, y, square_size, square_color, square_thickness)

        # Extraire la zone carrée pour la prédiction
        roi = frame[y:y+square_size, x:x+square_size]
    
        # Redimensionner la zone carrée pour l'entrée du modèle
        roi = cv2.resize(roi, (100, 100))
    
        # Normaliser l'image pour la prédiction
        roi = roi / 255.0
    
        # Effectuer la prédiction
        prediction = model_cnn.predict(np.expand_dims(roi, axis=0))
    
        # Afficher la prédiction à côté du carré
        if prediction[0][0] > 0.5:
            text = "Logo"
            square_color = (0, 255, 0)  # Vert (en format BGR) si c'est un logo
        else:
            text = "Non Logo"
            square_color = (0, 0, 255)  # Rouge (en format BGR) si ce n'est pas un logo

        cv2.putText(frame, text, (x + square_size + 10, y + square_size // 2), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Affiche le cadre
        cv2.imshow('Camera IP', frame)

        # Lire la touche du clavier
        key = cv2.waitKey(1)

        # Déplacer le carré avec les touches fléchées
        if key == ord('z'):
            y -= 10
        elif key == ord('s'):
            y += 10
        elif key == ord('q'):
            x -= 10
        elif key == ord('d'):
            x += 10

        # Quitte la boucle si 'q' est pressé
        if key & 0xFF == ord('a'):
            break
    else:
        break

# Lorsque tout est fini, relâche la capture
cap.release()
cv2.destroyAllWindows()