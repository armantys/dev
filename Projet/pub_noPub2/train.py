import os
import cv2
import numpy as np
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

print("Répertoire de travail actuel:", os.getcwd())

# Déclarer une variable globale pour stocker le modèle
loaded_model = None

def load_or_train_model():
    global loaded_model
    if loaded_model is not None:
        return loaded_model

    # Chercher le dernier modèle .keras dans le dossier models
    model_dir = "models"
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    model_files = [f for f in os.listdir(model_dir) if f.endswith(".keras")]
    if model_files:
        latest_model = max(model_files, key=lambda f: os.path.getmtime(os.path.join(model_dir, f)))
        model_path = os.path.join(model_dir, latest_model)
        print(f"Chargement du modèle existant : {model_path}")
        loaded_model = tf.keras.models.load_model(model_path)
        return loaded_model
    else:
        print("Aucun modèle n'a été trouvé. Entraînement d'un nouveau modèle...")
        model = train_model()
        loaded_model = model
        return model

def train_model():
    target_size = (100, 100)

    # Chargement des données
    pub_images = load_and_resize_images_from_folder(r"datasets\pub_no_pubV3\logo-tv", target_size)
    nopub_images = load_and_resize_images_from_folder(r"datasets\pub_no_pubV3\pas-logo-tv", target_size)

    pub_labels = np.ones(len(pub_images))
    nopub_labels = np.zeros(len(nopub_images))

    images = np.concatenate((pub_images, nopub_images))
    labels = np.concatenate((pub_labels, nopub_labels))

    # ✅ Normalisation des images
    images = images / 255.0

    # Split train/test
    X_train, X_test, y_train, y_test = train_test_split(images, labels, test_size=0.3, random_state=42)

    # ✅ Modèle CNN avec keras.Input
    model_cnn = keras.Sequential([
        keras.layers.Input(shape=(100, 100, 3)),
        keras.layers.Conv2D(64, (3, 3), activation='relu'),
        keras.layers.MaxPooling2D(2, 2),
        keras.layers.Conv2D(128, (3, 3), activation='relu'),
        keras.layers.MaxPooling2D(2, 2),
        keras.layers.Conv2D(256, (3, 3), activation='relu'),
        keras.layers.MaxPooling2D(2, 2),
        keras.layers.Flatten(),
        keras.layers.Dropout(0.3),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(2, activation='softmax')
    ])

    model_cnn.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    # ✅ Sauvegarde avec timestamp (.keras format)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_path = f"models/model_{timestamp}.keras"
    model_checkpoint = ModelCheckpoint(model_path, save_best_only=True, monitor='val_accuracy', mode='max', verbose=1)
    early_stopping = EarlyStopping(monitor='val_accuracy', patience=10, mode='max', verbose=1, restore_best_weights=True )

    # Entraînement
    model_cnn.fit(
        X_train, y_train,
        epochs=100,
        validation_data=(X_test, y_test),
        callbacks=[model_checkpoint, early_stopping]
    )

    # Évaluation
    loss, acc = model_cnn.evaluate(X_test, y_test)
    print(f"\n✅ Précision du modèle sur test : {acc:.4f}")

    # ✅ Rapport de classification
    y_pred = np.argmax(model_cnn.predict(X_test), axis=1)
    print("\n📊 Rapport de classification :\n")
    print(classification_report(y_test, y_pred, target_names=["nopub", "pub"]))

    return model_cnn

def predict_images(images):
    model = load_or_train_model()

    processed_images = [cv2.resize(image, (100, 100)) for image in images]
    processed_images = np.array(processed_images) / 255.0

    predictions = model.predict(processed_images)
    labels = ['nopub' if prediction[0] > prediction[1] else 'pub' for prediction in predictions]

    return labels

def load_and_resize_images_from_folder(folder, target_size):
    images = []
    print("Chargement des images depuis le dossier:", folder)
    abs_folder = os.path.abspath(folder)
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
                img = cv2.resize(img, target_size)
                images.append(img)
                print("Image chargée avec succès.")
            else:
                print("ERREUR: Impossible de charger l'image:", filename)
        else:
            print("Le chemin spécifié n'est pas un fichier:", filepath)

    print("Chargement terminé. Nombre total d'images chargées:", len(images))
    return images

# Point d'entrée
if __name__ == "__main__":
    model = load_or_train_model()
    if model:
        print("Modèle chargé avec succès.")
    else:
        print("Erreur lors du chargement du modèle.")
