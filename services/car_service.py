from flask_sqlalchemy import SQLAlchemy
from models import Car, Customer
from services.base_service import BaseService
from ext import db

class CarService(BaseService):
    
        def __init__(self):
            super().__init__(Car)
        
        def create(self, data):
            data = self.upper_color_and_model(data)
            if data['owner'] is not None:
                customer = Customer.query.get(data['owner'])
                if customer is not None:
                    cars = Car.query.filter_by(owner=customer.id).all()
                    if len(cars) < 3:
                        if customer.sale_opportunity:
                            customer.sale_opportunity = False
                            db.session.merge(customer)
                            db.session.commit()
                        return super().create(data)
                    else:
                        return {'message': 'Customer already has 3 cars'}, 400
                else:
                    return {'message': 'Customer does not exist'}, 400
            else:
                return super().create(data)
        
        def update(self, id, data):
            data = self.upper_color_and_model(data)
            if data['owner'] is not None:
                customer = Customer.query.get(data['owner'])
                if customer is not None:
                    cars = Car.query.filter_by(owner=customer.id).all()
                    if len(cars) <= 2:
                        car = Car.query.get(id)
                        old_owner = Customer.query.get(car.owner)
                        if old_owner is not None and old_owner.id != customer.id:
                            cars = Car.query.filter_by(owner=old_owner.id).all()
                            if len(cars) == 1:
                                old_owner.sale_opportunity = True
                                db.session.merge(old_owner)
                                db.session.commit()
                        if customer.sale_opportunity:
                            customer.sale_opportunity = False
                            db.session.merge(customer)
                            db.session.commit()
                        return super().update(id, data)
                    else:
                        return {'message': 'Customer already has 3 cars'}, 400
                else:
                    return {'message': 'Customer does not exist'}, 400
            else:
                return super().update(id, data)

        def delete(self, id):
            car = Car.query.get(id)
            owner = Customer.query.get(car.owner)
            if owner is not None:
                cars = Car.query.filter_by(owner=owner.id).all()
                if len(cars) == 1:
                    owner.sale_opportunity = True
                    db.session.merge(owner)
                    db.session.commit()
            return super().delete(id)
        
        def upper_color_and_model(self, data):
            data['color'] = data['color'].upper()
            data['model'] = data['model'].upper()
            return data
        