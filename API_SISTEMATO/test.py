import requests

response = requests.get('http://localhost:8000/products')
print(response.text)  # Stampa il testo della risposta
print(response)  # Stampa il contenuto della risposta come JSON