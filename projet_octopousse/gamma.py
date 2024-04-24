import os
import cv2
import numpy as np

# Chemins des dossiers d'entrée et de sortie
dossier_entree = "plan_couleur/"
dossier_sortie = "plan_noir_blanc/"

# Créer le dossier de sortie s'il n'existe pas
if not os.path.exists(dossier_sortie):
    os.makedirs(dossier_sortie)

# Liste des fichiers dans le dossier d'entrée
fichiers_images = os.listdir(dossier_entree)

# Paramètres pour la détection de contours
seuil_inf = 30
seuil_sup = 100

# Facteur d'assombrissement des zones noires
facteur_assombrissement = 0.8

# Parcourir chaque fichier dans le dossier d'entrée
for fichier in fichiers_images:
    # Chemin complet de l'image d'entrée
    chemin_image_entree = os.path.join(dossier_entree, fichier)
    
    # Charger l'image en couleur
    image_couleur = cv2.imread(chemin_image_entree)
    
    # Vérifier si l'image est correctement chargée
    if image_couleur is not None:
        # Redimensionner l'image tout en conservant le ratio d'aspect
        largeur, hauteur = image_couleur.shape[1], image_couleur.shape[0]
        nouvelle_largeur, nouvelle_hauteur = largeur, hauteur
        if largeur > 1920 or hauteur > 1440:
            ratio_largeur = 1920 / largeur
            ratio_hauteur = 1440 / hauteur
            ratio_redimensionnement = min(ratio_largeur, ratio_hauteur)
            nouvelle_largeur = int(largeur * ratio_redimensionnement)
            nouvelle_hauteur = int(hauteur * ratio_redimensionnement)
        image_couleur = cv2.resize(image_couleur, (nouvelle_largeur, nouvelle_hauteur))
        
        # Convertir l'image en noir et blanc
        image_gris = cv2.cvtColor(image_couleur, cv2.COLOR_BGR2GRAY)
        
        # Assombrir les zones noires
        image_gris_assombri = np.where(image_gris == 0, image_gris * facteur_assombrissement, image_gris)
        
        # Convertir l'image en niveaux de gris avec une profondeur de 8 bits non signée
        image_gris_assombri = np.uint8(image_gris_assombri)
        
        # Appliquer un flou gaussien pour réduire le bruit
        image_floue = cv2.GaussianBlur(image_gris_assombri, (5, 5), 0)
        
        # Détection des contours avec Canny
        edges = cv2.Canny(image_floue, seuil_inf, seuil_sup)
        
        # Inverser les couleurs (mise en négatif)
        edges_negatif = cv2.bitwise_not(edges)
        
        # Enregistrer l'image en négatif dans le dossier de sortie
        chemin_image_sortie = os.path.join(dossier_sortie, fichier)
        cv2.imwrite(chemin_image_sortie, edges_negatif)
    else:
        print(f"Impossible de charger l'image : {chemin_image_entree}")
