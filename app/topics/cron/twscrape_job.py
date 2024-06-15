import json
import re
import pandas as pd
import asyncio
from twscrape import API, gather
from twscrape.logger import set_log_level
from datetime import datetime, timedelta
import os
from ..models.topic_model import Topic
from ..models.mention_model import Mention


async def scrape_twitter(substraction_days=1):

    api=API()
    # Añadimos las cuentas que vayamos a utilizar e iniciamos sesión
    await api.pool.add_account("scrappingtwtest", "380pas380", "scrappingtwtest@gmail.com", "380pas380")
    await api.pool.add_account("scrapingtwtest2", "380pas380", "scrappingtwtest2@gmail.com", "380pas380")
    await api.pool.add_account("scrapingtwtest", "380pas380", "scrapingtwtest@outlook.com", "380pas380")
    await api.pool.add_account("scrapingtwtest3", "380pas380", "scrapingtwtest3@outlook.es", "380pas380")
    await api.pool.add_account("scrapingtwtest4", "380pas380", "scrapingtwtest4@outlook.es", "380pas380")
    await api.pool.add_account("scrapingtwtest5", "380pas380", "scrapingtwtest5@gmail.com", "380pas380")
    await api.pool.add_account("scrapingtwtest6", "380pas380", "scrapingtwtest6@outlook.es", "380pas380")
    await api.pool.add_account("scrapingtwtest7", "380pas380", "scrapingtwtest7@outlook.es", "380pas380")
    await api.pool.add_account("scrapingtwtest8", "380pas380", "scrapingtwtest8@outlook.es", "380pas380")
    await api.pool.add_account("scrapingtwtest9", "380pas380", "scrapingtwtest9@outlook.es", "380pas380")
    await api.pool.add_account("tfgscraper, 380pas380", "tfgscraper@gmail.com", "380pas380")
    await api.pool.add_account("tfgscraper2, 380pas380", "tfgscraper2@gmail.com", "380pas380")
    await api.pool.add_account("tfgscraper3, 380pas380", "tfgscraper3@gmail.com", "380pas380")
    await api.pool.add_account("tfgscraper4, 380pas380", "tfgscraper4@gmail.com", "380pas380")

    
    await api.pool.login_all()
    await api.pool.reset_locks()
    
    tweets_dict={}

    today =datetime.now()
    today_str = today.strftime("%Y-%m-%d")
  
    yesterday=(today - timedelta(days=substraction_days)).strftime("%Y-%m-%d")

    topics = Topic.get_all()


 


    for topic in topics:
        keyword=topic.title
        tweets_dict[keyword]=[]
        print(keyword)
        tweets=await gather(api.search(f"{keyword} since:{yesterday}"))
        print(tweets)
        #los añadimos al diccionario
        for tweet in tweets:
            print(tweet)
            tweets_dict[keyword].append({
                "scraper_date": today_str,
                "pub_date": tweet.date,
                "url": tweet.url,
                "content": tweet.rawContent,
                "num_visits": tweet.viewCount,
                "num_likes": tweet.likeCount,
                "num_retweets": tweet.retweetCount,
                })

    return tweets_dict
