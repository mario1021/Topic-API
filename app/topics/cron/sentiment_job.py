import pandas as pd
import re
from pysentimiento import create_analyzer
from collections import defaultdict
from datetime import datetime, timedelta
from ..models.topic_model import Topic
from ..models.mention_model import Mention

def analyze_tweets(tweets_dict):
        topics = Topic.get_all()        
        analyzer = create_analyzer(task="sentiment",lang="es")
        # self.full_criteria= list(zip(self.criteria_df['Ingredient'],self.criteria_df['Id']))
        for topic in topics:
            day_mentions=0
            tweets=tweets_dict[topic.title]
            for tweet in tweets:
                sentiment=analyzer.predict(tweet)
                day_mentions+=1
                if topic.sentiment_score is None:
                    print(sentiment.probas)
                    #example of sentiment.probas: {POS: 0.998, NEG: 0.002, NEU: 0.000}.
                    #if the sentiment is none, its the first time we ever see the topic, so we just assign the sentiment of the first tweet
                    topic.pos_score=sentiment.probas['POS']
                    topic.neg_score=sentiment.probas['NEG']
                    topic.neu_score=sentiment.probas['NEU']
                    #en topic.sentiment guardamos el valor de la clave con el valor más alto
                    topic.sentiment=max(sentiment.probas, key=sentiment.probas.get)
                else:
                    #if there are already values, we update the sentiment scores with a formula like this  # dict_score[key]=(dict_score[key]*mentions)/(mentions+1)+(sentiment.probas[key])/(mentions+1)
                    topic.pos_score=(topic.pos_score*topic.total_mentions)/(topic.total_mentions+1)+(sentiment.probas['POS'])/(topic.total_mentions+1)
                    topic.neg_score=(topic.neg_score*topic.total_mentions)/(topic.total_mentions+1)+(sentiment.probas['NEG'])/(topic.total_mentions+1)
                    topic.neu_score=(topic.neu_score*topic.total_mentions)/(topic.total_mentions+1)+(sentiment.probas['NEU'])/(topic.total_mentions+1)
                    topic.sentiment=max(sentiment.probas, key=sentiment.probas.get)
                topic.total_mentions+=1
                topic.save()
            mention=Mention(datetime.now(),topic.id,day_mentions)
            mention.save()
        return topics








        