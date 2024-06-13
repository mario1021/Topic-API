from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(30), nullable=False)

    def __init__(self, name, email):
        self.name = name
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return User.query.get(id)
    
    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).one_or_none()