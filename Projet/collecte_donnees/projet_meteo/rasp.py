# -*- coding: utf-8 -*-

import requests
import sys
import subprocess

def obtenir_donnees_raspy():
    try:
        url = "http://192.168.20.183/modulesGrove.php?DHT"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            temperature = data.get("temperature")
            humidite = data.get("humidite")

            if temperature is not None and humidite is not None:
                return temperature, humidite
            else:
                print("Les données de température et d'humidité ne sont pas disponibles dans la réponse.")
                subprocess.run(["bash", "gestionErreur.sh", "error_raspy"])
                sys.exit(1)  # Utilisez toujours le code 1 pour les erreurs liées aux données dans le script Python
        else:
            print(f"Erreur de requête HTTP : {response.status_code}")
            sys.exit(2)  # Utilisez un code différent pour les erreurs HTTP

    except Exception as e:
        print(f"Erreur lors de l'obtention des données du Raspberry Pi : {e}")
        subprocess.run(["bash", "gestionErreur.sh", "error_raspy"])
        sys.exit(3)  # Utilisez un code différent pour les autres erreurs

# Exemple d'utilisation
try:
    temperature, humidite = obtenir_donnees_raspy()
    # Faites quelque chose avec les données obtenues

except SystemExit as e:
    print(f"Les données de température et d'humidité ne sont pas disponibles dans la réponse. Code de sortie : {e.code}")
    sys.exit(e.code)