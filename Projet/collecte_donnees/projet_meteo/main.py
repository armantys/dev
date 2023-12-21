# main.py
from connexionBDD import inserer_donnees_meteo, inserer_donnees_raspy
from api_meteo import obtenir_donnees_meteo
from rasp import obtenir_donnees_raspy
import sys
import logging

# Ajoutez ces lignes pour configurer le logging dans le script Python
logging.basicConfig(filename='erreurs.log', level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Initialisation de la variable de contrôle d'erreur
    erreur = False

    try:
        # Obtenir les données météo
        temp_meteo, humidite_meteo = obtenir_donnees_meteo()
        # Obtenir les données du Raspberry Pi
        temperature_raspy, humidite_raspy = obtenir_donnees_raspy()
        
        if temp_meteo is not None and humidite_meteo is not None and temperature_raspy is not None and humidite_raspy is not None:
            # Utiliser la fonction d'insertion avec des valeurs par défaut pour les paramètres manquants
            inserer_donnees_meteo(
                temperature=temp_meteo,
                humidite=humidite_meteo,
                ville='besançon'
            )
            inserer_donnees_raspy(
                nom_raspberry='rasp3',
                temperature=temperature_raspy,
                humidite=humidite_raspy,
                emplacement='fenetre_265'
            )
            print(f"Données météo insérées : Température : {temp_meteo}, Humidité : {humidite_meteo}")
            print(f"Données Raspberry Pi insérées : Température : {temperature_raspy}, Humidité : {humidite_raspy}")
        else:
            print("Les données de température et d'humidité ne sont pas disponibles dans la réponse.")
            erreur = True
            
    except SystemExit as e:
        print(f"Erreur lors de l'obtention ou de l'insertion des données : {e}")
        erreur = True
        logger.error(f"Erreur lors de l'obtention ou de l'insertion des données : {e}")
        sys.exit(2)  # Utilisez toujours le code 2 pour les erreurs dans le script Python

    # Si une erreur s'est produite lors de l'obtention ou de l'insertion des données, afficher un message
    if erreur:
        print("Une ou plusieurs erreurs sont survenues. Aucune donnée n'a été insérée dans la base de données.")
        logger.error("Une ou plusieurs erreurs sont survenues. Aucune donnée n'a été insérée dans la base de données.")
        sys.exit(1)
    else:
        print("Aucune erreur détectée. Les données seront insérées dans la base de données.")
        # Ajoutez ici d'autres opérations si nécessaire

if __name__ == "__main__":
    main()