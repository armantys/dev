
# Demander à l'utilisateur d'entrer du texte
nouveau_texte = input("Entrez du texte à ajouter dans le fichier : ")

# Ouvrir le fichier en mode ajout ('a+')
with open('exemple.txt', 'a+') as fichier:
    
    # Écrire le nouveau texte dans le fichier, en sautant une ligne avant
    fichier.write(nouveau_texte + "\n")