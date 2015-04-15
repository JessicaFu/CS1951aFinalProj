import sys, os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "data_science_project.settings")
sys.path.append('/home/ubuntu/CS1951aFinalProj/')

from django.db import models
from news.models import *

import newspaper
from newspaper import Article
import re
import csv
import datetime


def main():
	source = 'http://www.theonion.com/'
	#file_name = 'onion.csv'
	#writer = csv.writer(open(file_name, 'w'))

	paper = newspaper.build(source, memoize_articles=False)

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
			continue

        # Here are all of the fields to be entered into the DB
        ####################################
		source_name = 'The Onion'
		date_time = None
		title = article.title
		url = article.url
		summary = article.summary
		keywords = article.keywords
		text = article.text
		####################################
		html = article.html.replace('\r','').replace('\n','')

		m = re.search('class="pubdate">(.+?)</span>', html)
		date = None
		if not m == None:
			date = m.group(1).strip()

		if not date == None:
			date_time = datetime.datetime.strptime(date + ' 12PM','%b %d, %Y %I%p').strftime('%c')
			#print date_time + ": " + title + " - " + summary

		#if not date == "Null":
		#	writer.writerow(map(lambda x: x.encode('utf-8'), [source, url, title, t, d, text, str(keywords), summary]))
		#	print title
                try:
                    article = {
                        'headline': title,
                        'url': url,
                        'text': text,
                        'date': date_time
                    }
                    newspaper_article(source_name, article, keywords=keywords)
                except Exception as ex:
                    print 'Article could not be created due to following error'
                    print ex


if __name__ == "__main__":
	main()

print 'DONE'
