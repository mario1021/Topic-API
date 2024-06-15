import newspaper
from deep_translator import GoogleTranslator
from ..models.source_model import Source
from ..models.article_model import Article
import datetime


def scrape_articles():
    articles_list = []
    sources = Source.get_all()
    for source in sources:
        paper = newspaper.build(source.url)
        paper.download_articles()
        for article in paper.articles:
            article.download()
            article.parse()
            article.nlp()
            #si la publish date es de hace más de dos días lo ignoramos
            if article.publish_date:
                if (datetime.datetime.now() - article.publish_date).days > 2:
                    continue
            if article.text:
                articles_list.append({
                    "title": article.title,
                    "text": article.text,
                    "full_text" : f"Title: {article.title}. \nText: {article.text}. \nKeywords: {(' ').join(article.keywords)}.",
                    "url": article.url,
                    "source_id": source.id,
                    "keywords": article.keywords,
                    "pub_date": article.publish_date
                })
    print(articles_list)           
    return articles_list