import json
from app.db import db
from app.models.base_model import BaseModel
import uuid
import datetime

class Processor(BaseModel):
    number = db.Column(db.Integer)
    name = db.Column(db.String(255))
    temperature = db.Column(db.Float)
    clock = db.Column(db.Float)
    power = db.Column(db.Float)
    cores = db.Column(db.Integer)
    sensors = db.Column(db.JSON)
    computer_id = db.Column(db.Integer, db.ForeignKey('computer.id'))

    @classmethod
    def from_json(cls, json_data):
        processor = cls()

        if json_data.get('id') != None:
            processor.id = json_data.get('id')
        if json_data.get('uuid') != None:
            processor.uuid = json_data.get('uuid')
        if json_data.get('added') != None:
            processor.added = json_data.get('added')
        if json_data.get('updated') != None:
            processor.updated = json_data.get('updated')

        processor.number = json_data.get('number')
        processor.name = json_data.get('name')
        processor.temperature = json_data.get('temperature')
        processor.clock = json_data.get('clock')
        processor.power = json_data.get('power')
        processor.cores = json_data.get('cores')
        processor.sensors = json_data.get('sensors')

        return processor

    def to_json(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'added': self.added.isoformat(),
            'updated': self.updated.isoformat(),
            'number': self.number,
            'name': self.name,
            'temperature': self.temperature,
            'clock': self.clock,
            'power': self.power,
            'cores': self.cores,
            'sensors': self.sensors
        }
        
    def setToAdd(self):
        self.id = None
        self.uuid = str(uuid.uuid4())
        self.added = datetime.datetime.now()
        self.updated = datetime.datetime.now()

    def update(self, old_processor, new_processor):
        old_processor.updated = datetime.datetime.now()
        old_processor.number = new_processor.number
        old_processor.name = new_processor.name
        old_processor.temperature = new_processor.temperature
        old_processor.clock = new_processor.clock
        old_processor.power = new_processor.power
        old_processor.cores = new_processor.cores
        old_processor.sensors = new_processor.sensors
