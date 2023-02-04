from getpass import getpass
import os
from flask import Flask, request
from flask_restx import Api, Resource, reqparse

from app.models.computer import Computer
import app.password_manager as password_manager
from flask_cors import CORS
from app.db import db

app = Flask(__name__    )
CORS(app)
api = Api(app)

app.config.update(DEBUG=True)

if os.path.exists('password'):
    password = password_manager.read_encrypted_file('password', b'techmanager_pswd')
else:
    password = getpass('Enter the password for the database: ')
    #key = input('Enter the key for the password encryption: ')
    password_manager.write_encrypted_file('password', b'techmanager_pswd', password)

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{password}@localhost:5432/techmanager'

from app import routes

with app.app_context():
    db.init_app(app)
    db.create_all()

api.add_namespace(routes.computer.api, path='/computer')
api.add_namespace(routes.reading.api, path='/reading')
        
api.init_app(routes.bp)
app.register_blueprint(routes.bp)

if __name__ == '__main__':
    app.run(host="0.0.0.0" ,port=9000)