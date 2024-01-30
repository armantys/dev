from BDD import connection_BDD
import mysql.connector

def inserer_donnees_meteo():
    try:
        # Obtenir la connexion à la base de données en appelant la fonction connection_BDD
        conn = connection_BDD()
        cursor = conn.cursor()
        
        current_weather_data = (20, 68, 22, 12, 52, 65, 21, 36, 4, 22, 55, 58, 102, 58, 42, 1)
        etat_unites_data = (1, 32, 1)
        releves_maison_data = (23, 2, 2)
        
        cursor.execute("""
        INSERT INTO current_weather (date_heure, current_temperature_2m, current_relative_humidity_2m, current_apparent_temperature, current_is_day, current_precipitation, current_rain, current_showers, current_snowfall, current_weather_code, current_cloud_cover, current_pressure_msl, current_surface_pressure, current_wind_speed_10m, current_wind_direction_10m, current_wind_gusts_10m, id_maison)
        VALUES (CURRENT_TIMESTAMP, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", current_weather_data
        )

        cursor.execute("""
        INSERT INTO etat_unites (date_heure, on_off, temperature_set_point, id_unite)
        VALUES (CURRENT_TIMESTAMP, %s, %s, %s)""", etat_unites_data
        )

        cursor.execute("""
        INSERT INTO releves_maison (date_heure, releve_capteur, id_capteur, id_type_mesure)
        VALUES (CURRENT_TIMESTAMP, %s, %s, %s)""", releves_maison_data
        )

        # Valider les changements et fermer la connexion
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Erreur MySQL: {err}")
    finally:
        # Fermer la connexion dans la clause finally pour s'assurer que cela se produit même en cas d'exception
        if 'conn' in locals() and conn.is_connected():
            conn.close()
            print("Connexion à la base de données fermée.")

        print("Données insérées dans la base de données.")

inserer_donnees_meteo()