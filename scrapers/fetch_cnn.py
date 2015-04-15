import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "data_science_project.settings")

from django.db import models
from news.models import *

import newspaper
from newspaper import news_pool, Config, Article, Source
import re
from time import sleep
from datetime import datetime
def fetch_data(cnn):
	cnn.build()
	for article in [x for x in cnn.articles]:
        	url = article.url
        	a = Article(url, language='en')
        	a.download()
        	for i in range(10):
            		if a.is_downloaded:
                		break
            		else:
               			a.download()

        	if not a.is_downloaded:
            		print("Error: Did not download something")
            		continue

        	a.parse()
        	a.nlp()
        	html = a.html
        	summary = a.summary
        	keywords = a.keywords
        	title = a.title
        	text = a.text
        	date_time = re.search(r'<meta itemprop="dateCreated" content="(.*?)">' , html).group(1).replace(".",":").split()[0]
		date = date_time.split("T")[0]
		time = date_time.split("T")[1][:-1]
		
		date = date.split("-")
		date[0], date[1], date[2] = date[1], date[2], date[0]
        	date = "/".join(date)

		time = time.split(":")
		time = time[0] + ":" + time[1]
		date_time = date + " " + time
		datetime_obj=datetime.strptime(date_time,'%m/%d/%Y %H:%M')
		try:
                    article = {
                        'headline': title,
                        'url': url,
                        'text': text,
                        'date': date_time
                    }
                    newspaper_article('CNN', article, keywords=keywords)
		    print "inserted"
                except Exception as ex:
                    print 'Article could not be created due to following error'
                    print ex

def main():
    source="CNN"
    cnnWorld = Source("http://www.cnn.com/world", memoize_articles=False)
    fetch_data(cnnWorld)
    cnnUsa = Source("http://www.cnn.com/us", memoize_articles=False)
    fetch_data(cnnUsa)

if __name__ == "__main__":
    main()

# source #
# url #
# text #
# time/date
# keywords #
# summary