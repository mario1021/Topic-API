from app import db
from datetime import datetime


class Mention(db.Model):
    __tablename__ = 'mentions'
    id = db.Column(db.BigInteger, primary_key=True)
    day_date = db.Column(db.DateTime, nullable=False)
    topic_id = db.Column(db.BigInteger, db.ForeignKey('topics.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    sentiment = db.Column(db.String(10), nullable=True)
    pos_score = db.Column(db.Float, nullable=True)
    neg_score = db.Column(db.Float, nullable=True)
    neu_score = db.Column(db.Float, nullable=True)

    def __init__(self, day_date, topic_id, amount):
        self.day_date = day_date
        self.topic_id = topic_id
        self.amount = amount

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'day_date': self.day_date,
            'topic_id': self.topic_id,
            'amount': self.amount,
            'sentiment': self.sentiment,
            'pos_score': self.pos_score,
            'neg_score': self.neg_score,
            'neu_score': self.neu_score

        }

    @staticmethod
    def get_by_id(id):
        return Mention.query.get(id)
    
    @staticmethod
    def get_by_topic_id(topic_id):
        return Mention.query.filter_by(topic_id=topic_id).all()
    
    @staticmethod
    def get_all():
        return Mention.query.all()
    
    @staticmethod
    def get_by_topic_ids(topic_ids):
        return Mention.query.filter(Mention.topic_id.in_(topic_ids)).all()
    
    @staticmethod
    def get_by_topic_ids_and_date_range(topic_ids, start_date, end_date):
        return Mention.query.filter(Mention.topic_id.in_(topic_ids), Mention.day_date >= start_date, Mention.day_date <= end_date).all()
    
    @staticmethod
    def get_filtered(topic_id, start_date, end_date):
        mentions = Mention.query.filter_by(topic_id=topic_id)
        if start_date is not None:
            mentions = mentions.filter(Mention.day_date >= start_date)
        if end_date is not None:
            mentions = mentions.filter(Mention.day_date <= end_date)
        return mentions.all()
