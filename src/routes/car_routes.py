from flask import Blueprint, request
from src.services.car_service import CarService
from src.validators.model_validator import car_validator
from src.validators.auth_validator import required_auth
from loguru import logger

car_routes = Blueprint('car_service', __name__)

@car_routes.route('/cars', methods=['GET'])
@required_auth
def get_cars():
    """Endpoint to get all cars
    ---
    parameters:
    - in: header
      name: Authorization
      required: true
      type: string        
    responses:
      200:
        description: A list of cars
        schema:
            id: int
            color: string
            model: string
            owner: int
    tags:
        - Car"""
    return CarService().get_all()

@car_routes.route('/cars/<int:id>', methods=['GET'])
@required_auth
def get_car(id):
    """Endpoint to get a car
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
        description: A car
        schema:
            id: int
            color: string
            model: string
            owner: int
    tags:
        - Car"""
    return CarService().get_by_id(id)

@car_routes.route('/cars', methods=['POST'])
@required_auth
def create_car():
    """Endpoint to create a car
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
          color:
            type: string
          model:
            type: string
          owner:
            type: integer
    responses:
      200:
        description: A car
        schema:
            id: int
            color: string
            model: string
            owner: int
    tags:
        - Car"""
    data = request.get_json()
    validation = car_validator(data)
    if "ok" in validation:
        logger.info("Creating car with data: " + str(data))
        return CarService().create(data)
    else:
        logger.info("Error creating car with data due to missing fields: " + str(data))
        return validation, 400

@car_routes.route('/cars/<int:id>', methods=['PUT'])
@required_auth
def update_car(id):
    """Endpoint to update a car
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
          color:
            type: string
          model:
            type: string
          owner:
            type: integer
    responses:
      200:
        description: A car
        schema:
            id: int
            color: string
            model: string
            owner: int
    tags:
        - Car"""
    data = request.get_json()
    return CarService().update(id, data)

@car_routes.route('/cars/<int:id>', methods=['DELETE'])
@required_auth
def delete_car(id):
    """Endpoint to delete a car
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
        description: A car
        schema:
            id: int
            color: string
            model: string
            owner: int
    tags:
        - Car"""
    return CarService().delete(id)