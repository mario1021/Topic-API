from flask import Blueprint
article_bp = Blueprint('article', __name__)
from .routes import article_route