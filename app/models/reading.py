import datetime
import json
import uuid

from flask import jsonify
from app.models.ram import RAM
from app.models.motherboard import Motherboard
from app.models.operating_system import OperatingSystem
from app.models.processor import Processor
from app.models.gpu import GPU
from app.models.storage import Storage
from app.db import db
from app.models.base_model import BaseModel
from sqlalchemy.dialects.postgresql import ARRAY
import uuid

class Reading(BaseModel):
    computer_uuid = db.Column(db.String(255), nullable=False)
    storages = db.Column(db.JSON)
    ram = db.Column(db.JSON)
    processors = db.Column(db.JSON)
    gpus = db.Column(db.JSON)

    @classmethod
    def from_json(cls, json_data):
        reading = cls()

        if json_data.get('id') != None:
            reading.id = json_data.get('id')
        if json_data.get('uuid') != None:
            reading.uuid = json_data.get('uuid')
        if json_data.get('added') != None:
            reading.added = json_data.get('added')
        if json_data.get('updated') != None:
            reading.updated = json_data.get('updated')

        reading.computer_uuid = json_data.get('computer_uuid')
        reading.storages = json_data.get('storages')
        reading.ram = json_data.get('ram')
        reading.processors = json_data.get('processors')
        reading.gpus = json_data.get('gpus')
        
        return reading

    def to_json(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'added': self.added.isoformat(),
            'updated': self.updated.isoformat(),
            'computer_uuid': self.computer_uuid,
            'storages': self.storages,
            'ram': self.ram,
            'processors': self.processors,
            'gpus': self.gpus
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def setToAdd(self):
        self.id = None
        self.uuid = str(uuid.uuid4())
        self.added = datetime.datetime.now()
        self.updated = datetime.datetime.now()

    def get_reading(self, reading_type):
        if reading_type == 'ram':
            return {'ram': json.loads(self.ram)}
        elif reading_type == 'storages':
            return {'storages': json.loads(self.storages)}
        elif reading_type == 'processors':
            return {'processors': json.loads(self.processors)}
        elif reading_type == 'gpus':
            return {'gpus': json.loads(self.gpus)}
        else:
            return None
        