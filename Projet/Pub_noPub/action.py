import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Charger le modèle entraîné
model = load_model('mon_model.h5')

# Paramètres de la caméra
camera = cv2.VideoCapture(0)  # Utilisez 0 pour la caméra par défaut, ajustez selon votre configuration
img_height, img_width = 100, 100

while True:
    # Capturez la vidéo image par image
    ret, frame = camera.read()

    # Redimensionnez l'image à la taille attendue par votre modèle
    resized_frame = cv2.resize(frame, (img_width, img_height))

    # Convertissez l'image en tableau NumPy et étendez les dimensions pour l'inférence
    img_array = np.expand_dims(resized_frame, axis=0)

    # Assurez-vous que l'image est normalisée
    img_array = img_array / 255.0

    # Faites la prédiction
    prediction = model.predict(img_array)

    # Seuil de probabilité pour la classification
    threshold = 0.5

    # Interprétation de la prédiction
    label = "Logo" if prediction >= threshold else "No Logo"

    # Afficher le résultat sur l'image en direct
    cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('Live Prediction', frame)

    # Quittez la boucle si la touche 'q' est enfoncée
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérez la capture de la caméra et fermez la fenêtre
camera.release()
cv2.destroyAllWindows()