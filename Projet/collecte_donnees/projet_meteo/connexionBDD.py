import mysql.connector
import sys
import subprocess

def inserer_donnees_meteo(temperature, humidite, ville):
    try:
        # Connect to the MySQL database
        conn = mysql.connector.connect(
            host='192.168.20.61',
            user='ludo',
            password='root',
            database='domotique'
        )

        # Create a MySQL cursor
        cursor = conn.cursor()

        # Insert data into the database
        insert_query = """
            INSERT INTO donneesMeteo (temperature_donneesMeteo, humidite_donneesMeteo, nom_lieu)
            VALUES (%s, %s, %s)
        """

        data_to_insert = (temperature, humidite, ville)

        cursor.execute(insert_query, data_to_insert)

        # Commit the transaction
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()

    except SystemExit as e:
        print("Impossible de se connecter à la base de données.")
        subprocess.run(["bash", "gestionErreur.sh", "error_bdd"])
        sys.exit(3)

def inserer_donnees_raspy(nom_raspberry, temperature, humidite, emplacement):
    try:
        # Connect to the MySQL database
        conn = mysql.connector.connect(
            host='192.168.20.61',
            user='ludo',
            password='root',
            database='domotique'
        )

        # Create a MySQL cursor
        cursor = conn.cursor()

        # Insert data into the database
        insert_query = """
            INSERT INTO capteurs (nom_capteur, temperature_capteur, humidite_capteur, nom_lieu)
            VALUES (%s, %s, %s, %s)
        """

        data_to_insert = (nom_raspberry, temperature, humidite, emplacement)

        cursor.execute(insert_query, data_to_insert)

        # Commit the transaction
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()



    except SystemExit as e:
        print(f"Erreur lors de la connexion à la base de données : {e}")
        subprocess.run(["bash", "gestionErreur.sh", "error_bdd"])
        sys.exit(3)

def inserer_donnees_comp_api(temperature_ludo, humidite_ludo, temperature_flo, humidite_flo, ressentie_flo, pression_flo, vitessevent_flo, directionvent_flo):
    try:
        # Connect to the MySQL database
        conn = mysql.connector.connect(
            host='192.168.20.61',
            user='ludo',
            password='root',
            database='domotique'
        )

        # Create a MySQL cursor
        cursor = conn.cursor()

        # Insert data into the database
        insert_query = """
            INSERT INTO comparaison_api (ludo_temperature_api, ludo_humidite_api, flo_temperature_api, flo_humidite_api, flo_ressentie_api, flo_pression_api, flo_vitessevent_api, flo_directionvent_api)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        data_to_insert = (temperature_ludo, humidite_ludo,temperature_flo, humidite_flo,  ressentie_flo,  pression_flo, vitessevent_flo, directionvent_flo)

        cursor.execute(insert_query, data_to_insert)

        # Commit the transaction
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        
    except SystemExit as e:
        print(f"Erreur lors de la connexion à la base de données : {e}")
        subprocess.run(["bash", "gestionErreur.sh", "error_bdd"])
        sys.exit(3)