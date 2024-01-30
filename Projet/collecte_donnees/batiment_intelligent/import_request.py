import requests

#PRM : s'obtient sur le compteur linky avedc le bouton + 
# API endpoint
url = "https://www.myelectricaldata.fr/consumption_load_curve/PRM/start/2024-01-12/end/2024-01-19"

# Authorization token
headers = {
    "Authorization": "-vwJb9MnziTiH3X8RhKwSJmDeNrQP2x828fvRfrQdDI="

}

# Perform the GET request
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # If desired, you can parse the JSON response (if the endpoint returns JSON data)
    data = response.json()
    # Print the data
    print(data)
else:
    print(f"Failed to retrieve data: {response.status_code}")