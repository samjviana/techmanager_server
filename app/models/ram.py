import json
from app.models.physical_memory import PhysicalMemory
from app.db import db
from app.models.base_model import BaseModel
import uuid
import datetime

class RAM(BaseModel):
    total = db.Column(db.Float)
    sensors = db.Column(db.JSON)
    physical_memories = db.relationship('PhysicalMemory', backref='ram', lazy=True)
    computer_id = db.Column(db.Integer, db.ForeignKey('computer.id'))

    @classmethod
    def from_json(cls, json_data):
        ram = cls()

        if json_data.get('id') != None:
            ram.id = json_data.get('id')
        if json_data.get('uuid') != None:
            ram.uuid = json_data.get('uuid')
        if json_data.get('added') != None:
            ram.added = json_data.get('added')
        if json_data.get('updated') != None:
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
        
    def setToAdd(self):
        self.id = None
        self.uuid = str(uuid.uuid4())
        self.added = datetime.datetime.now()
        self.updated = datetime.datetime.now()

        for physical_memory in self.physical_memories:
            physical_memory.setToAdd()


    def update(self, old_ram, new_ram):
        old_ram.updated = datetime.datetime.now()
        old_ram.total = new_ram.total
        old_ram.sensors = new_ram.sensors

        for i in range(len(old_ram.physical_memories)):
            old_ram.physical_memories[i].update(old_ram.physical_memories[i], new_ram.physical_memories[i])