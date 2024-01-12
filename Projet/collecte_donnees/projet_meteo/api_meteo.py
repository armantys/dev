# -*- coding: utf-8 -*-

import openmeteo_requests
import requests_cache
from retry_requests import retry
import sys
import subprocess
import mysql.connector

def obtenir_donnees_meteo():
    try:
        cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        openmeteo = openmeteo_requests.Client(session=retry_session)

        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": 47.2488,
            "longitude": 6.0182,
            "current": ["temperature_2m", "relative_humidity_2m"]
        }

        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]

        current = response.Current()
        current_temperature_2m = round(current.Variables(0).Value(), 2)
        current_relative_humidity_2m = current.Variables(1).Value()

    except Exception as e:
        print(f"Erreur lors de l'obtention des données météo : {e}")
        sys.exit(2)
    else:
        return current_temperature_2m, current_relative_humidity_2m
    
def obtenir_donnees_ludo_api():
    # Connexion à la base de données source
    source_db = mysql.connector.connect(
        host="192.168.20.61",
        user="ludo",
        password="root",
        database="domotique"
    )

    # Extraction des données
    source_cursor = source_db.cursor()
    source_cursor.execute("SELECT temperature_donneesMeteo, humidite_donneesMeteo FROM donneesMeteo ORDER BY id_donneesMeteo DESC LIMIT 1")
    
    # Récupérer la première (et unique) ligne résultante
    data_to_insert = source_cursor.fetchone()

    # Fermer le curseur et la connexion
    source_cursor.close()
    source_db.close()

    # Utiliser les données récupérées
    if data_to_insert:
        temperature, humidite = data_to_insert
        print("Température:", temperature)
        print("Humidité:", humidite)
        return temperature, humidite
    else:
        print("Aucune donnée trouvée.")

obtenir_donnees_ludo_api()