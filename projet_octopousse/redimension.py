import os
import cv2

# Chemins des dossiers d'entrée et de sortie
dossier_entree_couleur = "plan_couleur/"
dossier_entree_noir_blanc = "plan_noir_blanc/"
dossier_sortie_couleur_redimensionne = "plan_couleur_redimensionne/"

# Créer le dossier de sortie s'il n'existe pas
if not os.path.exists(dossier_sortie_couleur_redimensionne):
    os.makedirs(dossier_sortie_couleur_redimensionne)

# Liste des fichiers dans le dossier d'entrée noir et blanc
fichiers_images_noir_blanc = os.listdir(dossier_entree_noir_blanc)

# Parcourir chaque fichier dans le dossier d'entrée noir et blanc
for fichier in fichiers_images_noir_blanc:
    # Chemin complet de l'image noir et blanc
    chemin_image_noir_blanc = os.path.join(dossier_entree_noir_blanc, fichier)
    
    # Charger l'image en noir et blanc pour obtenir ses dimensions
    image_noir_blanc = cv2.imread(chemin_image_noir_blanc, cv2.IMREAD_GRAYSCALE)
    hauteur_noir_blanc, largeur_noir_blanc = image_noir_blanc.shape
    
    # Chemin complet de l'image couleur correspondante
    chemin_image_couleur = os.path.join(dossier_entree_couleur, fichier)
    
    # Charger l'image couleur
    image_couleur = cv2.imread(chemin_image_couleur)
    
    # Redimensionner l'image couleur pour qu'elle ait la même taille que l'image noir et blanc
    image_couleur_redimensionnee = cv2.resize(image_couleur, (largeur_noir_blanc, hauteur_noir_blanc))
    
    # Enregistrer l'image couleur redimensionnée dans le dossier de sortie
    chemin_image_sortie_couleur_redimensionne = os.path.join(dossier_sortie_couleur_redimensionne, fichier)
    cv2.imwrite(chemin_image_sortie_couleur_redimensionne, image_couleur_redimensionnee)
