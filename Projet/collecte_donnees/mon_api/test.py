import requests

url = "http://192.168.20.55:5000/capteur/570"  # Remplacez 1 par l'ID du capteur que vous souhaitez supprimer
response = requests.delete(url)

if response.status_code == 200:
    print("Capteur supprimé avec succès!")
else:
    print(f"La requête a échoué avec le code d'état {response.status_code}")