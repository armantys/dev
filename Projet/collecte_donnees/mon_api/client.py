import requests

base_url = 'http://192.168.20.61:5000'

# Obtenir la liste des tables disponibles
tables_url = f'{base_url}/tables'
tables_response = requests.get(tables_url)
tables = tables_response.json()['tables']
print('Tables disponibles:', tables)

# Supprimer toutes les données de la table "capteurs"
table_name = 'patate'
delete_url = f'{base_url}/table/{table_name}'
delete_response = requests.delete(delete_url)
print(delete_response.json())