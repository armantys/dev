import requests

adresse_ip = "192.168.20.95"

def allumer_feu(couleur):
    url = f"http://{adresse_ip}/feu{couleur.capitalize()}"
    response = requests.get(url)
    if response.status_code == 200:
        print(f"Feu allumé en {couleur} !")
    else:
        print(f"Erreur lors de l'allumage du feu en {couleur}. Code d'erreur : {response.status_code}")

def eteindre_feu():
    url = f"http://{adresse_ip}/feuOff"
    response = requests.get(url)
    if response.status_code == 200:
        print("Feu éteint.")
    else:
        print(f"Erreur lors de l'extinction du feu. Code d'erreur : {response.status_code}")

eteindre_feu()

