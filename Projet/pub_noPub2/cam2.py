import cv2
import numpy as np
import tensorflow as tf

# Charger le modèle
model = tf.keras.models.load_model('modeleOK1.h5')

# Fonction pour afficher du texte
def afficher_texte(image, texte, position=(10, 30), couleur=(0, 255, 0), taille=1):
    cv2.putText(image, texte, position, cv2.FONT_HERSHEY_SIMPLEX, taille, couleur, 2)

# Zones par défaut
top_left_box = (100, 100)
top_right_box = (300, 100)

# Callback souris pour ajuster les zones
def mouse_callback(event, x, y, flags, param):
    global top_left_box, top_right_box
    if event == cv2.EVENT_LBUTTONDOWN:
        if x < param.shape[1] // 2:
            top_left_box = (x, y)
        else:
            top_right_box = (x, y)

# Ouvrir la webcam
cap = cv2.VideoCapture(0)
cv2.namedWindow('Webcam')
cv2.setMouseCallback('Webcam', mouse_callback)

input_shape = (100, 100)

while True:
    ret, frame = cap.read()
    if not ret or frame is None:
        print("❌ Problème de lecture caméra.")
        break

    try:
        # Zones d'analyse
        top_left = frame[top_left_box[1]:top_left_box[1]+100, top_left_box[0]:top_left_box[0]+100]
        top_right = frame[top_right_box[1]:top_right_box[1]+100, top_right_box[0]:top_right_box[0]+100]

        if top_left.shape[:2] != input_shape or top_right.shape[:2] != input_shape:
            raise ValueError("💥 Mauvais format d'une des zones (doit être 100x100)")

        # Prétraitement
        left_input = np.expand_dims(top_left / 255.0, axis=0)
        right_input = np.expand_dims(top_right / 255.0, axis=0)

        # Prédiction
        pred_left = model.predict(left_input, verbose=0)[0]
        pred_right = model.predict(right_input, verbose=0)[0]

        # Résultats
        label_left = "Pub" if np.argmax(pred_left) == 1 else "No Pub"
        label_right = "Pub" if np.argmax(pred_right) == 1 else "No Pub"
        conf_left = np.max(pred_left) * 100
        conf_right = np.max(pred_right) * 100
        color_left = (0, 255, 0) if label_left == "No Pub" else (0, 0, 255)
        color_right = (0, 255, 0) if label_right == "No Pub" else (0, 0, 255)

        # Affichage
        cv2.rectangle(frame, top_left_box, (top_left_box[0]+100, top_left_box[1]+100), color_left, 2)
        cv2.rectangle(frame, top_right_box, (top_right_box[0]+100, top_right_box[1]+100), color_right, 2)
        afficher_texte(frame, f"{label_left} ({conf_left:.1f}%)", (top_left_box[0], top_left_box[1]-10), color_left)
        afficher_texte(frame, f"{label_right} ({conf_right:.1f}%)", (top_right_box[0], top_right_box[1]-10), color_right)

    except Exception as e:
        print(f"⚠️ Erreur dans la boucle principale : {e}")

    # Afficher le flux
    cv2.imshow('Webcam', frame)

    # Touche Q pour quitter
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
