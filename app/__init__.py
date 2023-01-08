from flask import Flask
from app.db import db
import os 
import app.password_manager as password_manager
from getpass import getpass
from flask_restx import Api, Swagger

from app.models.computer import Computer

def create_app():
    app = Flask(__name__)

    swagger = Swagger(app)
    api = Api(app, docs=swagger)

    app.config['SWAGGER_UI_JSONEDITOR'] = True
    app.config['SWAGGER_UI_DOC_EXPANSION'] = 'list'
    app.config['SWAGGER_URL'] = '/api/docs/'

    app.config.update(DEBUG=True)

    if os.path.exists('password'):
        password = password_manager.read_encrypted_file('password', b'techmanager_pswd')
    else:
        password = getpass('Enter the password for the database: ')
        #key = input('Enter the key for the password encryption: ')
        password_manager.write_encrypted_file('password', b'techmanager_pswd', password)

    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{password}@localhost:5432/techmanager'

    with app.app_context():
        db.init_app(app)
        db.create_all()

    from app import routes

    api.init_app(routes.bp)
    app.register_blueprint(routes.bp)

    return app, api

