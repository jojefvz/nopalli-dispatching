from flask import Blueprint

bp = Blueprint('dispatches', __name__)

from app.dispatches import routes