from flask import Flask
from os import path
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

VAPID_PRIVATE_KEY = 'yZPxyTnoniaB2jswVDv2V99LUuRSIlDfln-k7p7iFFY'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "0123456789" #Arbritrary key that allows to send flash messages

    #DATABASE SETUPS

    #TO HANDLE REQUESTS FROM EXTERNAL SOURCES
    CORS(app, origins= "*") #origins = "*" IS NOT SECURE CAUSE WE ARE ALLOWING REQUESTS FROM EVERYWHERE
    
    #BLUEPRINTS
    from .factory import factory
    from .notifier import notifier
    from .viewer import viewer
    app.register_blueprint(notifier, url_prefix = '/')
    app.register_blueprint(factory, url_prefix = '/factory')
    app.register_blueprint(viewer, url_prefix = '/view')

    from .models import Ticket, Trip, WebSubscription

    create_database()

    return app

def create_database(app):
    if not path.exists('instance/db.sqlite3'):
        with app.app_context():
            db.create_all()
            print("Created database")