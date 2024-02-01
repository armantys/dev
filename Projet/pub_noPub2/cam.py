import cv2
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.optimizers import Adam
import numpy as np

# Charger le modèle pré-entraîné
model = tf.keras.models.load_model('modele_logo.h5')

# Paramètres pour la capture vidéo
cap = cv2.VideoCapture(0)  # 0 correspond à la caméra par défaut
cap.set(3, 640)  # Largeur de la fenêtre de capture
cap.set(4, 480)  # Hauteur de la fenêtre de capture

# Réglages du modèle
input_shape = (100, 100, 3)
batch_size = 32

# Réentraîner le modèle avec un taux d'apprentissage plus bas
model.compile(optimizer=Adam(learning_rate=0.0001), loss='binary_crossentropy', metrics=['accuracy'])

while True:
    # Capture d'une image depuis la caméra
    ret, frame = cap.read()

    # Redimensionner l'image pour l'entrée du modèle
    img = cv2.resize(frame, (input_shape[0], input_shape[1]))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  # Normalisation

    # Effectuer la prédiction
    prediction = model.predict(img_array)

    # Interpréter la prédiction et afficher le résultat sur l'image
    if prediction[0][0] > 0.5:
        label = "Logo"
        color = (0, 255, 0)  # Couleur verte pour le texte
        if label == "Pas de logo":
            print(f"Faux positif - Image avec logo prédite comme sans logo. Probabilité : {prediction[0][0]}")
    else:
        label = "Pas de logo"
        color = (0, 0, 255)  # Couleur rouge pour le texte
        if label == "Logo":
            print(f"Faux négatif - Image sans logo prédite comme avec logo. Probabilité : {1 - prediction[0][0]}")

    # Afficher le résultat sur l'image en temps réel
    cv2.putText(frame, f"{label} - {prediction[0][0]:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    cv2.imshow('Logo Detection', frame)

    # Quitter la boucle si la touche 'q' est enfoncée
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer la capture vidéo et fermer la fenêtre
cap.release()
cv2.destroyAllWindows()