import os
import cv2
import numpy as np

# Définir les chemins des dossiers contenant les images
noir_blanc_dir = 'plan_noir_blanc'
couleur_dir = 'plan_couleur_redimensionne'
output_noir_blanc_dir = 'plan_noir_blanc_augmente'
output_couleur_dir = 'plan_couleur_redimensionne_augmente'

# Vérifier si les dossiers existent
if not os.path.exists(noir_blanc_dir) or not os.path.exists(couleur_dir):
    print("Les dossiers spécifiés n'existent pas.")
    exit()

# Créer les dossiers de sortie s'ils n'existent pas
os.makedirs(output_noir_blanc_dir, exist_ok=True)
os.makedirs(output_couleur_dir, exist_ok=True)

# Récupérer la liste des fichiers dans les dossiers
noir_blanc_files = os.listdir(noir_blanc_dir)
couleur_files = os.listdir(couleur_dir)

# Vérifier si le nombre d'images est le même dans les deux dossiers
if len(noir_blanc_files) != len(couleur_files):
    print("Le nombre d'images dans les dossiers n'est pas le même.")
    exit()

# Définir les transformations d'augmentation
def augmentation(image):
    # Rotation aléatoire entre -10 et 10 degrés
    angle = np.random.randint(-10, 10)
    # Obtenir les dimensions de l'image
    h, w = image.shape[:2]
    # Calculer le centre de l'image
    center = (w // 2, h // 2)
    # Créer la matrice de rotation
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    # Appliquer la rotation à l'image
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)
    return rotated

# Parcourir les images et appliquer l'augmentation
for nb_file, couleur_file in zip(noir_blanc_files, couleur_files):
    # Charger les images
    image_nb = cv2.imread(os.path.join(noir_blanc_dir, nb_file))
    image_couleur = cv2.imread(os.path.join(couleur_dir, couleur_file))
    
    # Appliquer l'augmentation 20 fois
    for i in range(20):
        # Appliquer l'augmentation
        image_nb_augmente = augmentation(image_nb)
        image_couleur_augmente = augmentation(image_couleur)
        
        # Enregistrer les images augmentées dans les dossiers de sortie
        cv2.imwrite(os.path.join(output_noir_blanc_dir, f"{nb_file.split('.')[0]}_{i}.jpg"), image_nb_augmente)
        cv2.imwrite(os.path.join(output_couleur_dir, f"{couleur_file.split('.')[0]}_{i}.jpg"), image_couleur_augmente)

print("Augmentation terminée.")
