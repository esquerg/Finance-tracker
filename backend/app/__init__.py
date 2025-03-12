from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

db = SQLAlchemy()

def create_app():
    #Create the Flask application instance 
    app = Flask(__name__)

    #Enable CORS to enable Vue to interact with the API 
    CORS(app)

    #Configure the app with settings
    #SQLite database file
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance_tracker.db'
    #Disable tracking modification to reduce overhead
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #Generate a Random Secret Key
    app.config['SECRET_KEY'] = os.urandom(24)

    #Initialize the DB
    from .routes import bp
    db.init_app(app)
    
    #Register the blueprints of the API, that would be the route handling 
    app.register_blueprint(bp, url_prefix='/api')

    return app