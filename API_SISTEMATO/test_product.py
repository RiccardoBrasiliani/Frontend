import pytest
from product import Product

test_product_data={'nome':'ciccio','marca':'pasticcio','prezzo':19099}

def test_create():
    product=Product.create(test_product_data)
    assert product is not None
    assert 'id' in product
    assert product['nome'] == test_product_data['nome']
    assert product['marca'] == test_product_data['marca']
    assert product['prezzo'] == test_product_data['prezzo']

def test_find():
    created_product = Product.create(test_product_data)
    found_product = Product.find(created_product['id'])
    assert found_product is not None

    assert found_product[1] == test_product_data['nome']
    assert found_product[2] == test_product_data['marca']
    assert found_product[3] == test_product_data['prezzo']

def test_update():
    created_product = Product.create(test_product_data)
    updated_product_data = {
        'id': created_product['id'],
        'nome': 'Updated Test Product',
        'prezzo': 20.0,
        'marca': 'Updated Test Brand'
    }
    Product.update(updated_product_data)
    updated_product = Product.find(created_product['id'])
    assert updated_product is not None
    assert updated_product[1] == updated_product_data['nome']
    assert updated_product[2] == updated_product_data['marca']
    assert updated_product[3] == updated_product_data['prezzo']
    

def test_delete():
    created_product = Product.create(test_product_data)
    Product.delete(created_product)
    deleted_product = Product.find(created_product['id'])
    assert deleted_product is None

if __name__ == "__main__":
    pytest.main()