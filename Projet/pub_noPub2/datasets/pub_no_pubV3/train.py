import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

print("Répertoire de travail actuel:", os.getcwd())

# Définir la taille cible des images
target_size = (100, 100)

# Définir la fonction pour charger et redimensionner les images depuis le dossier
def load_and_resize_images_from_folder(folder):
    images = []
    print("Chargement des images depuis le dossier:", folder)
    abs_folder = os.path.abspath(folder)  # Chemin absolu du dossier
    print("Chemin absolu du dossier:", abs_folder)

    if not os.path.exists(abs_folder):
        print("ERREUR: Le dossier spécifié n'existe pas.")
        return images

    for filename in os.listdir(abs_folder):
        filepath = os.path.join(abs_folder, filename)
        if os.path.isfile(filepath):
            print("Chargement de l'image:", filename)
            img = cv2.imread(filepath)
            if img is not None:
                img = cv2.resize(img, target_size)  # Redimensionner l'image à la taille cible
                images.append(img)
                print("Image chargée avec succès.")
            else:
                print("ERREUR: Impossible de charger l'image:", filename)
        else:
            print("Le chemin spécifié n'est pas un fichier:", filepath)

    print("Chargement terminé. Nombre total d'images chargées:", len(images))
    return images

# Utilisation de la fonction pour charger et redimensionner les images depuis le dossier
folder_path = "logo-tv"  # Chemin du dossier contenant les images
images = load_and_resize_images_from_folder(folder_path)

# Exemple d'utilisation : Afficher le nombre d'images chargées
print("Nombre total d'images chargées depuis le dossier:", len(images))

# Charger et redimensionner les images depuis les dossiers "pub" et "nopub"
pub_images = load_and_resize_images_from_folder(r"datasets\pub_no_pubV3\logo-tv")
nopub_images = load_and_resize_images_from_folder(r"datasets\pub_no_pubV3\pas-logo-tv")

# Créer les étiquettes correspondantes (1 pour "pub" et 0 pour "nopub")
pub_labels = np.ones(len(pub_images))
nopub_labels = np.zeros(len(nopub_images))

# Concaténer les images et les étiquettes
images = np.concatenate((pub_images, nopub_images))
labels = np.concatenate((pub_labels, nopub_labels))

# Diviser les données en ensembles d'apprentissage et de test
X_train, X_test, y_train, y_test = train_test_split(images, labels, test_size=0.3, random_state=42)

# Créer un modèle CNN Keras avec couche de convolution supplémentaire, pooling et dropout
model_cnn = keras.Sequential([
    keras.layers.Conv2D(64, (3, 3), activation='relu', input_shape=(100, 100, 3)),
    keras.layers.MaxPooling2D(2, 2),
    keras.layers.Conv2D(128, (3, 3), activation='relu'),
    keras.layers.MaxPooling2D(2, 2),
    keras.layers.Conv2D(256, (3, 3), activation='relu'),
    keras.layers.MaxPooling2D(2, 2),
    keras.layers.Flatten(),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')
])

# Compiler le modèle CNN Keras
model_cnn.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Définir un callback pour enregistrer le modèle avec la meilleure précision sur les données de validation
model_checkpoint = ModelCheckpoint('test_5.keras', save_best_only=True, monitor='val_accuracy', mode='max', verbose=1)

# Définir un callback pour arrêter l'entraînement si la précision ne s'améliore pas pendant un certain nombre d'époques
early_stopping = EarlyStopping(monitor='val_accuracy', patience=5, mode='max', verbose=1)

# Entraîner le modèle CNN Keras avec les données d'entraînement
model_cnn.fit(X_train, y_train, epochs=50, validation_data=(X_test, y_test), callbacks=[model_checkpoint, early_stopping])

# Évaluer le modèle CNN Keras sur les données de test
accuracy = model_cnn.evaluate(X_test, y_test)[1]
print(f"Précision du modèle CNN Keras sur les données de test: {accuracy}")
