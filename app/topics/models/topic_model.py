from app import db
from datetime import datetime


class Topic(db.Model):

    __tablename__ = 'topics'
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    sentiment_score = db.Column(db.Float, nullable=True)
    sentiment= db.Column(db.String(10), nullable=True)
    trend = db.Column(db.Float, default=0, nullable=False)
    priority = db.Column(db.Float, default=0, nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)
    articles= db.relationship('Article', secondary='topic_articles', backref=db.backref('topics', lazy='dynamic'))
    mentions= db.relationship('Mention', backref='topic', lazy='dynamic')
    

    def __init__(self, title, user_id):
        self.title = title
        self.user_id = user_id

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    @staticmethod
    def get_by_id(id):
        return Topic.query.get(id)
    
    @staticmethod
    def get_by_user_id(user_id):
        return Topic.query.filter_by(user_id=user_id).all()
    
    @staticmethod
    def get_all():
        return Topic.query.all()
    
    @staticmethod
    def delete_by_id(id):
        topic = Topic.get_by_id(id)
        if topic is not None:
            topic.delete()
            return True
        return False
    
topic_articles= db.Table('topic_articles',
                        db.Column('id', db.BigInteger, primary_key=True),
    db.Column('topic_id', db.BigInteger, db.ForeignKey('topics.id'), nullable=False),
    db.Column('article_id', db.BigInteger, db.ForeignKey('articles.id'), nullable=False),
)