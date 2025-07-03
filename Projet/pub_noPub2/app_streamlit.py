import streamlit as st
import numpy as np
import tensorflow as tf
import cv2
import os

# 🔄 Charger le dernier modèle .keras dans le dossier /models
@st.cache_resource
def load_latest_model():
    model_dir = "models"
    model_files = [f for f in os.listdir(model_dir) if f.endswith(".keras")]
    latest_model = max(model_files, key=lambda f: os.path.getmtime(os.path.join(model_dir, f)))
    model_path = os.path.join(model_dir, latest_model)
    st.success(f"Modèle chargé : {latest_model}")
    return tf.keras.models.load_model(model_path)

model = load_latest_model()

# 🔍 Fonction de prédiction
def predict(image):
    image_resized = cv2.resize(image, (100, 100))
    image_normalized = image_resized / 255.0
    image_batch = np.expand_dims(image_normalized, axis=0)

    prediction = model.predict(image_batch)[0]
    label = "pub" if prediction[1] > prediction[0] else "nopub"
    confidence = round(float(max(prediction)) * 100, 2)
    return label, confidence

# 🎨 Interface utilisateur
st.title("🧠 Détection de logo TV : pub ou nopub")
st.write("Upload une image, et le modèle prédit si elle contient un logo TV.")

uploaded_file = st.file_uploader("📂 Choisissez une image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    st.image(image_rgb, caption="Image chargée", use_column_width=True)

    label, confidence = predict(image_rgb)
    st.markdown(f"### Résultat : **{label.upper()}** ({confidence}%)")
