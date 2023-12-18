import requests
from connexionBDD import inserer_donnees_raspy

url = "http://192.168.20.183/modulesGrove.php?DHT"  # Remplacez ceci par l'URL réelle de votre script PHP

# Effectuer la requête GET
response = requests.get(url)

# Vérifier si la requête a réussi (code de statut HTTP 200)
if response.status_code == 200:
    # Analyser les données JSON
    data = response.json()

    # Extraire la température et l'humidité des données JSON
    temperature = data.get("temperature")
    humidite = data.get("humidite")

    # Vérifier si les valeurs existent
    if temperature is not None and humidite is not None:
        # Appeler la fonction pour insérer les données dans la base de données
        inserer_donnees_raspy('rasp3',temperature, humidite,'fenetre_265')

        # Afficher les données insérées
        print(f"Données insérées : Température = {temperature}, Humidité = {humidite}")
    else:
        print("Les données de température et d'humidité ne sont pas disponibles dans la réponse.")
else:
    print(f"Erreur de requête HTTP : {response.status_code}")