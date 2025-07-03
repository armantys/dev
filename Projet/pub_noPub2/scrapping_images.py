import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import csv

def download_images(search_terms):
    output_folder = r'datasets\image_folder_logo'
    os.makedirs(output_folder, exist_ok=True)

    # Fichier CSV de sortie
    csv_path = os.path.join(output_folder, 'images_info.csv')
    csv_exists = os.path.isfile(csv_path)

    # Ouvre le fichier CSV en mode ajout
    with open(csv_path, mode='a', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Écrit l'en-tête uniquement si le fichier est nouveau
        if not csv_exists:
            csvwriter.writerow(['filename', 'search_term', 'image_url'])

        for search_term in search_terms:
            url = rf'https://www.google.com/search?q={search_term}&tbm=isch&hl=fr'

            page = requests.get(url).text
            soup = BeautifulSoup(page, 'html.parser')

            thumbnails = []

            for raw_img in soup.find_all('img'):
                link = raw_img.get('src')
                if link and link.startswith("https://"):
                    thumbnails.append(link)

            existing_images = [file for file in os.listdir(output_folder) if file.endswith('.png')]
            latest_index = max([int(file.split('_')[1].split('.')[0]) for file in existing_images], default=-1) + 1

            for i, thumbnail in enumerate(thumbnails):
                img_url = urljoin(url, thumbnail)
                img_data = requests.get(img_url).content

                file_name = f'image_{latest_index + i}_{search_term.replace(" ", "_")}.png'
                img_path = os.path.join(output_folder, file_name)

                with open(img_path, 'wb') as img_file:
                    img_file.write(img_data)

                # Écrire les infos dans le CSV
                csvwriter.writerow([file_name, search_term, img_url])

            print(f"{len(thumbnails)} images appended in the '{output_folder}' folder for search term: '{search_term}' with .png extension.")

search_terms = ['france 3', 'tmc', 'france 4', 'gulli']
download_images(search_terms)
