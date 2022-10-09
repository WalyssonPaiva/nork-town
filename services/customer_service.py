from flask_sqlalchemy import SQLAlchemy
from models import Customer, Car
from services.base_service import BaseService
from loguru import logger
from ext import db

class CustomerService(BaseService):

    def __init__(self):
        super().__init__(Customer)
    
    # delete this customer and all cars associated with this customer
    def delete(self, id):
        try:
            cars = Car.query.filter_by(owner=id).all()
            for car in cars:
                db.session.delete(car)
            customer = Customer.query.get(id)
            db.session.delete(customer)
            db.session.commit()
            return customer.serialize()
        except Exception as e:
            logger.error(e)
            return {'message': 'Error deleting customer'}, 500
       

