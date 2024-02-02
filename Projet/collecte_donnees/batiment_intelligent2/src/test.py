import requests


# #----------------------- AJOUT D'UTILISATEUR--------------------------------

# # # Définissez l'URL de votre endpoint pour ajouter un utilisateur
# # add_user_url = 'http://localhost:5000/api/v1/auth/register'  # Assurez-vous que l'URL est correcte

# # # Données de l'utilisateur que vous souhaitez ajouter
# # user_data = {'username': 'testuser', 'password': 'testpassword'}

# # # Envoyez une requête POST pour ajouter l'utilisateur
# # response = requests.post(add_user_url, json=user_data)

# # # Affichez la réponse du serveur
# # print(f"Status Code: {response.status_code}")

# # try:
# #     # Essayez de convertir la réponse en JSON et l'afficher
# #     response_json = response.json()
# #     print(response_json)
# # except ValueError as e:
# #     # En cas d'erreur lors de la conversion JSON
# #     print(f"Failed to parse JSON response: {e}")
#     # print(f"Raw response: {response.text}")


# #----------------------CONNEXION UTILISATEUR ----------------------------------




login_url = 'http://localhost:5000/api/v1/auth/login'  # Assurez-vous que l'URL est correcte

# Données de connexion que vous souhaitez tester
login_data = {'nom_utilisateur': 'jeremy', 'mdp_utilisateur': 'ranguis'}

# Envoyez une requête POST pour la connexion
response = requests.post(login_url, json=login_data)

# Affichez la réponse du serveur
print(f"Status Code: {response.status_code}")

try:
    # Essayez de convertir la réponse en JSON et l'afficher
    response_json = response.json()
    print(response_json)
except ValueError as e:
    # En cas d'erreur lors de la conversion JSON
    print(f"Failed to parse JSON response: {e}")
    print(f"Raw response: {response.text}")

