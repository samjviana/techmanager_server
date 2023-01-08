import json
from app.models.physical_memory import PhysicalMemory
from app.db import db
from app.models.base_model import BaseModel

class RAM(BaseModel):
    total = db.Column(db.Float)
    sensors = db.Column(db.JSON)
    physical_memories = db.relationship('PhysicalMemory', backref='ram', lazy=True)
    computer_id = db.Column(db.Integer, db.ForeignKey('computer.id'))

    @classmethod
    def from_json(cls, json_data):
        ram = cls()

        if json_data.get('id'):
            ram.id = json_data.get('id')
        if json_data.get('uuid'):
            ram.uuid = json_data.get('uuid')
        if json_data.get('added'):
            ram.added = json_data.get('added')
        if json_data.get('updated'):
            ram.updated = json_data.get('updated')

        ram.total = json_data.get('total')
        ram.sensors = json_data.get('sensors')

        physical_memories = json_data.get('physical_memories')

        ram.physical_memories = [PhysicalMemory.from_json(physical_memory) for physical_memory in physical_memories]

        return ram

    def to_json(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'added': self.added.isoformat(),
            'updated': self.updated.isoformat(),
            'total': self.total,
            'sensors': self.sensors,
            'physical_memories': [physical_memory.to_json() for physical_memory in self.physical_memories]
        }
