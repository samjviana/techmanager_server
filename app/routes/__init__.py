from flask import Blueprint

bp = Blueprint('routes', __name__)

from app.routes import computer
from app.routes import reading