import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt

# Chemin vers le dossier contenant vos images originales
original_dataset_path = r"C:\Users\ludovic.souquet\Documents\GitHub\ludovic.souquet\Projet\Pub_noPub\pubnopub\nologo\normal"

# Chemin vers le dossier où vous souhaitez enregistrer les images augmentées
augmented_dataset_path = r"C:\Users\ludovic.souquet\Documents\GitHub\ludovic.souquet\Projet\Pub_noPub\pubnopub\nologo\augmenter"

# Créer un générateur d'images avec augmentation
datagen = ImageDataGenerator(
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

# Liste des extensions de fichiers image supportées
image_extensions = ['.jpg', '.jpeg', '.png']

# Parcourir toutes les images dans le dossier original
for root, dirs, files in os.walk(original_dataset_path):
    for file in files:
        # Vérifier si le fichier est une image basée sur son extension
        if any(file.lower().endswith(ext) for ext in image_extensions):
            original_image_path = os.path.join(root, file)
            img = image.load_img(original_image_path, target_size=(100, 100))

            # Convertir l'image en tableau numpy
            x = image.img_to_array(img)
            x = x.reshape((1,) + x.shape)

            # Générer des images augmentées
            i = 0
            while i < 20:  # Générer 5 images augmentées par image originale
                for batch in datagen.flow(x, batch_size=1, save_to_dir=augmented_dataset_path, save_prefix='aug', save_format='jpeg'):
                    i += 1
                    break