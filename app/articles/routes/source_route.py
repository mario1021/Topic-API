from flask import redirect, url_for, request, jsonify
from .. import article_bp
from ..models.source_model import Source
from flask_jwt_extended import jwt_required, get_jwt_identity


@article_bp.route('/sources', methods=['GET'], endpoint='get_sources')
@jwt_required()
def get_sources():
    user_id = get_jwt_identity()
    sources = Source.get_all()
    return jsonify([source.to_dict() for source in sources]), 200


