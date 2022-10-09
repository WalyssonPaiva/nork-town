from flask_sqlalchemy import SQLAlchemy
from loguru import logger
from ext import db

class BaseService:

    def __init__(self, model):
        self.model = model
    
    def create(self, data):
        try:
            new_model = self.model(**data)
            db.session.add(new_model)
            db.session.commit()
            return new_model.serialize(), 201
        except Exception as e:
            logger.error(e)
            return {'message': 'Error creating model'}, 500
    
    def get_all(self):
        try:
            models = self.model.query.all()
            return {self.model.__tablename__: [model.serialize() for model in models]}
        except Exception as e:
            logger.error(e)
            return {'message': 'Error getting models'}, 500

    def get_by_id(self, id):
        try:
            model = self.model.query.get(id)
            if model:
                return model.serialize()
            return {'message': 'Model not found'}, 404
        except Exception as e:
            logger.error(e)
            return {'message': 'Error getting model'}, 500
    
    def update(self, id, data):
        try:
            model = self.model.query.get(id)
            for key, value in data.items():
                setattr(model, key, value)
            db.session.merge(model)
            db.session.commit()
            return model.serialize()
        except Exception as e:
            logger.error(e)
            return {'message': 'Error updating model'}, 500
    
    def delete(self, id):
        try:
            model = self.model.query.get(id)
            db.session.delete(model)
            db.session.commit()
            return model.serialize()
        except Exception as e:
            logger.error(e)
            return {'message': 'Error deleting model'}, 500