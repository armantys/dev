import os
from openai import AzureOpenAI
import json
client = AzureOpenAI(
  api_key = os.getenv("12699e8302664cdc9e37e3fd929e3fe4"),  
  api_version = "2023-05-15",
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
)

response = client.chat.completions.create(
    model="gpt-35-turbo", # model = "deployment_name".
    messages=[
        {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
        {"role": "user", "content": "Who were the founders of Microsoft?"}
    ]
)

#print(response)
print(response.model_dump_json(indent=2))
print(response.choices[0].message.content)

mondico = {}
try:
    # Ajouter la réponse au dictionnaire
    mondico[len(mondico) + 1] = {"response": response.content}
    
    # Charger la réponse JSON
    response_json = json.loads(mondico[1]['response'])


    # Initialiser un dictionnaire pour stocker les titres et descriptions de chaque étape
    titres_descriptions = {}

    # Parcourir chaque étape dans response_json
    for etape, infos in response_json.items():
        # Extraire le titre et la description de chaque étape
        titre = infos.get('titre', 'Titre non trouvé')
        description = infos.get('description', 'Description non trouvée')

        # Stocker le titre et la description dans le dictionnaire
        titres_descriptions[etape] = {'titre': titre, 'description': description}

except Exception as e:
    print(f"Erreur lors de l'extraction des données de la réponse : {e}")