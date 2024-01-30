import pandas as pd
from BDD import connection_BDD
import mysql.connector
import matplotlib.pyplot as plt

def fetch_data(query):
    try:
        # Obtenir la connexion à la base de données en appelant la fonction connection_BDD
        conn = connection_BDD()
        cursor = conn.cursor()

        cursor.execute(query)

        # Récupérer les résultats de la requête dans un DataFrame
        df = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])

        # Fermer le curseur et la connexion
        cursor.close()
        conn.close()

        return df
    except mysql.connector.Error as err:
        print(f"Erreur MySQL: {err}")
        return None

# Exécuter les requêtes et récupérer les résultats dans des DataFrames
df_etat_unites = fetch_data("SELECT * FROM etat_unites WHERE id_unite = 1;")
df_releves_maison = fetch_data("SELECT * FROM releves_maison WHERE id_type_mesure = 2;")
df_releves_capteur = fetch_data("""
    SELECT capteurs.*
    FROM capteurs
    JOIN zones ON capteurs.id_capteur = zones.id_capteur
    JOIN unites ON zones.id_unite = unites.id_unite
    WHERE unites.thermostat_unite = 'numérique';
""")

# Fusionner les DataFrames en un seul
merged_df = pd.concat([df_etat_unites, df_releves_maison, df_releves_capteur], ignore_index=True)

# Afficher le DataFrame final
print(merged_df)

# Tracer une courbe temporelle pour la température, par exemple
plt.plot(merged_df['date_heure'], merged_df['temperature_set_point'])
plt.title('Évolution de la température au fil du temps')
plt.xlabel('Date et heure')
plt.ylabel('Température')
plt.show()