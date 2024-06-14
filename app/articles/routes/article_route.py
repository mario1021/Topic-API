from flask import redirect, url_for, request, jsonify
from .. import article_bp
from ..models.article_model import Article
from flask_jwt_extended import jwt_required, get_jwt_identity




#now the one for getting all articles for a user
@article_bp.route('/articles', methods=['GET'], endpoint='get_articles')
@jwt_required()
def get_articles():
    user_id = get_jwt_identity()
    articles = Article.get_by_user_id(user_id)
    return jsonify([article.to_dict() for article in articles]), 200

#now the one for getting them with a filter. the filter is optional, and user_id comes from the token
@article_bp.route('/articles/filter', methods=['GET'], endpoint='get_filtered_articles')
@jwt_required()
def get_filtered_articles():
    user_id = get_jwt_identity()
    source_id = request.args.get('source_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    topic_id = request.args.get('topic_id')
    articles = Article.get_filtered(source_id, user_id, start_date, end_date, topic_id)
    return jsonify([article.to_dict() for article in articles]), 200

@article_bp.route('/articles/<int:id>', methods=['DELETE'], endpoint='delete_article')
@jwt_required()
def delete_article(id):
    article = Article.get_by_id(id)
    if article is None:
        return jsonify({"message": "Article not found"}), 404
    article.delete()
    return jsonify({"message": "Article deleted successfully"}), 200