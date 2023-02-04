import json
from app.db import db
from app.models.base_model import BaseModel
import uuid
import datetime

class PhysicalMemory(BaseModel):
    capacity = db.Column(db.Float)
    ram_id = db.Column(db.Integer, db.ForeignKey('ram.id'))

    @classmethod
    def from_json(cls, json_data):
        physical_memory = cls()

        if json_data.get('id') != None:
            physical_memory.id = json_data.get('id')
        if json_data.get('uuid') != None:
            physical_memory.uuid = json_data.get('uuid')
        if json_data.get('added') != None:
            physical_memory.added = json_data.get('added')
        if json_data.get('updated') != None:
            physical_memory.updated = json_data.get('updated')

        physical_memory.capacity = json_data.get('capacity')

        return physical_memory

    def to_json(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'added': self.added.isoformat(),
            'updated': self.updated.isoformat(),
            'capacity': self.capacity
        }
        
    def setToAdd(self):
        self.id = None
        self.uuid = str(uuid.uuid4())
        self.added = datetime.datetime.now()
        self.updated = datetime.datetime.now()

    def update(self, old_physical_memory, new_physical_memory):
        old_physical_memory.updated = datetime.datetime.now()
        old_physical_memory.capacity = new_physical_memory.capacity