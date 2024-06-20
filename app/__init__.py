from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
import asyncio
import atexit
from .extensions import db, jwt
from .topics.cron.twscrape_job import scrape_twitter
from .topics.cron.sentiment_job import analyze_tweets
from .articles.cron.articles_scrape_job import scrape_articles
from .articles.cron.zero_shot_job import classificate_articles
from threading import Lock
from flask_cors import CORS



def create_app():
    app = Flask(__name__)
    CORS(app)
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
    from .articles import article_bp
    app.register_blueprint(article_bp)
    
    scheduler = BackgroundScheduler()

    tweets_dict = {}
    lock_tweets=Lock()

    articles_list = []
    lock_articles=Lock()

    def scheduled_scrape():
        nonlocal tweets_dict
        nonlocal lock_tweets
        with lock_tweets:
            with app.app_context():
                tweets_dict = asyncio.run(scrape_twitter())

    def sentiment_job():
        nonlocal tweets_dict
        nonlocal lock_tweets
        with lock_tweets:
            with app.app_context():
                topics = analyze_tweets(tweets_dict)
                print(topics)

    def articles_job():
        nonlocal articles_list
        nonlocal lock_articles
        with lock_articles:
            with app.app_context():
                articles_list = asyncio.run(scrape_articles())

    def zero_shot_job():
        nonlocal articles_list
        nonlocal lock_articles
        with lock_articles:
            with app.app_context():
                articles_list = classificate_articles(articles_list)
        

    scheduler.add_job(scheduled_scrape, trigger="cron", hour=3, minute=0)
    scheduler.add_job(sentiment_job, trigger="cron", hour=3, minute=0)

    scheduler.add_job(articles_job, trigger="cron", hour=14, minute=2)
    scheduler.add_job(zero_shot_job, trigger="cron", hour=14, minute=2)
                      
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())


    return app

