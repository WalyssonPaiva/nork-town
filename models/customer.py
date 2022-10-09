from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from ext import db

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    sale_opportunity = db.Column(db.Boolean, nullable=False, default=True)
    cars = db.relationship('Car')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Person %r>' % self.name
    
    def serialize(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }





    