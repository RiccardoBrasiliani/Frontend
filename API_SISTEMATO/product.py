from connessione import connect
import mysql.connector #importo le librerie 
import json

class Product:

            
    def __init__(self, id, nome, prezzo, marca):
        self.id = id
        self.nome = nome
        self.prezzo = prezzo
        self.marca = marca

    def fetchAll(): #metodo per la fetch all
        try: 
            db_manager = connect("192.168.2.200", 3306, "brasiliani_riccardo", "tentatively.apogees.beatific.", "brasiliani_riccardo_database") 
            conn = db_manager.connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products") #query 
            records = cursor.fetchall()
            conn.close()
            return records
        except mysql.connector.Error as e:
            print("Errore durante la ricerca dei prodotti:", str(e))

    
    def find(id): #metodo per la find 
        try:
            db_manager = connect("192.168.2.200", 3306, "brasiliani_riccardo", "tentatively.apogees.beatific.", "brasiliani_riccardo_database") 
            conn = db_manager.connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products WHERE id = %s", (id,)) #query
            #row = cursor.fetchone()
            product = cursor.fetchone()
            conn.close()
            if product:
                """
                print(row)
                return Product(row[0], row[1], row[2], row[3])
                """
                return product
            else:
                return None
        except mysql.connector.Error as e:
            print("Errore durante la ricerca del prodotto:", str(e))
            

    def create(product_data): #metodo per la create 
        try:
            db_manager = connect("192.168.2.200", 3306, "brasiliani_riccardo", "tentatively.apogees.beatific.", "brasiliani_riccardo_database") 
            conn = db_manager.connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO products (nome, prezzo, marca) VALUES (%s, %s, %s)", (product_data['nome'], product_data['prezzo'], product_data['marca']))
            conn.commit()
            product_id = cursor.lastrowid
            conn.close()
            product_data['id'] = product_id
            return product_data
        except mysql.connector.Error as e:
            print("Errore durante la creazione del prodotto:", str(e))

    def update(product_data): #metodo per la update 
        try:
            db_manager = connect("192.168.2.200", 3306, "brasiliani_riccardo", "tentatively.apogees.beatific.", "brasiliani_riccardo_database") 
            conn = db_manager.connection()
            cursor = conn.cursor()
            bind = (product_data["marca"], product_data["prezzo"], product_data["nome"], product_data["id"])
            cursor.execute("UPDATE products SET marca = %s, prezzo = %s, nome = %s WHERE id = %s", bind)
            conn.commit()
            conn.close()
        except mysql.connector.Error as e:
            print("Errore durante l'aggiornamento del prodotto:", str(e))
    
    def delete(self): #metodo per la delete 
        try:
            db_manager = connect("192.168.2.200", 3306, "brasiliani_riccardo", "tentatively.apogees.beatific.", "brasiliani_riccardo_database") 
            conn = db_manager.connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM products WHERE id = %s", (self.id, )) #query 
            conn.commit()
            conn.close()
        except mysql.connector.Error as e:
            print("Errore durante l'eliminazione del prodotto:", str(e))