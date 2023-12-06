import os
import nbformat
from pprint import pprint
# Dictionnaire pour stocker les résultats
valeurs_variables = {}
resultats = {}


def listdirectory(path, variables_a_chercher):
    # Liste des fichiers avec l'extension .ipynb dans le répertoire
    fichiers_ipynb = [fichier for fichier in os.listdir(path) if fichier.endswith('.ipynb')]

    for nom_fichier in fichiers_ipynb:
        nom = nom_fichier.split(".")[0]

        # Vérifier si le fichier n'est pas "script.ipynb"
        if nom_fichier != "script.ipynb":
            with open(os.path.join(path, nom_fichier), 'r', encoding='utf-8') as fichier:
                contenu = nbformat.read(fichier, as_version=4)

                for cellule in contenu['cells'][:-2]:
                    if cellule['cell_type'] == 'code':
                        # Extraire le contenu du code dans la cellule
                        code = cellule['source']

                        for variable in variables_a_chercher:
                            if variable in code:
                                exec(code)  # Exécute le code de la cellule
                                valeurs_variables[variable] = locals()[variable]

                # Créer le dictionnaire si l'élève n'existe pas
                if nom not in resultats:
                    resultats[nom] = {}

                # Ajouter les notes à l'élève et à l'exercice spécifiés
                for exercice, note in valeurs_variables.items():
                    #met dans le dictionnaire resultats le nom et dedans l'exercice étant la clé et note étant la valeur 
                    resultats[nom][exercice] = note
                    # moyenne_eleve= sum(note)/len(notes)
                    # print(moyenne_eleve)

    # Afficher le dictionnaire résultant
    pprint(resultats)

# Noms des variables à rechercher
notes = ["note00", "note01", "note1", "note2", "note3", "note4", "note5"]

# Chemin vers le répertoire contenant les fichiers .ipynb
chemin = r"C:\Users\ludovic.souquet\Documents\GitHub\ludovic.souquet\piscine_python\Evaluation python classroom ciel 28092923\Evaluation python classroom ciel 28092923\\"

listdirectory(chemin, notes)


totaux = [7, 12, 10, 17, 14, 12]
ponderations = [2, 2, 4, 2, 4, 1]


def moyenne():
    # Initialisation de la somme des moyennes par élève
    somme_moyenne_par_eleve = 0
    
    # Boucle à travers chaque élève et ses résultats
    for eleve, valeur in resultats.items():
        # Liste pour stocker les notes pondérées pour chaque exercice
        exo = []
        # Initialisation de la somme pondérée des notes
        note_ponderee_somme = 0 
        
        # Boucle à travers chaque exercice et note de l'élève
        for exercice, note in valeur.items():
            # Extraction du numéro de l'exercice
            exer = [*exercice.replace("note", "")]
            
            # Vérification de la longueur du numéro de l'exercice
            if len(exer) > 1:
                try:
                    # Ajout de la note à la liste correspondante à l'exercice
                    exo[int(exer[0])] += note
                except:
                    # Si la liste n'existe pas encore, la créer et ajouter la note
                    exo.append(note)
            else:
                # Si l'exercice n'a qu'un chiffre, ajouter simplement la note
                exo.append(note)

        # Calcul de la note pondérée pour chaque exercice
        for note, ponderation, total in zip(exo, ponderations, totaux):
            note_ponderee_somme += ponderation * (note * 20) / total
            
        # Calcul de la moyenne pondérée par élève
        moyenne_par_eleve = note_ponderee_somme / sum(ponderations)
        # Ajout de la moyenne de l'élève à la somme totale
        somme_moyenne_par_eleve += moyenne_par_eleve
    
    # Calcul de la moyenne de classe
    moyenne_de_classe = somme_moyenne_par_eleve / len(resultats)
    
    # Affichage de la moyenne générale de la classe arrondie à deux décimales
    print("la moyenne general est : ", round(moyenne_de_classe, 2))

# Appel de la fonction moyenne
moyenne()



def moyenne_par_exercice():
    # Initialiser un dictionnaire pour stocker les notes par exercice
    notes_par_exercice = {}

    # Parcourir chaque élève
    for eleve, valeur in resultats.items():
        # Parcourir chaque exercice pour cet élève
        for exercice, note in valeur.items():
            # Remplacer "note" par "exercice" dans le nom de l'exercice
            exer = exercice.replace("note", "exercice ")

            # Ajouter la note à la liste correspondante dans le dictionnaire
            if exer not in notes_par_exercice:
                notes_par_exercice[exer] = []    
            notes_par_exercice[exer].append(note)
    
    # Calculer la moyenne pour chaque exercice
    moyenne_par_exercice = {exer: sum(notes) / len(notes) for exer, notes in notes_par_exercice.items()}
    pprint(moyenne_par_exercice)
    # Afficher la moyenne par exercice
    for exer, moyenne in moyenne_par_exercice.items():
        print(f"la moyenne de l'{exer} est : {round(moyenne,2)}")

# Appel de la fonction
moyenne_par_exercice()