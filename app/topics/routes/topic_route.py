from flask import redirect, url_for, request, jsonify
from .. import topic_bp
from ..models.topic_model import Topic
from flask_jwt_extended import jwt_required, get_jwt_identity



@topic_bp.route('/topics', methods=['POST'], endpoint='create_topic')
@jwt_required()
def create_topic():
    data=request.get_json()
    title = data.get('title')
    user_id = get_jwt_identity()
    print(user_id)
    topic = Topic(title, user_id)
    topic.save()
    return jsonify({"message": "Topic created successfully"}), 201

#now the one for getting all topics for a user
@topic_bp.route('/topics', methods=['GET'], endpoint='get_topics')
@jwt_required()
def get_topics():
    user_id = get_jwt_identity()
    topics = Topic.get_by_user_id(user_id)
    return jsonify([topic.to_dict() for topic in topics]), 200

#now the one for getting topics filtered by title
@topic_bp.route('/topics/filter', methods=['GET'], endpoint='get_filtered_topics')
@jwt_required()
def get_filtered_topics():
    user_id = get_jwt_identity()
    title = request.args.get('title')
    if title is None:
        topics = Topic.get_by_user_id(user_id)
        return jsonify([topic.to_dict() for topic in topics]), 200
    topics = Topic.get_filtered(title, user_id)
    return jsonify([topic.to_dict() for topic in topics]), 200

#the one for get by Id
@topic_bp.route('/topics/<int:id>', methods=['GET'], endpoint='get_topic_by_id')
@jwt_required()
def get_topic_by_id(id):
    user_id = get_jwt_identity()
    topic = Topic.get_by_id(id)
    if topic is None:
        return jsonify({"message": "Topic not found"}), 404
    if topic.user_id != user_id:
        return jsonify({"message": "You are not authorized to view this topic"}), 403
    return jsonify(topic.to_dict()), 200

@topic_bp.route('/topics/<int:id>', methods=['DELETE'], endpoint='delete_topic')
@jwt_required()
def delete_topic(id):
    user_id = get_jwt_identity()
    topic = Topic.get_by_id(id)
    if topic is None:
        return jsonify({"message": "Topic not found"}), 404
    if topic.user_id != user_id:
        return jsonify({"message": "You are not authorized to delete this topic"}), 403
    topic.delete()
    return jsonify({"message": "Topic deleted successfully"}), 200

