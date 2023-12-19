import requests
from connexionBDD import inserer_donnees_raspy
import sys  # Importez le module sys pour manipuler le code de sortie

url = "http://192.168.20.183/modulesGrove.php?DHT"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    temperature = data.get("temperature")
    humidite = data.get("humidite")

    if temperature is not None and humidite is not None:
        inserer_donnees_raspy('rasp3', temperature, humidite, 'fenetre_265')
        print(f"Données insérées : Température = {temperature}, Humidité = {humidite}")
    else:
        print("Les données de température et d'humidité ne sont pas disponibles dans la réponse.")
        sys.exit(1)  # Code de sortie 1 pour signaler une erreur
else:
    print(f"Erreur de requête HTTP : {response.status_code}")
    sys.exit(1)  # Code de sortie 1 pour signaler une erreur