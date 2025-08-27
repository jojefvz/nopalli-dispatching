from flask import Blueprint

bp = Blueprint('locations', __name__)

from app.locations import routes