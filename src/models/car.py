from ext import db
from sqlalchemy import inspect
import enum

class Color(enum.Enum):
    YELLOW = 'yellow'
    BLUE = 'blue'
    GRAY = 'gray'

class Model(enum.Enum):
    HATCH = 'hatch'
    SEDAN = 'sedan'
    CONVERTIBLE = 'convertible'

class Car(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.Enum(Color), nullable=False)
    model = db.Column(db.Enum(Model), nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)

    def __init__(self, color, model, owner):
        self.color = color.upper()
        self.model = model.upper()
        self.owner = owner

    def __repr__(self):
        return '<Car %r>' % self.id
    
    def serialize(self):
        for c in inspect(self).mapper.column_attrs:
            if c.key == 'color' and not isinstance(getattr(self, c.key), str):
                setattr(self, c.key, getattr(self, c.key).value)
            if c.key == 'model' and not isinstance(getattr(self, c.key), str):
                setattr(self, c.key, getattr(self, c.key).value)
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }