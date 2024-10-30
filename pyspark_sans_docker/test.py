import requests

# Exemple de caractéristiques pour le test
features = [0.0, 1.0, 3.0, 1.0, 4.0, 0.0, 0.0, 1.0, 7.0, 1.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 4.0]

# URL de l'API
url = "http://localhost:5000/predict"

# Envoyer la requête POST avec les caractéristiques en JSON
response = requests.post(url, json={"features": features})

# Afficher le statut et le contenu brut de la réponse
print("Statut de la réponse :", response.status_code)
print("Contenu de la réponse :", response.text)

# Si la réponse est correcte, afficher le JSON
if response.status_code == 200:
    print("Réponse JSON :", response.json())
else:
    print("Erreur lors de l'appel à l'API")
