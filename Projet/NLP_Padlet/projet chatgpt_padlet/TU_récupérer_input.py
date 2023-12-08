user_input = input("> ")
if len(user_input)< 10:
    print("votre message est trop court")
    user_input = input("> ")
elif user_input.isdigit():
    print("Veuillez entrer du texte, pas uniquement des chiffres.")
    user_input = input("> ")
else:
    #suite du code chat GPT