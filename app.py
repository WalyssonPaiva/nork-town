from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from ext import db
import os
from flasgger import Swagger

app = Flask(__name__)

env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
from models import Customer, Car

from routes.customer_routes import customer_routes
from routes.car_routes import car_routes
from routes.user_routes import user_routes
app.register_blueprint(customer_routes)
app.register_blueprint(car_routes)
app.register_blueprint(user_routes)
swagger = Swagger(app)


if __name__ == '__main__':
    app.run()