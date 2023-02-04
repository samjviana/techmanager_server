import json
from flask_sqlalchemy import SQLAlchemy
from app.models.base_model import BaseModel
from app.db import db
import uuid
import datetime

class Storage(BaseModel):
    index = db.Column(db.Integer)
    name = db.Column(db.String(255))
    size = db.Column(db.Float)
    disks = db.Column(db.String(255))
    read = db.Column(db.Float)
    write = db.Column(db.Float)
    sensors = db.Column(db.JSON)
    computer_id = db.Column(db.Integer, db.ForeignKey('computer.id'))

    @classmethod
    def from_json(cls, json_data):
        storage = cls()

        if json_data.get('id') != None:
            storage.id = json_data.get('id')
        if json_data.get('uuid') != None:
            storage.uuid = json_data.get('uuid')
        if json_data.get('added') != None:
            storage.added = json_data.get('added')
        if json_data.get('updated') != None:
            storage.updated = json_data.get('updated')

        storage.index = json_data.get('index')
        storage.name = json_data.get('name')
        storage.size = json_data.get('size')
        storage.disks = json_data.get('disks')
        storage.read = json_data.get('read')
        storage.write = json_data.get('write')
        storage.sensors = json_data.get('sensors')

        return storage

    def to_json(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'added': self.added.isoformat(),
            'updated': self.updated.isoformat(),
            'index': self.index,
            'name': self.name,
            'size': self.size,
            'disks': self.disks,
            'read': self.read,
            'write': self.write,
            'sensors': self.sensors
        }
        
    def setToAdd(self):
        self.id = None
        self.uuid = str(uuid.uuid4())
        self.added = datetime.datetime.now()
        self.updated = datetime.datetime.now()

    def update(self, old_storage, new_storage):
        old_storage.updated = datetime.datetime.now()
        old_storage.index = new_storage.index
        old_storage.name = new_storage.name
        old_storage.size = new_storage.size
        old_storage.disks = new_storage.disks
        old_storage.read = new_storage.read
        old_storage.write = new_storage.write
        old_storage.sensors = new_storage.sensors
