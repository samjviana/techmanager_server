import json
from flask import jsonify
from app.db import db
from app.models.base_model import BaseModel
from psycopg2.extras import Json
import uuid
import datetime

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

        if json_data.get('id') != None:
            gpu.id = json_data.get('id')
        if json_data.get('uuid') != None:
            gpu.uuid = json_data.get('uuid')
        if json_data.get('added') != None:
            gpu.added = json_data.get('added')
        if json_data.get('updated') != None:
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

    def setToAdd(self):
        self.id = None
        self.uuid = str(uuid.uuid4())
        self.added = datetime.datetime.now()
        self.updated = datetime.datetime.now()

    def update(self, old_gpu, new_gpu):
        old_gpu.updated = datetime.datetime.now()
        old_gpu.number = new_gpu.number
        old_gpu.name = new_gpu.name
        old_gpu.temperature = new_gpu.temperature
        old_gpu.core_clock = new_gpu.core_clock
        old_gpu.memory_clock = new_gpu.memory_clock
        old_gpu.power = new_gpu.power
        old_gpu.sensors = new_gpu.sensors
