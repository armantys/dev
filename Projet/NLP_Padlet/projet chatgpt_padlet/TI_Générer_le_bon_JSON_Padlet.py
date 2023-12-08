import requests
from input import response_json
# Remplacez 'YOUR_API_KEY' par votre clé d'API Padlet
API_KEY = 'pdltp_a659b4e7996157e7b5fc15a1799ca9d00c310060e541f2d9452c7353508755f3ffe9c1'
BOARD_ID = 'v96n8l3kxjayrndm'

# Endpoint pour créer un post sur Padlet
PADLET_API_ENDPOINT = f"https://api.padlet.dev/v1/boards/{BOARD_ID}/posts"

# ID de la section Padlet sur laquelle vous souhaitez créer le post
SECTION_ID = 'sec_ke9KqzbV8RwdqYQG'
for etape, infos in response_json.items():
    # Données du post que vous souhaitez créer
    payload = {
        "data": {
            "type": "post",
            "attributes": {
                "content": {
                    "subject": f"{etape}: {infos['titre']}",
                    "body": infos['description'],
                
                },
                "color": "red"
            },
            "relationships": {
                "section": {
                    "data": {
                        "id": SECTION_ID
                    }
                }
            }
        }
    }


    headers = {
        "accept": "application/vnd.api+json",
        "content-type": "application/vnd.api+json",
        "X-Api-Key": API_KEY
    }

    # Envoi de la requête POST pour créer le post
    response = requests.post(PADLET_API_ENDPOINT, json=payload, headers=headers)

# Vérification de la réponse
if response.status_code == 200:
    print('Post créé avec succès!')
    print('ID du post:', response.json().get('id'))
else:
    print('Erreur lors de la création du post. Code de statut:', response.status_code)
    print('Message d\'erreur:', response.text)