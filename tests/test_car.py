import pytest

def test_create_car(client, get_jwt_token):
    response = client.post('/cars', json={
        'color': 'blue',
        'model': 'hatch',
        'owner': 1
    }, headers={'Authorization': f'{get_jwt_token}'})
    assert response.status_code == 201
    assert response.json['color'] == 'blue'
    assert response.json['model'] == 'hatch'
    assert response.json['owner'] == 1

def test_list_cars(client, get_jwt_token):
    response = client.get('/cars', headers={'Authorization': f'{get_jwt_token}'})
    assert response.status_code == 200
    assert len(response.json['cars']) >= 4

def test_get_car(client, get_jwt_token):
    response = client.get('/cars/1', headers={'Authorization': f'{get_jwt_token}'})
    assert response.status_code == 200
    assert response.json['color'] == 'blue'
    assert response.json['model'] == 'hatch'
    assert response.json['owner'] == 1

def test_update_car(client, get_jwt_token):
    response = client.put('/cars/5', json={
        'color': 'yellow',
        'model': 'hatch',
        'owner': 6
    }, headers={'Authorization': f'{get_jwt_token}'})
    assert response.status_code == 200
    assert response.json['color'] == 'yellow'
    assert response.json['model'] == 'hatch'
    assert response.json['owner'] == 6

def test_delete_car(client, get_jwt_token):
    # Delete a car
    response = client.delete('/cars/4', headers={'Authorization': f'{get_jwt_token}'})
    assert response.status_code == 200
    # Check if the car was deleted
    response = client.get('/cars/4', headers={'Authorization': f'{get_jwt_token}'})
    assert response.status_code == 404

def test_update_car_and_old_owner_get_sale_opportunity(client, get_jwt_token):
    # create customer
    response_owner_before_update = client.post('/customers', json={ "name": "John Doe Teste Car" }, headers={'Authorization': f'{get_jwt_token}'})

    response = client.put('/cars/5', json={
        'color': 'yellow',
        'model': 'hatch',
        'owner': response_owner_before_update.json['id']
    }, headers={'Authorization': f'{get_jwt_token}'})
    
    response_owner_after_update = client.get(f"/customers/{response_owner_before_update.json['id']}", headers={'Authorization': f'{get_jwt_token}'})
    # update again to set sleep_opportunity to True again
    response = client.put('/cars/5', json={
        'color': 'yellow',
        'model': 'hatch',
        'owner': 6
    }, headers={'Authorization': f'{get_jwt_token}'})
    response_owner_after_update_again = client.get(f"/customers/{response_owner_before_update.json['id']}", headers={'Authorization': f'{get_jwt_token}'})
    assert response_owner_before_update.json['sale_opportunity'] == True
    assert response_owner_after_update.json['sale_opportunity'] == False
    assert response_owner_after_update_again.json['sale_opportunity'] == True

def test_create_car_and_set_sale_oportunity_to_false(client, get_jwt_token):
    # create customer
    response_owner = client.post('/customers', json={ "name": "John Doe Teste Car" }, headers={'Authorization': f'{get_jwt_token}'})
    response = client.post('/cars', json={
        'color': 'blue',
        'model': 'hatch',
        'owner': response_owner.json['id']
    }, headers={'Authorization': f'{get_jwt_token}'})
    response_owner_after_create = client.get(f"/customers/{response_owner.json['id']}", headers={'Authorization': f'{get_jwt_token}'})
    assert response_owner.json['sale_opportunity'] == True
    assert response_owner_after_create.json['sale_opportunity'] == False

def test_create_more_than_3_cars_to_a_owner(client, get_jwt_token):
    # create customer
    response_owner = client.post('/customers', json={ "name": "John Doe Teste 3 Car" }, headers={'Authorization': f'{get_jwt_token}'})
    response1 = client.post('/cars', json={
        'color': 'blue',
        'model': 'hatch',
        'owner': response_owner.json['id']
    }, headers={'Authorization': f'{get_jwt_token}'})
    response2 = client.post('/cars', json={
        'color': 'blue',
        'model': 'hatch',
        'owner': response_owner.json['id']
    }, headers={'Authorization': f'{get_jwt_token}'})
    response3 = client.post('/cars', json={
        'color': 'blue',
        'model': 'hatch',
        'owner': response_owner.json['id']
    }, headers={'Authorization': f'{get_jwt_token}'})
    response4 = client.post('/cars', json={
        'color': 'blue',
        'model': 'hatch',
        'owner': response_owner.json['id']
    }, headers={'Authorization': f'{get_jwt_token}'})
    assert response4.status_code == 400
    assert response4.json['message'] == 'Customer already has 3 cars'

def test_create_car_with_invalid_owner(client, get_jwt_token):
    response = client.post('/cars', json={
        'color': 'blue',
        'model': 'hatch',
        'owner': 1000
    }, headers={'Authorization': f'{get_jwt_token}'})
    assert response.status_code == 400
    assert response.json['message'] == 'Customer does not exist'