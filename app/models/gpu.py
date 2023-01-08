import json
from flask import jsonify
from app.db import db
from app.models.base_model import BaseModel
from psycopg2.extras import Json

class GPU(BaseModel):
    number = db.Column(db.Integer)
    name = db.Column(db.String(255))
    temperature = db.Column(db.Float)
    core_clock = db.Column(db.Float)
    memory_clock = db.Column(db.Float)
    power = db.Column(db.Float)
    sensors = db.Column(db.JSON)
    computer_id = db.Column(db.Integer, db.ForeignKey('computer.id'))

    @classmethod
    def from_json(cls, json_data):
        gpu = cls()

        if json_data.get('id'):
            gpu.id = json_data.get('id')
        if json_data.get('uuid'):
            gpu.uuid = json_data.get('uuid')
        if json_data.get('added'):
            gpu.added = json_data.get('added')
        if json_data.get('updated'):
            gpu.updated = json_data.get('updated')

        gpu.number = json_data.get('number')
        gpu.name = json_data.get('name')
        gpu.temperature = json_data.get('temperature')
        gpu.core_clock = json_data.get('core_clock')
        gpu.memory_clock = json_data.get('memory_clock')
        gpu.power = json_data.get('power')
        gpu.sensors = json_data.get('sensors')

        return gpu

    def to_json(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'added': self.added.isoformat(),
            'updated': self.updated.isoformat(),
            'number': self.number,
            'name': self.name,
            'temperature': self.temperature,
            'core_clock': self.core_clock,
            'memory_clock': self.memory_clock,
            'power': self.power,
            'sensors': self.sensors
        }