from flask_restx import Namespace, Resource, fields, reqparse
from app.models.computer import Computer
from app.routes import bp
from flask import request

api = Namespace('computer', description='Computadores')

parser = reqparse.RequestParser()

@api.route('/')
class ComputerRootResource(Resource):
    @api.doc(description='Cria um novo computador caso o UUID não tenha sido informado')
    def post(self):
        data = request.get_json()
        if 'uuid' not in data:
            computer = Computer.from_json(data)
            computer.save()
            return {'message': 'Computador criado'}, 201
            
        computer = Computer.query.filter_by(uuid=data['uuid']).first()
        if computer:
            return {'message': 'Computador já existe'}, 409
        else:
            return {'message': 'Computador não existe'}, 404

    @api.doc(description='Retorna todos os computadores')
    def get(self):
        computers = Computer.query.all()
        return [computer.to_json() for computer in computers], 200

@api.route('/<string:uuid>')
class ComputerUUIDResource(Resource):
    @api.doc(description='Retorna um computador pelo UUID')
    def get(self, uuid):
        computer = Computer.query.filter_by(uuid=uuid).first()
        if computer:
            return computer.to_json(), 200
        else:
            return {'message': 'Computador não existe'}, 404