import json
from app.models.super_io import SuperIO
from app.db import db
from app.models.base_model import BaseModel
import uuid
import datetime

class Motherboard(BaseModel):
    name = db.Column(db.String(255))
    super_io = db.relationship('SuperIO', backref='motherboard', uselist=False, lazy=True)
    computer_id = db.Column(db.Integer, db.ForeignKey('computer.id'))

    @classmethod
    def from_json(cls, json_data):
        motherboard = cls()

        if json_data.get('id') != None:
            motherboard.id = json_data.get('id')
        if json_data.get('uuid') != None:
            motherboard.uuid = json_data.get('uuid')
        if json_data.get('added') != None:
            motherboard.added = json_data.get('added')
        if json_data.get('updated') != None:
            motherboard.updated = json_data.get('updated')

        motherboard.name = json_data.get('name')

        super_io = json_data.get('super_io')
        motherboard.super_io = SuperIO.from_json(super_io)

        return motherboard

    def to_json(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'added': self.added.isoformat(),
            'updated': self.updated.isoformat(),
            'name': self.name,
            'super_io': self.super_io.to_json()
        }

    def setToAdd(self):
        self.id = None
        self.uuid = str(uuid.uuid4())
        self.added = datetime.datetime.now()
        self.updated = datetime.datetime.now()

        self.super_io.setToAdd()

    def update(self, old_motherboard, new_motherboard):
        old_motherboard.updated = datetime.datetime.now()
        old_motherboard.name = new_motherboard.name

        old_motherboard.super_io.update(old_motherboard.super_io, new_motherboard.super_io)