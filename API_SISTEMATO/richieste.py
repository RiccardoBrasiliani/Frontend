import requests

# URL del server

url = 'http://localhost:8000/api/products/'

# Esempio di dati per inviare con le richieste POST e PATCH
data = {'nome': 'Prodotto1', 'prezzo': 10.99, 'marca': 'Marca1'}

# Effettua una richiesta GET per ottenere tutti i prodotti
response = requests.get('http://localhost:8000/api/products')
print('GET Response:', response)

# Effettua una richiesta POST per aggiungere un nuovo prodotto
response = requests.post(url, json=data)
print('POST Response:', response)

# ID del prodotto da modificare o eliminare
product_id = 1

# Effettua una richiesta PATCH per modificare un prodotto
patch_url = f'{url}/{product_id}'
new_data = {'prezzo': 15.99}
response = requests.patch(patch_url, json=new_data)
print('PATCH Response:', response)

# Effettua una richiesta DELETE per eliminare un prodotto
delete_url = f'{url}/{product_id}'
response = requests.delete(delete_url)
print('DELETE Response:', response)