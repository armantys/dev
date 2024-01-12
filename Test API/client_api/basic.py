import requests

endpoint = "http://httpbin.org"
response = requests.get(endpoint)
print(response.text)