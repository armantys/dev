import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def download_images(search_terms):
    for search_term in search_terms:
        url = rf'https://www.google.fr/search?sca_esv=601398990&hl=fr&sxsrf=ACQVn0-9hdMGVh-PZ6CVtN4ZY-zDT9oWPQ:1706189726510&q={search_term}&tbm=isch&source=lnms&sa=X&ved=2ahUKEwiSscWE1PiDAxWqQ6QEHcMWC90Q0pQJegQIEhAB&biw=1920&bih=919&dpr=1'

        page = requests.get(url).text
        soup = BeautifulSoup(page, 'html.parser')

        thumbnails = []

        for raw_img in soup.find_all('img'):
            link = raw_img.get('src')

            if link and link.startswith("https://"):
                thumbnails.append(link)

        output_folder = 'image_folder'
        os.makedirs(output_folder, exist_ok=True)

        
        existing_images = [file for file in os.listdir(output_folder) if file.endswith('.png')]
        latest_index = max([int(file.split('_')[1].split('.')[0]) for file in existing_images], default=-1) + 1

        for i, thumbnail in enumerate(thumbnails):
            img_url = urljoin(url, thumbnail)
            img_data = requests.get(img_url).content

            img_path = os.path.join(output_folder, f'image_{latest_index + i}_{search_term.replace(" ", "_")}.png')

            with open(img_path, 'wb') as img_file:
                img_file.write(img_data)

        print(f"{len(thumbnails)} images appended in the '{output_folder}' folder for search term: '{search_term}' with .png extension.")

search_terms = ['logo chaîne française M6', 'logo ABC', 'logo XYZ']
download_images(search_terms)
