import os
import pandas as pd
import re
import imgaug.augmenters as iaa
from skimage import io, transform, img_as_ubyte

# Chemin du dossier contenant les images
dossier_images = r"C:\Users\ludovic.souquet\Documents\GitHub\ludovic.souquet\Projet\Pub_noPub\pubnopub\logo2\normal"

# Obtenez la liste de tous les fichiers dans le dossier
fichiers_images = os.listdir(dossier_images)

# Triez les noms de fichiers numériquement
fichiers_images = sorted(fichiers_images, key=lambda x: [int(num) if num.isdigit() else num for num in re.split('(\d+)', x)])

# Créez une liste de noms d'images en extrayant les noms de fichiers des chemins d'accès
noms_images = [os.path.basename(fichier) for fichier in fichiers_images]

# Créez une liste de chemins d'accès complets aux images
chemins_images = [os.path.join(dossier_images, fichier) for fichier in fichiers_images]

# Vérifiez si le nombre d'URLs correspond au nombre d'images
if len(noms_images) != len(chemins_images):
    raise ValueError("Le nombre d'URLs ne correspond pas au nombre d'images.")

# Créez un DataFrame avec les noms d'images et les chemins d'accès aux images
df = pd.DataFrame({"Image_Name": noms_images, "Image_Path": chemins_images})

# Chemin du fichier texte contenant les URLs
chemin_fichier_urls = r"C:\Users\ludovic.souquet\Documents\GitHub\ludovic.souquet\Projet\Pub_noPub\pubnopub\logo.txt"

# Lire les URLs à partir du fichier texte
with open(chemin_fichier_urls, 'r') as file:
    urls = [line.strip() for line in file.readlines() if line.strip().startswith("https")]

# Vérifiez si le nombre d'URLs correspond au nombre d'images
if len(urls) != len(noms_images):
    raise ValueError("Le nombre d'URLs ne correspond pas au nombre d'images.")

# Ajouter la colonne des URLs au DataFrame
df["URL"] = urls

# Fonction pour augmenter une image
def augmenter_image(image_path):
    image = io.imread(image_path)
    seq = iaa.Sequential([
        iaa.Fliplr(0.5),
        iaa.Affine(rotate=(-10, 10)),
        iaa.GaussianBlur(sigma=(0, 1.0)),
        iaa.Multiply((0.8, 1.2), per_channel=0.2),
        iaa.ContrastNormalization((0.5, 1.5), per_channel=0.2)
    ], random_order=True)

    augmented_image = seq.augment_image(image)

    # Convertir l'image augmentée en mode RGB si elle est en mode RGBA
    if augmented_image.shape[2] == 4:
        augmented_image = augmented_image[:, :, :3]

    # Redimensionner l'image à 100x100 pixels
    augmented_image_resized = transform.resize(augmented_image, (100, 100))

    return augmented_image_resized

# Appliquer l'augmentation et le redimensionnement à chaque image
for index, row in df.iterrows():
    augmented_image = augmenter_image(row["Image_Path"])
    
    # Convertir l'image en valeurs d'entiers non signés 8 bits
    augmented_image_uint8 = img_as_ubyte(augmented_image)
    
    # Sauvegarder l'image augmentée et redimensionnée
    nom_fichier_sortie = f"augmented_resized_{row['Image_Name']}"
    chemin_sortie = os.path.join(r"C:\Users\ludovic.souquet\Documents\GitHub\ludovic.souquet\Projet\Pub_noPub\pubnopub\logo2\augmenter", nom_fichier_sortie)
    io.imsave(chemin_sortie, augmented_image_uint8)

# Affichez le DataFrame
print(df)