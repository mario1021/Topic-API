from transformers import pipeline
from ...topics.models.topic_model import Topic
from ..models.article_model import Article

def classificate_articles(articles_list):
    zeroshot_classifier = pipeline("zero-shot-classification", model="MoritzLaurer/deberta-v3-large-zeroshot-v2.0")
    hypothesis_template = "This article is about {}"
    threshold=0.75
    topic_titles = [topic.title for topic in Topic.get_all()]
    topics=Topic.get_all()

    for article in articles_list:
        classification=zeroshot_classifier(article['full_text'], candidate_labels=topic_titles, multi_label=True, hypothesis_template=hypothesis_template)
        #labels=[label for label in classification['labels'] if classification['scores'][classification['labels'].index(label)]>threshold]
        labels=[label for label in classification['labels'] if classification['scores'][classification['labels'].index(label)]>threshold]
        print(labels)

        #now we need to save the article with the topics that were classified
        article=Article(article['title'], article['text'], article['url'], article['source_id'], article['pub_date'])
        article.save()
        for label in labels:
            article.topics.append(topics[topic_titles.index(label)])
        article.save()
    return articles_list

        

