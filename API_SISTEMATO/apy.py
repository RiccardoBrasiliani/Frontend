from flask import Flask, jsonify, request, url_for
from product import Product

app = Flask(__name__)

# Rotta per elencare tutti i prodotti
@app.route('/products', methods=['GET'])#fatto
def get_products():
    records = Product.fetchAll()
    # Converti i record in una lista di dizionari
    keys = ["id", "nome", "prezzo", "marca"]
    products_list = []
    for record in records:
        product_dict = {key: value for key, value in zip(keys, record)}
        products_list.append(product_dict)
    
    # Converti la lista di dizionari in JSON utilizzando jsonify e restituiscila come risposta
    return jsonify({'data': products_list})


# Rotta per ottenere un singolo prodotto
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    record = Product.find(product_id)
    keys = ["id", "nome", "prezzo", "marca"]
    product_dict = {key: value for key, value in zip(keys, record)}
    return jsonify(product_dict)



@app.route('/products', methods=['POST'])
def create_product():
    if not request.json:
        return jsonify({'error': 'La richiesta deve essere in formato JSON'}), 400

    if 'nome' not in request.json or 'prezzo' not in request.json or 'marca' not in request.json:
        return jsonify({'error': 'Dati incompleti'}), 400

    new_product = {
        'nome': request.json['nome'],
        'prezzo': request.json['prezzo'],
        'marca': request.json['marca']
    }
    
    product = Product.create(new_product)

    return jsonify(product), 201 


if __name__ == '__main__':
    app.run(debug=True)