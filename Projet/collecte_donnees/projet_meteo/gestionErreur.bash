#!/bin/bash

# Scénario 1: Problème RASPI
echo "Test du Problème RASPI"
raspi_status=$(raspi-config non_existent_command 2>&1)
if [ $? -ne 0 ]; then
    echo "Erreur: $raspi_status"
fi

# Scénario 2: Problème API Meteo
echo "Test du Problème API Meteo"
meteo_status=$(curl -s https://api.meteo.com/non_existent_endpoint)
if [ $? -ne 0 ]; then
    echo "Erreur: Impossible de se connecter à l'API Meteo"
fi

# Scénario 3: Problème BDD
echo "Test de la connexion à la base de données"
mysql -u 'ludo' -p 'root' -h '192.168.20.61' -e "USE domotique; SELECT 1;" 2>> "$LOG_FILE"
if [ $? -ne 0 ]; then
    log_error "Impossible de se connecter à la base de données"
fi

# Scénario 4: Temps d'exécution trop long
echo "Test du Temps d'exécution trop long"
sleep 15s
echo "Le temps d'exécution a pris trop de temps."

# Ajoutez d'autres scénarios de test au besoin

echo "Fin du script de test d'erreurs"