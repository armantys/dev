import requests


# #----------------------- AJOUT D'UTILISATEUR--------------------------------

# # Définissez l'URL de votre endpoint pour ajouter un utilisateur
# add_user_url = 'http://localhost:5000/api/v1/auth/register'  # Assurez-vous que l'URL est correcte

# # Données de l'utilisateur que vous souhaitez ajouter
# user_data = {'username': 'bernard', 'password': 'dupond'}

# # Envoyez une requête POST pour ajouter l'utilisateur
# response = requests.post(add_user_url, json=user_data)

# # Affichez la réponse du serveur
# print(f"Status Code: {response.status_code}")

# try:
#     # Essayez de convertir la réponse en JSON et l'afficher
#     response_json = response.json()
#     print(response_json)
# except ValueError as e:
#     # En cas d'erreur lors de la conversion JSON
#     print(f"Failed to parse JSON response: {e}")
#     print(f"Raw response: {response.text}")


# #----------------------CONNEXION UTILISATEUR ----------------------------------




# login_url = 'http://localhost:5000/api/v1/auth/login'  # Assurez-vous que l'URL est correcte

# # Données de connexion que vous souhaitez tester
# login_data = {'nom_utilisateur': 'testuser', 'mdp_utilisateur': 'testpassword'}

# # Envoyez une requête POST pour la connexion
# response = requests.post(login_url, json=login_data)

# # Affichez la réponse du serveur
# print(f"Status Code: {response.status_code}")

# try:
#     # Essayez de convertir la réponse en JSON et l'afficher
#     response_json = response.json()
#     print(response_json)
# except ValueError as e:
#     # En cas d'erreur lors de la conversion JSON
#     print(f"Failed to parse JSON response: {e}")
#     print(f"Raw response: {response.text}")


import requests
from werkzeug.security import check_password_hash, generate_password_hash

# URL de connexion
login_url = 'http://localhost:5000/api/v1/auth/login'

# Envoi de la requête POST pour l'authentification et récupération du mot de passe haché
login_data = {'nom_utilisateur': 'bernard', 'mdp_utilisateur': 'dupond'}
login_response = requests.post(login_url, json=login_data)

if login_response.status_code == 200:
    try:
        user_data = login_response.json().get('user')
        refresh_token = user_data.get('refresh')
        access_token = user_data.get('access')

        if refresh_token and access_token:
            print("Connexion réussie!")
            print(f"Refresh Token: {refresh_token}")
            print(f"Access Token: {access_token}")
        else:
            print("Tokens non disponibles dans la réponse.")
    except Exception as e:
        print(f"Exception lors de la lecture de la réponse : {e}")
else:
    print(f"Échec de la connexion. Code de statut: {login_response.status_code}")
    print(f"Réponse du serveur: {login_response.text}")



