import cv2
import os

# Chemin vers votre dossier d'images
folder_path = "plan_noir_blanc"
# Liste pour stocker les noms des fichiers d'images
image_files = []

# Parcours du dossier pour trouver les fichiers d'images
for filename in os.listdir(folder_path):
    # Vérification de l'extension pour s'assurer qu'il s'agit d'un fichier d'image
    if filename.endswith(".png") or filename.endswith(".jpg"):
        # Ajout du chemin complet du fichier à la liste
        image_files.append(os.path.join(folder_path, filename))

# Parcours de la liste des fichiers d'images
for image_file in image_files:
    # Chargement de l'image en niveaux de gris
    image = cv2.imread(image_file, cv2.IMREAD_GRAYSCALE)
    # Affichage de la forme de l'image
    print(f"Forme de l'image {os.path.basename(image_file)}: {image.shape}")