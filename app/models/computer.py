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
from app.models.reading import Reading

class Computer(BaseModel):
    name = db.Column(db.String(255), nullable=False)
    part_of_domain = db.Column(db.Boolean)
    domain = db.Column(db.String(255))
    work_group = db.Column(db.String(255))
    dns_name = db.Column(db.String(255))
    domain_role = db.Column(db.String(255))
    current_user = db.Column(db.String(255))
    computer_type = db.Column(db.String(255))
    manufacturer = db.Column(db.String(255))
    model = db.Column(db.String(255))
    power_state = db.Column(db.String(255))
    owner_contact = db.Column(db.String(255))
    owner_name = db.Column(db.String(255))
    support_contact = db.Column(db.String(255))
    system_type = db.Column(db.String(255))
    thermal_state = db.Column(db.String(255))
    status = db.Column(db.Boolean, nullable=False)
    sensors = db.Column(db.JSON)
    installed_softwares = db.Column(ARRAY(db.String(255)))
    storages = db.relationship('Storage', backref='computer', lazy=True)
    ram = db.relationship('RAM', backref='computer', uselist=False, lazy=True)
    processors = db.relationship('Processor', backref='computer', lazy=True)
    gpus = db.relationship('GPU', backref='computer', lazy=True)
    motherboard = db.relationship('Motherboard', backref='computer', uselist=False, lazy=True)
    operating_system = db.relationship('OperatingSystem', backref='computer', uselist=False, lazy=True)

    @classmethod
    def from_json(cls, json_data):
        computer = cls()

        if json_data.get('id') != None:
            computer.id = json_data.get('id')
        if json_data.get('uuid') != None:
            computer.uuid = json_data.get('uuid')
        if json_data.get('added') != None:
            computer.added = json_data.get('added')
        if json_data.get('updated') != None:
            computer.updated = json_data.get('updated')

        computer.name = json_data.get('name')
        computer.part_of_domain = json_data.get('part_of_domain')
        computer.domain = json_data.get('domain')
        computer.work_group = json_data.get('work_group')
        computer.dns_name = json_data.get('dns_name')
        computer.domain_role = json_data.get('domain_role')
        computer.current_user = json_data.get('current_user')
        computer.computer_type = json_data.get('computer_type')
        computer.manufacturer = json_data.get('manufacturer')
        computer.model = json_data.get('model')
        computer.power_state = json_data.get('power_state')
        computer.owner_contact = json_data.get('owner_contact')
        computer.owner_name = json_data.get('owner_name')
        computer.support_contact = json_data.get('support_contact')
        computer.system_type = json_data.get('system_type')
        computer.thermal_state = json_data.get('thermal_state')
        computer.status = json_data.get('status')
        computer.sensors = json_data.get('sensors')
        computer.installed_softwares = json_data.get('installed_softwares')

        storages = json_data.get('storages', [])
        ram = json_data.get('ram')
        processors = json_data.get('processors', [])
        gpus = json_data.get('gpus', [])    
        motherboard = json_data.get('motherboard')
        operating_system = json_data.get('operating_system')

        computer.storages = [Storage.from_json(storage) for storage in storages]
        computer.ram = RAM.from_json(ram)
        computer.processors = [Processor.from_json(processor) for processor in processors]
        computer.gpus = [GPU.from_json(gpu) for gpu in gpus]
        computer.motherboard = Motherboard.from_json(motherboard)
        computer.operating_system = OperatingSystem.from_json(operating_system)
        
        return computer

    def to_json(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'added': self.added.isoformat(),
            'updated': self.updated.isoformat(),
            'name': self.name,
            'part_of_domain': self.part_of_domain,
            'domain': self.domain,
            'work_group': self.work_group,
            'dns_name': self.dns_name,
            'domain_role': self.domain_role,
            'current_user': self.current_user,
            'computer_type': self.computer_type,
            'manufacturer': self.manufacturer,
            'model': self.model,
            'power_state': self.power_state,
            'owner_contact': self.owner_contact,
            'owner_name': self.owner_name,
            'support_contact': self.support_contact,
            'system_type': self.system_type,
            'thermal_state': self.thermal_state,
            'status': self.status,
            'sensors': self.sensors,
            'installed_softwares': self.installed_softwares,
            'storages': [storage.to_json() for storage in self.storages],
            'ram': self.ram.to_json(),
            'processors': [processor.to_json() for processor in self.processors],
            'gpus': [gpu.to_json() for gpu in self.gpus],
            'motherboard': self.motherboard.to_json(),
            'operating_system': self.operating_system.to_json()
        }

    def save(self):
        self.status = True
        db.session.add(self)
        db.session.commit()

    def update(self, old_computer, new_computer):
        new_computer = Computer.from_json(new_computer)
        
        old_computer.name = new_computer.name
        old_computer.part_of_domain = new_computer.part_of_domain
        old_computer.domain = new_computer.domain
        old_computer.work_group = new_computer.work_group
        old_computer.dns_name = new_computer.dns_name
        old_computer.domain_role = new_computer.domain_role
        old_computer.current_user = new_computer.current_user
        old_computer.computer_type = new_computer.computer_type
        old_computer.manufacturer = new_computer.manufacturer
        old_computer.model = new_computer.model
        old_computer.power_state = new_computer.power_state
        old_computer.owner_contact = new_computer.owner_contact
        old_computer.owner_name = new_computer.owner_name
        old_computer.support_contact = new_computer.support_contact
        old_computer.system_type = new_computer.system_type
        old_computer.thermal_state = new_computer.thermal_state
        old_computer.status = new_computer.status
        old_computer.sensors = new_computer.sensors
        old_computer.installed_softwares = new_computer.installed_softwares
        old_computer.updated = datetime.datetime.now()
        old_computer.status = True

        for i in range(len(old_computer.storages)):
            old_computer.storages[i].update(old_computer.storages[i], new_computer.storages[i])
        old_computer.ram.update(old_computer.ram, new_computer.ram)
        for i in range(len(old_computer.processors)):
            old_computer.processors[i].update(old_computer.processors[i], new_computer.processors[i])
        for i in range(len(old_computer.gpus)):
            old_computer.gpus[i].update(old_computer.gpus[i], new_computer.gpus[i])
        old_computer.motherboard.update(old_computer.motherboard, new_computer.motherboard)
        old_computer.operating_system.update(old_computer.operating_system, new_computer.operating_system)

        db.session.commit()

    def setToAdd(self):
        self.id = None
        self.uuid = str(uuid.uuid4())
        self.added = datetime.datetime.now()
        self.updated = datetime.datetime.now()

        for storage in self.storages:
            storage.setToAdd()
        self.ram.setToAdd()
        for processor in self.processors:
            processor.setToAdd()
        for gpu in self.gpus:
            gpu.setToAdd()
        self.motherboard.setToAdd()
        self.operating_system.setToAdd()
        
    def save_reading(self):
        reading = Reading()
        reading.setToAdd()
        reading.computer_uuid = self.uuid
        
        storage_readings = []
        for storage in self.storages:
            storage_sensors = storage.sensors
            storage_sensors['uuid'] = storage.uuid
            storage_readings.append(storage_sensors)
        reading.storages = json.dumps(storage_readings)

        reading.ram = json.dumps(self.ram.sensors)

        processor_readings = []
        for processor in self.processors:
            processor.sensors['uuid'] = processor.uuid
            processor.sensors['added'] = processor.added.isoformat()
            processor_readings.append(processor.sensors)
        reading.processors = json.dumps(processor_readings)

        gpu_readings = []
        for gpu in self.gpus:
            gpu_readings.append(gpu.sensors)
        reading.gpus = json.dumps(gpu_readings)

        reading.save()
        