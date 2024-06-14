from app import db
from datetime import datetime


class Mention(db.Model):
    __tablename__ = 'mentions'
    id = db.Column(db.BigInteger, primary_key=True)
    #esta tabla tiene date, topic_id, amount, created_at, updated_at
    date = db.Column(db.DateTime, nullable=False)
    topic_id = db.Column(db.BigInteger, db.ForeignKey('topics.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)

    def __init__(self, date, topic_id, amount):
        self.date = date
        self.topic_id = topic_id
        self.amount = amount

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

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
        return Mention.query.filter(Mention.topic_id.in_(topic_ids), Mention.date >= start_date, Mention.date <= end_date).all()
