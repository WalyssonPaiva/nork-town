from flask import Blueprint, request
from src.services.customer_service import CustomerService
from src.validators.model_validator import customer_validator
from src.validators.auth_validator import required_auth

customer_routes = Blueprint('customer_service', __name__)

@customer_routes.route('/customers', methods=['GET'])
@required_auth
def get_customers():
    """Endpoint to get all customers
    ---
    parameters:
    - in: header
      name: Authorization
      required: true
      type: string        
    responses:
      200:
        description: A list of customers
        schema:
            id: int
            name: string
            sale_opportunity: boolean
    tags:
        - Customer"""
    return CustomerService().get_all()

@customer_routes.route('/customers/<int:id>', methods=['GET'])
@required_auth
def get_customer(id):
    """Endpoint to get a customer
    ---
    parameters:
    - in: header
      name: Authorization
      required: true
      type: string
    - in: path
      name: id
      required: true
      type: integer
    responses:
      200:
        description: A customer
        schema:
            id: int
            name: string
            sale_opportunity: boolean
    tags:
        - Customer"""
    return CustomerService().get_by_id(id)
    return CustomerService().get_by_id(id)

@customer_routes.route('/customers', methods=['POST'])
@required_auth
def create_customer():
    """Endpoint to create a customer
    ---
    parameters:
    - in: header
      name: Authorization
      required: true
      type: string
    - in: body
      name: body
      schema:
        type: object
        properties:
          name:
            type: string
            required: true
          sale_opportunity:
            type: boolean
            required: false
    responses:
      200:
        description: A customer
        schema:
            id: int
            name: string
            sale_opportunity: boolean
    tags:
        - Customer"""
    data = request.get_json()
    validation = customer_validator(data)
    if "ok" in validation:
        return CustomerService().create(data)
    else:
        return validation, 400

@customer_routes.route('/customers/<int:id>', methods=['PUT'])
@required_auth
def update_customer(id):
    """Endpoint to update a customer
    ---
    parameters:
    - in: header
      name: Authorization
      required: true
      type: string
    - in: path
      name: id
      required: true
      type: integer
    - in: body
      name: body
      schema:
        type: object
        properties:
          name:
            type: string
            required: true
          sale_opportunity:
            type: boolean
            required: false
    responses:
      200:
        description: A customer
        schema:
            id: int
            name: string
            sale_opportunity: boolean
    tags:
        - Customer"""
    data = request.get_json()
    return CustomerService().update(id, data)

@customer_routes.route('/customers/<int:id>', methods=['DELETE'])
@required_auth
def delete_customer(id):
    """Endpoint to delete a customer
    ---
    parameters:
    - in: header
      name: Authorization
      required: true
      type: string
    - in: path
      name: id
      required: true
      type: integer
    responses:
      200:
        description: A customer
        schema:
            id: int
            name: string
            sale_opportunity: boolean
    tags:
        - Customer"""
    return CustomerService().delete(id)