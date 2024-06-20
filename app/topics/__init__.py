from flask import Blueprint
topic_bp = Blueprint('topics', __name__)
from .routes import topic_route
from .routes import mention_route