from src.models import Customer, Car

# validate if a dict contains all the required values of a model
def base_validator(model, data):
    for column in model.__table__.columns:
        if column.name not in data and not column.nullable and not column.primary_key and not column.default:
            return {'error': f'{column.name} is required'}
    return {"ok": True}

def customer_validator(data):
    return base_validator(Customer, data)

def car_validator(data):
    return base_validator(Car, data)


