import json
from app.db import db
from app.models.base_model import BaseModel

class SuperIO(BaseModel):
    name = db.Column(db.String(255))
    motherboard_id = db.Column(db.Integer, db.ForeignKey('motherboard.id'))

    @classmethod
    def from_json(cls, json_data):
        super_io = cls()

        if json_data.get('id'):
            super_io.id = json_data.get('id')
        if json_data.get('uuid'):
            super_io.uuid = json_data.get('uuid')
        if json_data.get('added'):
            super_io.added = json_data.get('added')
        if json_data.get('updated'):
            super_io.updated = json_data.get('updated')

        super_io.name = json_data.get('name')

        return super_io

    def to_json(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'added': self.added.isoformat(),
            'updated': self.updated.isoformat(),
            'name': self.name
        }