from pushbullet import Pushbullet

# Remplacez 'YOUR_API_KEY' par votre jeton API Pushbullet
pb = Pushbullet('o.oYQhOS109R2euC9Vj9Z2sShM2sByFmFe')

# Remplacez 'Titre' par le titre de votre notification
# Remplacez 'Corps du message' par le corps de votre notification
push = pb.push_note('erreur', 'vous avez une erreur')