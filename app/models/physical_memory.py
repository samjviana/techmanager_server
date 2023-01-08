import json
from app.db import db
from app.models.base_model import BaseModel

class PhysicalMemory(BaseModel):
    capacity = db.Column(db.Float)
    ram_id = db.Column(db.Integer, db.ForeignKey('ram.id'))

    @classmethod
    def from_json(cls, json_data):
        physical_memory = cls()

        if json_data.get('id'):
            physical_memory.id = json_data.get('id')
        if json_data.get('uuid'):
            physical_memory.uuid = json_data.get('uuid')
        if json_data.get('added'):
            physical_memory.added = json_data.get('added')
        if json_data.get('updated'):
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