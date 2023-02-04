from flask_restx import Namespace, Resource, fields, reqparse
from app.models.reading import Reading
from app.routes import bp
from flask import request
import json
import datetime
from sqlalchemy import and_

api = Namespace('reading', description='Leituras')

parser = reqparse.RequestParser()

@api.route('/<string:computer_uuid>/<string:reading_type>')
class ReadingByTypeResource(Resource):
    @api.doc(description='Retorna a leitura de um computador pelo UUID e tipo de leitura')
    def get(self, computer_uuid, reading_type):
        reading = Reading.query.filter_by(computer_uuid=computer_uuid).order_by(Reading.id.desc()).first()
        if reading:
            reading_to_return = reading.get_reading(reading_type)[reading_type]
            return reading_to_return, 200
        else:
            return {'message': 'Leitura não existe'}, 404

@api.route('/<string:computer_uuid>')
class ReadingByDateResource(Resource):
    @api.doc(description='Retorna a leitura de um computador pelo UUID e tipo de leitura')
    def get(self, computer_uuid):
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")   
        if start_date and end_date:
            start_date = datetime.datetime.strptime(start_date, '%d-%m-%Y %H:%M:%S')
            end_date = datetime.datetime.strptime(end_date, '%d-%m-%Y %H:%M:%S')
            readings = Reading.query.filter(Reading.added >= start_date, Reading.added <= end_date, Reading.computer_uuid == computer_uuid).order_by(Reading.id.desc()).all()
            if readings:
                readings = [reading.to_json() for reading in readings]
                return readings, 200
            else:
                return {'message': 'Leitura não existe'}, 404
        else:
            return {'message': 'Leitura não aexiste'}, 404

@api.route('/<string:computer_uuid>/<string:reading_type>/<int:index>')
class ReadingByIndexResource(Resource):
    @api.doc(description='Retorna a leitura de um computador pelo UUID e tipo de leitura e índice')
    def get(self, computer_uuid, reading_type, index):
        reading = Reading.query.filter_by(computer_uuid=computer_uuid).order_by(Reading.id.desc()).first()
        if reading:
            reading_values = reading.get_reading(reading_type)
            reading_to_return = reading_values[reading_type][index]
            return reading_to_return, 200
        else:
            return {'message': 'Leitura não existe'}, 404
