# main.py
from connexionBDD import inserer_donnees_meteo, inserer_donnees_raspy, inserer_donnees_comp_api
from api_meteo import obtenir_donnees_meteo, obtenir_donnees_ludo_api
from rasp import obtenir_donnees_raspy
from recup_flo import obtenir_donnees_flo_api
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
        # Obtenir les données de flo
        temperature_flo, humidite_flo, ressentie_flo, pression_flo, vitessevent_flo, directionvent_flo  = obtenir_donnees_flo_api()
        # Obtenir les données de ludo
        temperature_ludo, humidite_ludo = obtenir_donnees_ludo_api()
        
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
            inserer_donnees_comp_api(
                temperature_ludo = temperature_ludo,
                humidite_ludo= humidite_ludo,
                temperature_flo=temperature_flo,
                humidite_flo= humidite_flo,
                ressentie_flo= ressentie_flo,
                pression_flo= pression_flo,
                vitessevent_flo= vitessevent_flo,
                directionvent_flo= directionvent_flo

            )


            print(f"Données météo insérées : Température : {temp_meteo}, Humidité : {humidite_meteo}")
            print(f"Données Raspberry Pi insérées : Température : {temperature_raspy}, Humidité : {humidite_raspy}")
            print(f"Données météo comparaison insérées : Température de ludo : {temperature_ludo}, Humidité de ludo : {humidite_ludo}, Température de flo : {temperature_flo}, humidité de flo : {humidite_flo}, Température ressentie de flo : {ressentie_flo}, pression atmosphérique de flo : {pression_flo}, vitesse du vent de flo : {vitessevent_flo}, direction du vent de flo : {directionvent_flo}")
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