import requests
from generate_token import get_stored_token

def make_request(endpoint):
    stored_token = get_stored_token()

    if stored_token:
        headers = {'Authorization': f'Bearer {stored_token}'}
        response = requests.get(endpoint, headers=headers)

        if response.status_code == 200:
            data = response.json()
            print(data)
        else:
            print(f"Erreur de requête : {response.status_code}")
            print(response.text)  # Affichez le contenu de la réponse pour obtenir des détails supplémentaires
    else:
        print("Token non trouvé. Veuillez vous connecter.")

if __name__ == "__main__":
    # Remplacez l'URL de l'API par la vôtre
    endpoint_url = "http://127.0.0.1:5000/api/data"
    
    make_request(endpoint_url)