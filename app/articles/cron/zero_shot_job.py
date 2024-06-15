from transformers import pipeline
from ...topics.models.topic_model import Topic
from ..models.article_model import Article
import re

def split_text(text):
    split_text = re.split(r'(?<=[.!?]) +', text)
    return split_text



def classificate_articles(articles_list):
    zeroshot_classifier = pipeline("zero-shot-classification", model="MoritzLaurer/deberta-v3-large-zeroshot-v2.0")
    hypothesis_template = "This article is about {}"
    threshold=0.75
    topic_titles = [topic.title for topic in Topic.get_all()]
    topics=Topic.get_all()

    translate_pipeline = pipeline("translation", model="Helsinki-NLP/opus-mt-es-en")
    for topic in topic_titles:
        topic = translate_pipeline(topic, target_language="es")[0]['translation_text']


    for article in articles_list:
        #to translate the article, we split it into sentences and translate each one, then we join them back together
        senteces = split_text(article['full_text'])
        translated_text = ""
        for sentence in senteces:
            translated_text += translate_pipeline(sentence, target_language="en")[0]['translation_text'] + " "
        article['full_text'] = translated_text
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

        

