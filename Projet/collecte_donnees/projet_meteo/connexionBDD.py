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