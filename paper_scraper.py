import sys, os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "data_science_project.settings")
sys.path.append('/home/ubuntu/CS1951aFinalProj/')

from django.db import models
from news.models import *

import newspaper
import datetime

def scrape(source_name, source_url, date_func):
	paper = newspaper.build(source_url, memoize_articles=False)

	for article in paper.articles:
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
               
                try:
                    article = {
                        'headline': title,
                        'url': url,
                        'text': text,
                        'date': date_time
                    }
                    newspaper_article(source, article, keywords=keywords)
                    print 'article created'
                except Exception as ex:
                    print 'Article could not be created due to following error'
                    print ex

