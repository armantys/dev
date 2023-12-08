from openai import OpenAI
import json
client = OpenAI(api_key="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")

messages = [
    {"role": "system", "content": "fait une réponse sous forme Json  Etape X -> titre de l'étape, description: description de l'étape"}
]

print("Bonjour, n'hésitez pas à me poser des questions ou appuyer sur CTRL+C pour quitter !")

user_input = input("> ")
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    temperature=1
).choices[0].message

messages.append(response)