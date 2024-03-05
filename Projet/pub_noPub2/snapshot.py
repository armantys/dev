import requests
from requests.auth import HTTPDigestAuth

def enregistrer_snapshot(adresse_ip, port, nom_utilisateur, mot_de_passe, duree_salve, nb_images, filename_prefix):
    # URL du flux vidéo de la caméra
    url_flux_video = f'http://{adresse_ip}:{port}/cgi-bin/CGIProxy.fcgi?cmd=snapPicture2&usr={nom_utilisateur}&pwd={mot_de_passe}'

    # Boucle pour enregistrer chaque snapshot
    for i in range(nb_images):
        filename = f"{filename_prefix}_{duree_salve}_{i}.jpg"  # Construire le nom de fichier correctement
        # Récupérer l'image du flux vidéo de la caméra
        response = requests.get(url_flux_video, auth=HTTPDigestAuth(nom_utilisateur, mot_de_passe), stream=True)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Snapshot {i+1}/{nb_images} enregistré avec succès!")
        else:
            print("Impossible de récupérer l'image")
