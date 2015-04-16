import sys, os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "data_science_project.settings")
sys.path.append('/home/ubuntu/CS1951aFinalProj/')

from django.db import models
from news.models import *

import newspaper
from newspaper import news_pool, Config, Article, Source
import re
from datetime import datetime, timedelta

def main():
    source="The Guardian"
    #config = Config()
    #config.memoize_articles = False
    guardian = Source("http://www.theguardian.com/world", memoize_articles=False)
    guardian.build()
    #guardian = newspaper.build('http://theguardian.com/world', memoize_articles=False)
    #news_pool.set([guardian], threads_per_source=2)
    #news_pool.join()

    #print(guardian.size())

    for article in [x for x in guardian.articles if re.match(".*/world/.*", x.url) is not  None]:
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

        html = a.html
        summary = a.summary
        keywords = a.keywords
        title = a.title
        text = a.text
        date = str(a.publish_date).split()[0].split("-")
        date[0], date[1], date[2] = date[1], date[2], date[0]
        date = "/".join(date)
        delta = re.search(r'<span class="content__dateline-time">(.*)</span>' , html).group(1).replace(".",":").split()[0]
	time = datetime.now() + timedelta(hours=delta )
        date_time = date + " " + time
        #print(title)
        #print(date_time)
        date_obj = datetime.datetime.strptime(date_time,'%m/%d/%Y %H:%M')
        #print(date_obj.strftime('%Y/%m/%d %I:%M %p'))
        #TODO: Add stuff to the DB

        try:
            article = {
                'headline': title,
                'url': url,
                'text': text,
                'date': date_obj
            }
            newspaper_article('The Guardian', article, keywords=keywords)
        except Exception as ex:
            print 'Article could not be created due to following error'
            print ex

if __name__ == "__main__":
    main()

# source #
# url #
# text #
# time/date
# keywords #
# summary
