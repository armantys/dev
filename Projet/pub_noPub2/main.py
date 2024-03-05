import time  # Importer le module time pour utiliser la fonction sleep
import connexion_firebase
from snapshot import enregistrer_snapshot

latest_acquisition = connexion_firebase.get_latest_acquisition()
latest_application = connexion_firebase.get_latest_application()
latest_model_IA = connexion_firebase.get_latest_model_IA()

# Utilisez les données récupérées selon vos besoins
print("Dernière acquisition:", latest_acquisition)
print("Dernière application:", latest_application)
print("Dernier modèle IA:", latest_model_IA)

def main():
    # Récupérer les données de la dernière acquisition depuis Firebase
    latest_acquisition = connexion_firebase.get_latest_acquisition()

    # Vérifier si les données ont été récupérées avec succès
    if latest_acquisition:
        # Récupérer la durée de la salve et le nombre d'images
        duree_salve, nb_images = latest_acquisition

        adresse_ip = '192.168.20.37'  # Adresse IP de votre caméra IP
        port = 88  # Port par défaut pour la plupart des caméras IP
        nom_utilisateur = 'dev_IA_P3'  # Nom d'utilisateur de la caméra
        mot_de_passe = 'dev_IA_P3'  # Mot de passe de la caméra

        # Calculer le délai entre chaque enregistrement d'image
        delai_entre_images = duree_salve / nb_images

        # Appel de la fonction pour enregistrer chaque snapshot
        for i in range(nb_images):
            # Construire le nom de fichier avec un indice unique
            filename = f'snapshot\snapshot_{duree_salve}_{i}.jpg'
            # Appel de la fonction pour enregistrer un snapshot
            enregistrer_snapshot(adresse_ip, port, nom_utilisateur, mot_de_passe, duree_salve, 1, filename)
            print(f"Snapshot {i+1}/{nb_images} enregistré avec succès!")
            # Attendre le délai entre chaque enregistrement
            time.sleep(delai_entre_images)
    else:
        print("Aucune acquisition trouvée dans la base de données.")

if __name__ == "__main__":
    main()