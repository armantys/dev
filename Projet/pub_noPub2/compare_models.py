import os
import time
import numpy as np
import cv2
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.applications import ResNet50, MobileNetV2
from tensorflow.keras.applications.resnet50 import preprocess_input as resnet_preprocess
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input as mobilenet_preprocess
from tensorflow.keras.layers import Input, Dense, Flatten, Dropout, GlobalAveragePooling2D
from tensorflow.keras.models import Sequential
from tensorflow.keras.callbacks import EarlyStopping

# --- CONFIGURATION ---
IMG_SIZE = 100
EPOCHS = 10
BATCH_SIZE = 32
logo_dir = r"datasets\pub_no_pubV3\logo-tv"
nopub_dir = r"datasets\pub_no_pubV3\pas-logo-tv"

# --- UTILS ---
def load_images(folder, label, target_size=(IMG_SIZE, IMG_SIZE)):
    images, labels = [], []
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        img = cv2.imread(path)
        if img is not None:
            img = cv2.resize(img, target_size)
            images.append(img)
            labels.append(label)
    return images, labels

print("📦 Chargement des images...")
X_pub, y_pub = load_images(logo_dir, 1)
X_nopub, y_nopub = load_images(nopub_dir, 0)

X = np.array(X_pub + X_nopub)
y = np.array(y_pub + y_nopub)

X = X / 255.0  # Normalisation standard

# Split train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# --- MODELE 1 : CNN PERSONNALISÉ ---
def build_custom_cnn():
    model = Sequential([
        Input(shape=(IMG_SIZE, IMG_SIZE, 3)),
        keras.layers.Conv2D(64, (3, 3), activation='relu'),
        keras.layers.MaxPooling2D(2, 2),
        keras.layers.Conv2D(128, (3, 3), activation='relu'),
        keras.layers.MaxPooling2D(2, 2),
        keras.layers.Conv2D(256, (3, 3), activation='relu'),
        keras.layers.MaxPooling2D(2, 2),
        Flatten(),
        Dropout(0.3),
        Dense(128, activation='relu'),
        Dense(64, activation='relu'),
        Dense(2, activation='softmax')
    ])
    return model

# --- MODELE 2 : RESNET50 ---
def build_resnet50():
    base_model = ResNet50(include_top=False, input_shape=(IMG_SIZE, IMG_SIZE, 3), weights='imagenet')
    base_model.trainable = False
    model = Sequential([
        base_model,
        GlobalAveragePooling2D(),
        Dropout(0.3),
        Dense(2, activation='softmax')
    ])
    return model

# --- MODELE 3 : MOBILENET V2 ---
def build_mobilenetv2():
    base_model = MobileNetV2(include_top=False, input_shape=(IMG_SIZE, IMG_SIZE, 3), weights='imagenet')
    base_model.trainable = False
    model = Sequential([
        base_model,
        GlobalAveragePooling2D(),
        Dropout(0.3),
        Dense(2, activation='softmax')
    ])
    return model

# --- COMPARAISON ---
models = {
    "CNN personnalisé": build_custom_cnn(),
    "ResNet50": build_resnet50(),
    "MobileNetV2": build_mobilenetv2()
}

histories = {}

for name, model in models.items():
    print(f"\n🚀 Entraînement du modèle : {name}")
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    start = time.time()
    history = model.fit(
        X_train, y_train,
        validation_data=(X_test, y_test),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        callbacks=[EarlyStopping(monitor='val_accuracy', patience=5, restore_best_weights=True)],
        verbose=1
    )
    duration = time.time() - start
    print(f"⏱️ Temps d'entraînement : {duration:.2f} secondes")
    loss, acc = model.evaluate(X_test, y_test)
    print(f"✅ Accuracy {name} : {acc:.4f}")
    y_pred = np.argmax(model.predict(X_test), axis=1)
    print(classification_report(y_test, y_pred, target_names=["nopub", "pub"]))
    histories[name] = (acc, duration)

# --- RÉSUMÉ FINAL ---
print("\n📊 Résumé des performances :")
for model_name, (acc, duration) in histories.items():
    print(f"🧠 {model_name} | Accuracy: {acc:.4f} | Durée: {duration:.2f} sec")

# --- VISUALISATION COMPARATIVE ---
model_names = list(histories.keys())
accuracies = [acc * 100 for acc, _ in histories.values()]
durations = [dur for _, dur in histories.values()]

x = np.arange(len(model_names))  # positions x
width = 0.35  # largeur des barres

fig, ax1 = plt.subplots(figsize=(10, 6))

# Barres pour l'accuracy
bars1 = ax1.bar(x - width/2, accuracies, width, label='Accuracy (%)')
ax1.set_ylabel('Accuracy (%)')
ax1.set_ylim(0, 100)
ax1.set_title('📊 Comparaison des modèles')
ax1.set_xticks(x)
ax1.set_xticklabels(model_names)
ax1.legend(loc='upper left')

# Ajout de la deuxième axe y pour la durée
ax2 = ax1.twinx()
bars2 = ax2.bar(x + width/2, durations, width, color='orange', label='Durée (s)')
ax2.set_ylabel('Durée d\'entraînement (s)')
ax2.legend(loc='upper right')

# Ajout des valeurs sur les barres
for bar in bars1:
    height = bar.get_height()
    ax1.annotate(f'{height:.1f}', xy=(bar.get_x() + bar.get_width() / 2, height),
                 xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')

for bar in bars2:
    height = bar.get_height()
    ax2.annotate(f'{height:.1f}', xy=(bar.get_x() + bar.get_width() / 2, height),
                 xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')

plt.tight_layout()
plt.show()
