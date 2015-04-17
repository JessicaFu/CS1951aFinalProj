import os,sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "data_science_project.settings")
sys.path.append('/home/ubuntu/CS1951aFinalProj/')

from django.db import models
from news.models import *

import newspaper
from newspaper import news_pool, Config, Article, Source
import re
from datetime import datetime

def fetch_data(bbc):
	bbc.build()
	for article in [x for x in bbc.articles]:
        	url = article.url
        	a = Article(url, language='en')
        	a.download()
        	for i in range(10):
            		if a.is_downloaded:
                		break
            		else:
                		a.download()
        	try:
            		a.parse()
            		a.nlp()
        	except:
            		print("Error: Not parsed/downloaded correctly.")
            		continue

       		a.parse()
        	a.nlp()	
        	html = a.html
        	summary = a.summary
        	keywords = a.keywords
        	title = a.title
		print title
        	text = a.text
        	#date = str(a.publish_date).split()[0].split("-")
        	#date[0], date[1], date[2] = date[1], date[2], date[0]
        	#date = "/".join(date)
        	#time = re.search(r'<span class="date date--v2 relative-time">(.*)<\/span>' , html).group(1).replace(".",":").split()[0]
		#bbc does not have a time div in html
		date_time = datetime.now()	
        	
		try:
                    article = {
                        'headline': title,
                        'url': url,
                        'text': text,
                        'date': date_time
                    }
                    newspaper_article('BBC', article, keywords=keywords)
                except Exception as ex:
                    print 'Article could not be created due to following error'
                    print ex

def main():
    source="BBC"
    bbc = Source("http://www.bbc.com/news", memoize_articles=False)
    fetch_data(bbc)


if __name__ == "__main__":
    main()

# source #
# url #
# text #
# time/date
# keywords #
# summary
