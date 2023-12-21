#!/bin/bash


echo "Début du script"
# Obtenir la date et l'heure actuelles
current_datetime=$(date +"%Y-%m-%d %H:%M:%S")

LOG_FILE="erreurs.log"

# Crée le fichier log s'il n'existe pas
touch "$LOG_FILE"

# Capturer le code de sortie du script Python
python_exit_code=$?

# Vérifier le code de sortie du script Python
if [ $python_exit_code -eq 1 ]; then
    echo "Erreur dans le script Python : Les données de température et d'humidité ne sont pas disponibles dans la réponse.">> "$LOG_FILE"
    # Ajoutez ici votre logique spécifique pour l'erreur 1
elif [ $python_exit_code -eq 2 ]; then
    echo "Erreur lors de l'exécution du script Python"
    # Ajoutez ici votre logique spécifique pour l'erreur 2
elif [ $python_exit_code -eq 3 ]; then
    echo "Impossible de se connecter à la base de données"
    # Ajoutez ici votre logique spécifique pour l'erreur 3
elif [ $python_exit_code -eq 4 ]; then
    echo "Erreur inattendue dans le script Python"
    # Ajoutez ici votre logique spécifique pour l'erreur 4
fi

echo "Fin du script de gestion des erreurs"
