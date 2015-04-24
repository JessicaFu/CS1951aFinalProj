import sys, os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "data_science_project.settings")
sys.path.append('/home/ubuntu/CS1951aFinalProj/')

from django.db import models
from news.models import *

import newspaper
import datetime

def scrape_article(article, date_func):
    """
        scrapes a single article using newspaper returning all the article data

        article
            a newspaper article url
        
        date_func
                a function to extract the date given an article
    """
    article = newspaper.Article(article)
    article.download()
    for i in range(10):
        if article.is_downloaded:
                break
        else:
                article.download()

        if not article.is_downloaded:
            print("Error: Did not donwnload something")
            continue

        try:
            article.parse()
            article.nlp()
        except newspaper.article.ArticleException, e:
            print 'nlp parsing failed'
            continue

    date_time = None
    title = article.title
    html = article.html.replace('\r','').replace('\n','')
    url = article.url
    summary = article.summary
    keywords = article.keywords
    text = article.text
    dt = None
    try:
        dt = date_func(article)
    except Exception as ex:
        print 'date func failed with exception'
        print ex

    if dt == None:
        print 'date could not be found, setting time to now'
        dt = datetime.datetime.now()
   
    article = {
        'headline': title,
        'url': url,
        'text': text,
        'date': date_time
    }
    return (article, keywords)

def scrape(source_name, source_url, date_func):
    """
        scrapes a full source and writes each article to the db

        source_name
        the name of the source as it appears in the db, eg. 'The Chronicle'

        source_url
        the url to the source homepage

        date_func
        a function to extract the date given an article
    """
    paper = newspaper.build(source_url, memoize_articles=False)

    for article in paper.articles:
        (article_data, keywords) = scrape_article(article, date_func)
        try:
            newspaper_article(source, article_data, keywords=keywords)
            print 'article created'
        except Exception as ex:
            print 'Article could not be created due to following error'
            print ex


