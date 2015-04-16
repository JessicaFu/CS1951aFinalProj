import sys, os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "data_science_project.settings")
sys.path.append('/home/ubuntu/CS1951aFinalProj/')

from django.db import models
from news.models import *

import newspaper

import re
from datetime import datetime

def fetch_data(source):
    cnn = newspaper.build(source, memoize_articles=False)
    for a in cnn.articles:
        url = a.url
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
                'date': datetime_obj
            }
            newspaper_article('CNN', article, keywords=keywords)
            print "inserted"
        except Exception as ex:
            print 'Article could not be created due to following error'
            print ex

def main():
    fetch_data("http://www.cnn.com/world")
    fetch_data("http://www.cnn.com/us")

if __name__ == "__main__":
    main()

# source #
# url #
# text #
# time/date
# keywords #
# summary
