from flask import redirect, url_for, request, jsonify
from .. import topic_bp
from ..models.topic_model import Topic
from ..models.mention_model import Mention
from flask_jwt_extended import jwt_required, get_jwt_identity

#we need just one endpoint, getFiltered, the filter will be by topic_id, start_date, end_date. as usual, start_date and end_date are optional
@topic_bp.route('/mentions/filter', methods=['GET'], endpoint='get_filtered_mentions')
@jwt_required()
def get_filtered_mentions():
    topic_id = request.args.get('topic_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    mentions = Mention.get_filtered(topic_id, start_date, end_date)
    return jsonify([mention.to_dict() for mention in mentions]), 200
