import json
from app.db import db
from app.models.base_model import BaseModel

class OperatingSystem(BaseModel):
    name = db.Column(db.String(255))
    version = db.Column(db.String(255))
    build = db.Column(db.String(255))
    manufacturer = db.Column(db.String(255))
    architecture = db.Column(db.String(255))
    serial_key = db.Column(db.String(255))
    serial_number = db.Column(db.String(255))
    status = db.Column(db.String(255))
    install_date = db.Column(db.String(255))
    language = db.Column(db.String(255))
    country = db.Column(db.String(255))
    code_page = db.Column(db.Integer)
    boot_device = db.Column(db.String(255))
    system_path = db.Column(db.String(255))
    install_path = db.Column(db.String(255))
    computer_id = db.Column(db.Integer, db.ForeignKey('computer.id'))

    @classmethod
    def from_json(cls, json_data):
        operating_system = cls()

        if json_data.get('id'):
            operating_system.id = json_data.get('id')
        if json_data.get('uuid'):
            operating_system.uuid = json_data.get('uuid')
        if json_data.get('added'):
            operating_system.added = json_data.get('added')
        if json_data.get('updated'):
            operating_system.updated = json_data.get('updated')

        operating_system.name = json_data.get('name')
        operating_system.version = json_data.get('version')
        operating_system.build = json_data.get('build')
        operating_system.manufacturer = json_data.get('manufacturer')
        operating_system.architecture = json_data.get('architecture')
        operating_system.serial_key = json_data.get('serial_key')
        operating_system.serial_number = json_data.get('serial_number')
        operating_system.status = json_data.get('status')
        operating_system.install_date = json_data.get('install_date')
        operating_system.language = json_data.get('language')
        operating_system.country = json_data.get('country')
        operating_system.code_page = json_data.get('code_page')
        operating_system.boot_device = json_data.get('boot_device')
        operating_system.system_path = json_data.get('system_path')
        operating_system.install_path = json_data.get('install_path')

        return operating_system

    def to_json(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'added': self.added.isoformat(),
            'updated': self.updated.isoformat(),
            'name': self.name,
            'version': self.version,
            'build': self.build,
            'manufacturer': self.manufacturer,
            'architecture': self.architecture,
            'serial_key': self.serial_key,
            'serial_number': self.serial_number,
            'status': self.status,
            'install_date': self.install_date,
            'language': self.language,
            'country': self.country,
            'code_page': self.code_page,
            'boot_device': self.boot_device,
            'system_path': self.system_path,
            'install_path': self.install_path
        }