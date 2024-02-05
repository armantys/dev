# __init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os

db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.getenv("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI='mysql+mysqlconnector://ludo:root@192.168.20.61/domotique',  
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY='pomme'
        )
    else:
        app.config.from_mapping(test_config)

    JWTManager(app)

    db.init_app(app)  # Initialisez l'extension Flask-SQLAlchemy ici


    return app