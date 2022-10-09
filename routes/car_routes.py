from flask import Blueprint, request
from services.car_service import CarService
from validators.model_validator import car_validator
from validators.auth_validator import required_auth
from loguru import logger

car_routes = Blueprint('car_service', __name__)

@car_routes.route('/cars', methods=['GET'])
@required_auth
def get_cars():
    return CarService().get_all()

@car_routes.route('/cars/<int:id>', methods=['GET'])
@required_auth
def get_car(id):
    logger.info("Getting car with id: " + str(id))
    return CarService().get_by_id(id)

@car_routes.route('/cars', methods=['POST'])
@required_auth
def create_car():
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
    data = request.get_json()
    return CarService().update(id, data)

@car_routes.route('/cars/<int:id>', methods=['DELETE'])
@required_auth
def delete_car(id):
    logger.info("Deleting car with id: " + str(id))
    return CarService().delete(id)