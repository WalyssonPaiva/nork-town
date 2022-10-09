import pytest


def test_create_customer(client, get_jwt_token):
    # Create a new customer
    response = client.post('/customers', json={
        'name': 'John Doe',
    }, headers={'Authorization': f'{get_jwt_token}'})
    assert response.status_code == 201
    assert response.json['name'] == 'John Doe'
    assert response.json['sale_opportunity'] == True

def test_list_customers(client, get_jwt_token):
    # List all customers
    response = client.get('/customers', headers={'Authorization': f'{get_jwt_token}'})
    assert response.status_code == 200
    assert len(response.json['customers']) >= 4

def test_get_customer(client, get_jwt_token):
    # Get a customer by id
    response = client.get('/customers/1', headers={'Authorization': f'{get_jwt_token}'})
    assert response.status_code == 200
    assert response.json['name'] == 'John Doe'

def test_update_customer(client, get_jwt_token):
    # Update a customer by id
    response = client.put('/customers/3', json={
        'name': 'John Doe Updated',
    }, headers={'Authorization': f'{get_jwt_token}'})
    assert response.status_code == 200
    assert response.json['name'] == 'John Doe Updated'

    response_get = client.get('/customers/3', headers={'Authorization': f'{get_jwt_token}'})
    assert response_get.status_code == 200
    assert response_get.json['name'] == 'John Doe Updated'

def test_delete_customer(client, get_jwt_token):
    # Delete a customer by id
    response = client.delete('/customers/4', headers={'Authorization': f'{get_jwt_token}'})
    assert response.status_code == 200

    response_get = client.get('/customers/4', headers={'Authorization': f'{get_jwt_token}'})
    assert response_get.status_code == 404