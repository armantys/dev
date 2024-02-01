import os
import requests
from urllib.parse import urlparse
from PIL import Image
import shutil

def download_images(file_path, output_folder):
    with open(file_path, 'r') as file:
        urls = file.read().splitlines()

    # Supprime le dossier existant s'il existe
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)

    # Crée le sous-dossier
    os.makedirs(output_folder, exist_ok=True)

    # Liste des URLs à supprimer du fichier .txt
    urls_to_remove = []

    for index, url in enumerate(urls, start=1):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                _, file_extension = os.path.splitext(urlparse(url).path)

                # Ignore les fichiers SVG, WEBP, et GIF
                if file_extension.lower() in ['.svg', '.webp', '.gif']:
                    print(f"Ignoré le fichier {file_extension.upper()} {url}")
                    urls_to_remove.append(url)
                    continue

                # Utilise les parties significatives de l'URL pour générer un nom de fichier
                filename = f"{index}.{file_extension.lstrip('.')}"

                # Si le fichier n'a pas d'extension, essaye de la déduire avec Pillow
                if not file_extension:
                    # Utilise Pillow pour ouvrir l'image et obtenir le format
                    image = Image.open(BytesIO(response.content))
                    image_type = image.format.lower()
                    filename = f"{index}.{image_type}"

                filepath = os.path.join(output_folder, filename)
                with open(filepath, 'wb') as img_file:
                    img_file.write(response.content)
                print(f"Téléchargement de {filename} terminé.")
            else:
                print(f"Échec du téléchargement de {url}. Code d'état : {response.status_code}")
                # Ajoute l'URL à la liste des URLs à supprimer
                urls_to_remove.append(url)
        except Exception as e:
            print(f"Erreur lors du téléchargement de {url}: {str(e)}")
            # Ajoute l'URL à la liste des URLs à supprimer
            urls_to_remove.append(url)

    # Supprime les URLs du fichier .txt
    with open(file_path, 'w') as file:
        for line in urls:
            if line not in urls_to_remove:
                file.write(line + '\n')

def clean_txt_file(file_path):
    # Lit le contenu du fichier .txt
    with open(file_path, 'r') as file:
        urls = file.read().splitlines()

    # Supprime les URLs avec les extensions .webp, .svg et .gif
    cleaned_urls = [url for url in urls if not url.lower().endswith(('.webp', '.svg', '.gif'))]

    # Écrit le nouveau contenu dans le fichier .txt
    with open(file_path, 'w') as file:
        file.write('\n'.join(cleaned_urls))

if __name__ == "__main__":
    root_folder = "."  # Le dossier racine à partir duquel commencer la recherche
    for file in os.listdir(root_folder):
        if file.lower().endswith('.txt'):
            txt_file_path = os.path.join(root_folder, file)
            output_folder = os.path.join(root_folder, os.path.splitext(file)[0])
            clean_txt_file(txt_file_path)
            download_images(txt_file_path, output_folder)
