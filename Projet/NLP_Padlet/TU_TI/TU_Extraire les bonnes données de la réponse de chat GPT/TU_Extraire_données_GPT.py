#permet de mettre la réponse sous forme de json
messages = [
    {"role": "system", "content": "fait une réponse sous forme Json  Etape X -> titre de l'étape, description: description de l'étape"}
]

mondico = {}

# Ajouter la réponse au dictionnaire
mondico[len(mondico) + 1] = {"response": response.content}
    
# Charger la réponse JSON
response_json = json.loads(mondico[1]['response'])