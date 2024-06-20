from app import db
from datetime import datetime
from ...topics.models.mention_model import Mention


class Topic(db.Model):

    __tablename__ = 'topics'
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    pos_score = db.Column(db.Float, nullable=True)
    neg_score = db.Column(db.Float, nullable=True)
    neu_score = db.Column(db.Float, nullable=True)
    sentiment= db.Column(db.String(10), nullable=True)
    trend = db.Column(db.Float, default=0, nullable=False)
    priority = db.Column(db.Float, default=0, nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)
    total_mentions = db.Column(db.Integer, default=0, nullable=False)
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

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'pos_score': self.pos_score,
            'neg_score': self.neg_score,
            'neu_score': self.neu_score,
            'sentiment': self.sentiment,
            'trend': self.trend,
            'priority': self.priority,
            'user_id': self.user_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'total_mentions': self.total_mentions,
            'mentions': [mention.to_dict() for mention in self.mentions]
        }


    @staticmethod
    def get_by_id(id):
        return Topic.query.get(id)
    
    @staticmethod
    def get_by_user_id(user_id):
        return Topic.query.filter_by(user_id=user_id).all()
    
    @staticmethod
    def get_filtered(title, user_id):
        #the title is optional, and we filter it using like, not an exact match
        if title is None:
            return Topic.query.filter_by(user_id=user_id).all()
        return Topic.query.filter(Topic.title.like(f'%{title}%'), Topic.user_id==user_id).all()
    
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
    
