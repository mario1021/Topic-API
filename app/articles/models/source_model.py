from app import db
from datetime import datetime


class Source(db.Model):
    __tablename__ = 'sources'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)

    def __init__(self, name, url):
        self.name = name
        self.url = url

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Source.query.get(id)
    
    @staticmethod
    def get_all():
        return Source.query.all()