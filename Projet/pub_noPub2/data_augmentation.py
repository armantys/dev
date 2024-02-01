import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
import shutil

# Définition des chemins des dossiers
dossier_racine = r'C:\Users\ludovic.souquet\Documents\GitHub\ludovic.souquet\Projet\pub_noPub2'
dossier_datasets = os.path.join(dossier_racine, 'datasets')
dossier_image_logo = os.path.join(dossier_datasets, 'image_folder')
dossier_image_no_logo = os.path.join(dossier_datasets, 'image_folder_no_logo')

# Création d'un dossier pour les images augmentées
dossier_augmente = os.path.join(dossier_datasets, 'augmente')
os.makedirs(dossier_augmente, exist_ok=True)

# Paramètres pour la data augmentation
datagen = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

# Fonction pour appliquer la data augmentation et sauvegarder les images augmentées
def augmenter_images(input_folder, output_folder, prefix, nb_augmentations):
    os.makedirs(output_folder, exist_ok=True)
    images = os.listdir(input_folder)

    for img_name in images:
        img_path = os.path.join(input_folder, img_name)
        img = image.load_img(img_path, target_size=(100, 100))
        img_array = image.img_to_array(img)
        img_array = img_array.reshape((1,) + img_array.shape)

        i = 0
        for batch in datagen.flow(img_array, batch_size=1, save_to_dir=output_folder, save_prefix=prefix, save_format='jpeg'):
            i += 1
            if i >= nb_augmentations:
                break

# Appliquer la data augmentation pour les images avec logos
augmenter_images(dossier_image_logo, os.path.join(dossier_augmente, 'logo'), 'aug_logo', 5)

# Appliquer la data augmentation pour les images sans logos
augmenter_images(dossier_image_no_logo, os.path.join(dossier_augmente, 'no_logo'), 'aug_no_logo', 5)
