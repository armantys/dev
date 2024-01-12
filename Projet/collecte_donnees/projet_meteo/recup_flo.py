import mysql.connector

def obtenir_donnees_flo_api():
    # Connexion à la base de données source
    source_db = mysql.connector.connect(
        host="192.168.20.109",
        user="p3",
        password="p3",
        database="projet_collecte_donnees"
    )

    # Extraction des données
    source_cursor = source_db.cursor()
    source_cursor.execute("SELECT temperature_donnerMeteo, humidite_donnerMeteo, temperature_ressentie_donnerMeteo, pression_atmospherique_donnerMeteo, vitesse_vent_donnerMeteo, direction_vent_donnerMeteo FROM donneesMeteo ORDER BY id_donneeMeteo DESC LIMIT 1")
    
    # Récupérer la première (et unique) ligne résultante
    data_to_insert = source_cursor.fetchone()

    # Fermer le curseur et la connexion
    source_cursor.close()
    source_db.close()

    # Utiliser les données récupérées
    if data_to_insert:
        temperature, humidite, ressentie, pression, vitessevent, directionvent = data_to_insert
        print("Température:", temperature)
        print("Humidité:", humidite)
        print("Température ressentie:", ressentie)
        print("pression atmosphérique:", pression)
        print("Vitesse du vent:", vitessevent)
        print("Direction du vent:", directionvent)
        return temperature, humidite, ressentie, pression, vitessevent, directionvent
    else:
        print("Aucune donnée trouvée.")

obtenir_donnees_flo_api()