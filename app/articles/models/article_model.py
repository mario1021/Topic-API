from app import db
from datetime import datetime


class Article(db.Model):
    __tablename__ = 'articles'
    #a new has id, title, content, url, source_id, pub_date, created_at, updated_at. content is text type in the sql
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    url = db.Column(db.String(100), nullable=False)
    source_id = db.Column(db.BigInteger, db.ForeignKey('sources.id'), nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)

    def __init__(self, title, content, url, source_id, pub_date):
        self.title = title
        self.content = content
        self.url = url
        self.source_id = source_id
        self.pub_date = pub_date

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()