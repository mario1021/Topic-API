from app import db
from datetime import datetime
from ...topics.models.topic_model import Topic

topic_articles= db.Table('topic_articles',
                        db.Column('id', db.BigInteger, primary_key=True),
    db.Column('topic_id', db.BigInteger, db.ForeignKey('topics.id'), nullable=False),
    db.Column('articles_id', db.BigInteger, db.ForeignKey('articles.id'), nullable=False),
)

class Article(db.Model):
    __tablename__ = 'articles'
    #a new has id, title, content, url, source_id, pub_date, created_at, updated_at. content is text type in the sql
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    url = db.Column(db.String(100), nullable=False)
    source_id = db.Column(db.BigInteger, db.ForeignKey('sources.id'), nullable=False)
    source = db.relationship('Source', backref=db.backref('articles', lazy='dynamic'))
    pub_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)
    topics = db.relationship('Topic', secondary=topic_articles, backref=db.backref('articles', lazy='dynamic'))

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

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'url': self.url,
            'source': self.source.to_dict(),
            'pub_date': self.pub_date,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'topics': [topic.to_dict() for topic in self.topics]
        }
    
    @staticmethod
    def get_by_id(id):
        return Article.query.get(id)
    
    @staticmethod
    def get_all():
        return Article.query.all()
    
    
    @staticmethod
    def get_filtered(source_id, user_id, start_date, end_date, topic_id):
        #note that the relation to user is via topic_articles then topic which has user_id
        #also on this method each of the parameters is optional, so we need to check if they are None
        query = Article.query
        if source_id:
            query = query.filter_by(source_id=source_id)  
        if start_date:
            query = query.filter(Article.pub_date >= start_date)
        if end_date:
            query = query.filter(Article.pub_date <= end_date)
            
        if user_id or topic_id:
            query = query.join(topic_articles).join(Topic)
        if user_id:
            query = query.filter(Topic.user_id==user_id)
        if topic_id:
            query = query.filter(Topic.id==topic_id)
        
        # if topic_id:
        #     query = query.join(topic_articles).filter(topic_articles.c.topic_id==topic_id)
        return query.all()
    
