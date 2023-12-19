import openmeteo_requests
from connexionBDD import inserer_donnees_meteo
import requests_cache
from retry_requests import retry
import sys

def obtenir_donnees_meteo():
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 47.2488,
        "longitude": 6.0182,
        "current": ["temperature_2m", "relative_humidity_2m"]
    }

    try:
        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]

        current = response.Current()
        current_temperature_2m = round(current.Variables(0).Value(), 2)
        current_relative_humidity_2m = current.Variables(1).Value()

        # Utiliser la fonction d'insertion
        inserer_donnees_meteo(current_temperature_2m, current_relative_humidity_2m, 'besançon')

        print(f"Current temperature_2m {current_temperature_2m}")
        print(f"Current relative_humidity_2m {current_relative_humidity_2m}")

    except Exception as e:
        print(f"Erreur lors de l'obtention des données météo : {e}")
        sys.exit(2)