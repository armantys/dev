import os
import requests
from urllib.parse import urlparse
from PIL import Image

def clean_filename(filename):
    return ''.join(c if c.isalnum() or c in {'-', '_', '.'} else '_' for c in filename)

def download_images(file_path, output_folder):
    with open(file_path, 'r') as file:
        urls = file.read().splitlines()

    # Crée le sous-dossier s'il n'existe pas
    os.makedirs(output_folder, exist_ok=True)

    for index, url in enumerate(urls, start=1):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                filename = f"image_{index}_{clean_filename(os.path.basename(urlparse(url).path))}"

                filepath = os.path.join(output_folder, filename)
                with open(filepath, 'wb') as img_file:
                    img_file.write(response.content)
                print(f"Téléchargement de {filename} terminé.")

                convert_to_jpg(filepath)
            else:
                print(f"Échec du téléchargement de {url}. Code d'état : {response.status_code}")
        except Exception as e:
            print(f"Erreur lors du téléchargement de {url}: {str(e)}")

def convert_to_jpg(filepath):
    _, extension = os.path.splitext(filepath)
    extension = extension.lower()

    if extension != ".jpg":
        try:
            img = Image.open(filepath)
            jpg_filepath = os.path.splitext(filepath)[0] + ".jpg"
            img.convert('RGB').save(jpg_filepath, 'JPEG')
            print(f"Conversion de {filepath} en {jpg_filepath} terminée.")
            
            os.remove(filepath)
            print(f"Suppression de {filepath}.")
        except Exception as e:
            print(f"Erreur lors de la conversion de {filepath} en JPG: {str(e)}")

if __name__ == "__main__":
    root_folder = "."  # Le dossier racine à partir duquel commencer la recherche
    for file in os.listdir(root_folder):
        if file.lower().endswith('.txt'):
            txt_file_path = os.path.join(root_folder, file)
            output_folder = os.path.join(root_folder, os.path.splitext(file)[0])
            download_images(txt_file_path, output_folder)
