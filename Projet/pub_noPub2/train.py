import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

print("Répertoire de travail actuel:", os.getcwd())

def load_or_train_model():
    model_path = "test_5.keras"
    if os.path.exists(model_path):
        # Charger le modèle existant
        print("Chargement du modèle existant...")
        return tf.keras.models.load_model(model_path)
    else:
        # Si le modèle n'existe pas, effectuer le processus d'entraînement
        print("Aucun modèle n'a été trouvé. Entraînement d'un nouveau modèle...")
        # Votre code d'entraînement ici
        # Assurez-vous de sauvegarder le modèle après l'entraînement
        model = train_model()  # Appel de la fonction pour l'entraînement du modèle
        return model

def train_model():
    # Définir la taille cible des images
    target_size = (100, 100)

    # Charger et redimensionner les images depuis les dossiers "pub" et "nopub"
    pub_images = load_and_resize_images_from_folder(r"datasets\pub_no_pubV3\logo-tv", target_size)
    nopub_images = load_and_resize_images_from_folder(r"datasets\pub_no_pubV3\pas-logo-tv", target_size)

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
        keras.layers.Dense(2, activation='softmax')  # Nombre de neurones = nombre de classes
    ])

    # Compiler le modèle CNN Keras
    model_cnn.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    # Définir un callback pour enregistrer le modèle avec la meilleure précision sur les données de validation
    model_checkpoint = ModelCheckpoint('test_5.keras', save_best_only=True, monitor='val_accuracy', mode='max', verbose=1)

    # Définir un callback pour arrêter l'entraînement si la précision ne s'améliore pas pendant un certain nombre d'époques
    early_stopping = EarlyStopping(monitor='val_accuracy', patience=5, mode='max', verbose=1)

    # Entraîner le modèle CNN Keras avec les données d'entraînement
    model_cnn.fit(X_train, y_train, epochs=50, validation_data=(X_test, y_test), callbacks=[model_checkpoint, early_stopping])

    # Évaluer le modèle CNN Keras sur les données de test
    accuracy = model_cnn.evaluate(X_test, y_test)[1]
    print(f"Précision du modèle CNN Keras sur les données de test: {accuracy}")

    return model_cnn

def predict_images(images):
    # Charger le modèle entraîné
    model = tf.keras.models.load_model('test_5.keras')

    # Prétraiter les images avant de les passer au modèle
    processed_images = [cv2.resize(image, (100, 100)) for image in images]
    processed_images = np.array(processed_images) / 255.0  # Normalisation des valeurs de pixel

    # Effectuer les prédictions sur les images
    predictions = model.predict(processed_images)

    # Convertir les prédictions en étiquettes (0 pour nopub, 1 pour pub)
    labels = ['nopub' if prediction[0] < 0.5 else 'pub' for prediction in predictions]

    return labels

# Définir la fonction pour charger et redimensionner les images depuis le dossier
def load_and_resize_images_from_folder(folder, target_size):
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

# Si vous souhaitez tester la fonction de chargement ou d'entraînement du modèle individuellement
if __name__ == "__main__":
    model = load_or_train_model()
    if model:
        print("Modèle chargé avec succès.")
    else:
        print("Impossible de charger le modèle. Veuillez vérifier le code d'entraînement.")
