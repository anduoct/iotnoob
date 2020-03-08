from flask import Blueprint

bp = Blueprint('api', __name__)

# void importing too much
from app.api import ping, tokens, errors, users, blogs