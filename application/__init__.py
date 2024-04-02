from flask import Flask
from os import path
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

VAPID_PRIVATE_KEY = 'yZPxyTnoniaB2jswVDv2V99LUuRSIlDfln-k7p7iFFY'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "0123456789" #Arbritrary key that allows to send flash messages

    #DATABASE SETUP
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    app.app_context().push()

    from .models import Ticket, Trip, WebSubscription
    create_database(app)

    #TO HANDLE REQUESTS FROM EXTERNAL SOURCES
    CORS(app, origins= "*") #origins = "*" IS NOT SECURE CAUSE WE ARE ALLOWING REQUESTS FROM EVERYWHERE
    
    #BLUEPRINTS
    from .factory import factory
    from .notifier import notifier
    from .viewer import viewer
    app.register_blueprint(notifier, url_prefix = '/')
    app.register_blueprint(factory, url_prefix = '/factory')
    app.register_blueprint(viewer, url_prefix = '/view')

    return app

def create_database(app):
    if not path.exists('instance/db.sqlite3'):
        with app.app_context():
            db.create_all()
            print("Created database")