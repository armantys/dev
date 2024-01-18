# Importations Streamlit
import streamlit as st
import matplotlib.pyplot as plt
import pickle
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image

# Charger le modèle sauvegardé
modele_charge = load_model('mon_modele_mnist.h5')

# Charger l'historique d'entraînement
with open('training_history.pkl', 'rb') as history_file:
    history = pickle.load(history_file)

# Interface Streamlit
st.title('Application MNIST CNN')

# Visualiser l'historique d'entraînement
st.subheader('Visualisation de l\'historique d\'entraînement')

# Graphique d'exactitude
fig1, ax1 = plt.subplots()
ax1.plot(history['accuracy'], label='Précision d\'entraînement')
ax1.plot(history['val_accuracy'], label='Précision de validation')
ax1.set_xlabel('Époque')
ax1.set_ylabel('Précision')
ax1.legend()
st.pyplot(fig1)

# Graphique de perte
fig2, ax2 = plt.subplots()
ax2.plot(history['loss'], label='Perte d\'entraînement')
ax2.plot(history['val_loss'], label='Perte de validation')
ax2.set_xlabel('Époque')
ax2.set_ylabel('Perte')
ax2.legend()
st.pyplot(fig2)

# Interface pour tester une prédiction
st.subheader('Tester une prédiction avec le modèle chargé')

# Charger une image de test
uploaded_file = st.file_uploader("Choisissez une image de chiffre manuscrit...", type="png")

if uploaded_file is not None:
    # Prétraiter l'image et faire une prédiction
    image = Image.open(uploaded_file).convert('L')  # Convertir en niveau de gris
    image = np.array(image.resize((28, 28))) / 255.0  # Redimensionner et normaliser
    image = image.reshape((1, 28, 28, 1))  # Ajouter une dimension pour le lot

    # Faire la prédiction avec le modèle
    prediction = modele_charge.predict(image)
    predicted_class = np.argmax(prediction)

    # Vérifier si la prédiction est correcte
    true_label = st.number_input("Entrez la vraie classe (0-9)", min_value=0, max_value=9, step=1)
    correct_prediction = (predicted_class == true_label)

    # Afficher le résultat de la prédiction
    st.write(f"Classe prédite : {predicted_class}")
    st.write(f"Confiance : {prediction[0][predicted_class]:.2%}")
    st.write(f"Prédiction correcte : {'Oui' if correct_prediction else 'Non'}")

    # Ajouter au journal des prédictions
    with open('predictions_log.txt', 'a') as log_file:
        log_file.write(f"Classe réelle : {true_label}, Classe prédite : {predicted_class}, Prédiction correcte : {correct_prediction}\n")

    # Afficher l'image téléchargée
    st.image(uploaded_file, caption='Image de test', use_column_width=True)

