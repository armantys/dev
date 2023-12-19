#!/bin/bash

LOG_FILE="erreurs.log"

# Créer le fichier log s'il n'existe pas
touch "$LOG_FILE"

# ...

# Exécution du script Python
python3 rasp.py

# Vérifier le code de sortie du script Python
if [ $? -eq 1 ]; then
    echo "Erreur dans le script Python : Données de température et d'humidité non disponibles." >> "$LOG_FILE"
    # Ajoutez ici votre logique spécifique pour l'erreur 1
fi


# Scénario 2: Problème API Meteo
echo "Test du Problème API Meteo"
meteo_status=$(curl -s https://api.meteo.com/non_existent_endpoint)
if [ $2 -ne 0 ]; then
    echo "Erreur: Impossible de se connecter à l'API Meteo"
    exit $ERROR_API_METEO
fi

# Scénario 3: Problème BDD
echo "Test de la connexion à la base de données"
mysql -u 'ludo' -p 'root' -h '192.168.20.61' -e "USE domotique; SELECT 1;" 2>> "$LOG_FILE"
if [ $3 -ne 0 ]; then
    log_error "Impossible de se connecter à la base de données"
    exit $ERROR_BDD
fi

# Scénario 4: Temps d'exécution trop long
echo "Test du Temps d'exécution trop long"
sleep 15s
echo "Le temps d'exécution a pris trop de temps."
exit $ERROR_TEMPS_EXECUTION

# Ajoutez d'autres scénarios de test au besoin

echo "Fin du script de test d'erreurs"