import os
import pandas as pd
import re

# Chemin du dossier contenant les images
dossier_images = r"C:\Users\ludovic.souquet\Documents\GitHub\ludovic.souquet\Projet\Pub_noPub\pubnopub\nologo\nologo"

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
df = pd.DataFrame({"Image_Name": noms_images})

# Chemin du fichier texte contenant les URLs
chemin_fichier_urls = r"C:\Users\ludovic.souquet\Documents\GitHub\ludovic.souquet\Projet\Pub_noPub\pubnopub\nologo\nologo.txt"

# Lire les URLs à partir du fichier texte
with open(chemin_fichier_urls, 'r') as file:
    urls = [line.strip() for line in file.readlines() if line.strip().startswith("https")]

# Vérifiez si le nombre d'URLs correspond au nombre d'images
if len(urls) != len(noms_images):
    raise ValueError("Le nombre d'URLs ne correspond pas au nombre d'images.")

# Ajouter la colonne des URLs au DataFrame
df["URL"] = urls

# Affichez le DataFrame
print(df)