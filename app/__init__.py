from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
import asyncio
import atexit
from .extensions import db, jwt
from .topics.cron.twscrape_job import scrape_twitter
from threading import Lock


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/topicapp'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
    db.init_app(app)
    jwt.init_app(app)

    
    # Registro de los Blueprints
    from .auth import auth_bp
    app.register_blueprint(auth_bp)
    from .topics import topic_bp
    app.register_blueprint(topic_bp)
    
    scheduler = BackgroundScheduler()

    tweets_dict = {}
    lock=Lock()

    def scheduled_scrape():
        nonlocal tweets_dict
        nonlocal lock
        with lock:
            with app.app_context():
                tweets_dict = asyncio.run(scrape_twitter())

    def another_job():
        nonlocal tweets_dict
        nonlocal lock
        with lock:
            with app.app_context():
                print(tweets_dict)

    scheduler.add_job(scheduled_scrape, 'interval', minutes=2)
    scheduler.add_job(another_job, 'interval', minutes=2)
                      
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())


    return app

