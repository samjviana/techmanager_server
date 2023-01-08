from datetime import datetime
import uuid
from app.db import db

class BaseModel(db.Model):
    def __init__(self):
        self.uuid = str(uuid.uuid4())
        
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False)
    added = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)