#requete_bdd.py

import mysql.connector

def inserer_donnees_meteo(temperature_2m, relative_humidity_2m,nom_lieu):
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

    data_to_insert = (temperature_2m, relative_humidity_2m,nom_lieu)

    cursor.execute(insert_query, data_to_insert)

    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()

def inserer_donnees_raspy(nomcap,temp, humidite, nom_lieu):
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
        INSERT INTO capteurs (nom_capteur,temperature_capteur, humidite_capteur, nom_lieu)
        VALUES (%s,%s, %s, %s)
    """

    data_to_insert = (nomcap, temp, humidite,nom_lieu)

    cursor.execute(insert_query, data_to_insert)

    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()