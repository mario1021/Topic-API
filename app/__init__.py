from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/TFG'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
    jwt = JWTManager(app)

    db.init_app(app)
    # Registro de los Blueprints
    from .auth import auth_bp
    app.register_blueprint(auth_bp)
    from .topics import topic_bp
    app.register_blueprint(topic_bp)
    # from .admin import admin_bp
    # app.register_blueprint(admin_bp)
    # from .public import public_bp
    # app.register_blueprint(public_bp)
    return app

