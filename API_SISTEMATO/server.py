import json
from http.server import BaseHTTPRequestHandler, HTTPServer #importo le librerie 
from product import Product
import traceback

class RequestHandler(BaseHTTPRequestHandler):
    
    def _set_response(self, status_code=200, content_type='application/json'):
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', "*")
        self.send_header('Access-Control-Allow-methods', "POST,PUT,DELETE")
        self.send_header('Access-Control-Allow-Headers', "content-type")
        self.end_headers()

    def do_GET(self):
        if self.path == '/products':
            self.get_products()
        elif self.path.startswith('/products/'):
            parts = self.path.split('/')
            product_id = int(parts[2])
            self.get_product(product_id)
        else:
            self.send_error(404, 'Not Found')
            

    def get_products(self):
        records = Product.fetchAll()
        #keys = ["id", "nome", "prezzo", "marca"]
        #products_list = [{key: value for key, value in zip(keys, record)} for record in records]
        json_temp2 = []
        i = 0
        for r in records:
            json_temp = {"type":"products", "id": str(r[0]), "attributes":{"nome": r[1], "marca":r[2], "prezzo":r[3]}}
            json_temp2.append(json_temp)
            #string = json.dumps({"data": {"type":"products", "a":products}}, indent=2)
        json_def = {"data":json_temp2}
        json_def = json.dumps(json_def)
        self._set_response(200)
        self.wfile.write(json_def.encode('utf-8'))



    def get_product(self, product_id):
        product = Product.find(product_id)
        if product is not None:
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header('Access-Control-Allow-Origin', "*")
            self.end_headers()
            jsondata={"data": {"type": "products", "id": product[0], "attributes":{"nome": product[1], "marca":product[2], "prezzo":product[3]}}}
            self.wfile.write(json.dumps(jsondata).encode('utf-8'))
        else:
            self.send_error(404, 'Product Not Found')
            
            

    def do_POST(self):
        if self.path == '/products':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            self.create_product(post_data)
        else:
            self.send_error(404, 'Not Found')

    def create_product(self, post_data):
        try:
            data = json.loads(post_data)
            """
            if 'marca' not in data or 'nome' not in data or 'prezzo' not in data:
                self.send_error(400, 'Bad Request - Incomplete Data')
                return
            """
            new_product = {
                'marca': data["data"]["attributes"]['marca'],
                'nome': data["data"]["attributes"]['nome'],
                'prezzo': data["data"]["attributes"]['prezzo']
            }
            product = Product.create(new_product)
            self._set_response(status_code=201)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            json_p = json.dumps({"data": {"type": "products", "id": product["id"], "attributes":{"nome": product["nome"], "marca":product["marca"], "prezzo":product["prezzo"]}}}, indent=2)
            self.wfile.write(json_p.encode('utf-8'))
        except json.JSONDecodeError as e:
            traceback.print_exception(e)
            self.send_error(400, 'Bad Request - Invalid JSON')
            
            
    def do_DELETE(self):
        if self.path.startswith('/products/'):
            parts = self.path.split('/')
            product_id = int(parts[2])
            row = Product.find(product_id)
            product = Product(row[0], row[1], row[2], row[3])
            if product:
                self.delete_product(product)
            else:
                self.send_error(404, 'Product Not Found')
        else:
            self.send_error(404, 'Not Found')
            

    def delete_product(self, product):
        try:
            product = product.delete()
            self._set_response(status_code=204)  
        except Exception as e:
            traceback.print_exception(e)
            self.send_error(500, f'Internal Server Error: {str(e)}')


    def do_PUT(self):
        if self.path.startswith('/products/'):
            parts = self.path.split('/')
            product_id = int(parts[2])
            product = Product.find(product_id)
            if product:
                self.update_product(product)
            else:
                self.send_error(404, 'Product Not Found')
        else:
            self.send_error(404, 'Not Found')

    def update_product(self, product):
        try:
            parts = self.path.split('/')
            product_id = int(parts[2])
            if self.headers.get('Content-Length') is None:
                return self.send_error(400, 'Bad Request - Empty PATCH Body')
            content_length = int(self.headers['Content-Length'])
            patch_data = self.rfile.read(content_length)
            data = json.loads(patch_data.decode('utf-8'))
            new_product = {'id':product_id, 'marca': data["data"]["attributes"]['marca'], "prezzo": data["data"]["attributes"]["prezzo"], "nome": data["data"]["attributes"]["nome"]}
            product = Product.update(new_product)
            product = Product.find(product_id)
            product = json.dumps({"data": {"type": "products", "id": product[0], "attributes":{"nome": product[1], "marca":product[2], "prezzo":product[3]}}})
            self._set_response(status_code=200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(product.encode('utf-8'))
        except Exception as e:
            traceback.print_exception(e)
            self.send_error(500, f'Internal Server Error: {str(e)}')


    def do_OPTIONS(self):
        self._set_response(status_code=200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS,PUT')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')  # Aggiungi 'Content-Type' qui
        self.end_headers()
        
        
        

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8888):
    server_address = ('0.0.0.0', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()