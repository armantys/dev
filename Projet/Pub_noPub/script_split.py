import os
import random
from shutil import move

# Chemin du répertoire contenant toutes vos images
all_images_dir = r'C:\Users\ludovic.souquet\Documents\GitHub\ludovic.souquet\Projet\Pub_noPub\dataset\train'

# Répertoires pour l'entraînement et la validation
train_dir = r'C:\Users\ludovic.souquet\Documents\GitHub\ludovic.souquet\Projet\Pub_noPub\pubnopub\dataset\train_split'
validation_dir = r'C:\Users\ludovic.souquet\Documents\GitHub\ludovic.souquet\Projet\Pub_noPub\pubnopub\dataset\validation_split'

# Créer les répertoires d'entraînement et de validation
os.makedirs(train_dir, exist_ok=True)
os.makedirs(validation_dir, exist_ok=True)

# Liste de toutes les images dans le répertoire
all_images = os.listdir(all_images_dir)

# Définir la proportion pour la validation (par exemple, 20%)
validation_proportion = 0.2

# Calculer le nombre d'images à déplacer vers la validation
num_validation_images = int(validation_proportion * len(all_images))

# Sélectionner aléatoirement les images pour la validation
validation_images = random.sample(all_images, num_validation_images)

# Déplacer les images vers le répertoire de validation
for image in validation_images:
    src_path = os.path.join(all_images_dir, image)
    dest_path = os.path.join(validation_dir, image)
    move(src_path, dest_path)

# Déplacer les images restantes vers le répertoire d'entraînement
for image in os.listdir(all_images_dir):
    src_path = os.path.join(all_images_dir, image)
    dest_path = os.path.join(train_dir, image)
    move(src_path, dest_path)

# Afficher le nombre d'images dans chaque répertoire
print(f"Nombre d'images dans le répertoire d'entraînement : {len(os.listdir(train_dir))}")
print(f"Nombre d'images dans le répertoire de validation : {len(os.listdir(validation_dir))}")