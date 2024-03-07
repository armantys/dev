import requests
from requests.auth import HTTPDigestAuth
import datetime
import os

def enregistrer_snapshot(adresse_ip, port, nom_utilisateur, mot_de_passe, duree_salve, nb_images_par_salve):
    # Créer le chemin complet du dossier avec la date actuelle
    date_du_jour = datetime.date.today().strftime("%Y-%m-%d")
    snapshot_folder = os.path.join(os.getcwd(), 'snapshot', date_du_jour)
    
    # Assurez-vous que le répertoire datedujour existe. S'il n'existe pas, créez-le.
    if not os.path.exists(snapshot_folder):
        os.makedirs(snapshot_folder)

    # URL du flux vidéo de la caméra
    url_flux_video = f'http://{adresse_ip}:{port}/cgi-bin/CGIProxy.fcgi?cmd=snapPicture2&usr={nom_utilisateur}&pwd={mot_de_passe}'

    # Boucle pour enregistrer chaque snapshot
    for i in range(nb_images_par_salve):
        # Construire le nom de fichier avec un index unique
        filename = f"snapshot_{i+1}.jpg"  # Utilisation de l'index pour générer un nom de fichier unique
        filepath = os.path.join(snapshot_folder, filename)
        # Récupérer l'image du flux vidéo de la caméra
        response = requests.get(url_flux_video, auth=HTTPDigestAuth(nom_utilisateur, mot_de_passe), stream=True)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                f.write(response.content)
            print(f"Snapshot {i+1}/{nb_images_par_salve} enregistré avec succès dans {snapshot_folder}!")

    print(f"Tous les snapshots ont été enregistrés avec succès dans {snapshot_folder}!")
