from openai import OpenAI
import json
client = OpenAI(api_key="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")

messages = [
    {"role": "system", "content": "fait une réponse sous forme Json  Etape X -> titre de l'étape, description: description de l'étape"}
]

print("Bonjour, n'hésitez pas à me poser des questions ou appuyer sur CTRL+C pour quitter !")

mondico = {}


user_input = input("> ")
messages.append({"role": "user", "content": user_input})

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    temperature=1
).choices[0].message

messages.append(response)

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