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
#import newspaper.article.ArticleException

def main():
	source = 'http://www.heraldsun.com.au/'
	#file_name = 'heraldsun.csv'
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

		source_name = 'The Herald Sun'
		title = article.title
		html = article.html#.replace('\r','').replace('\n','')
		url = article.url
		summary = article.summary
		keywords = article.keywords
		text = article.text

		m1 = re.search('datestamp">(.+?)</span>', html)
		d = None
		if m1 != None:
			d = m1.group(1)
		m2 = re.search('timestamp">(.+?)</span>', html)
		t = None
		if m2 != None:
			t = m2.group(1)

		#print title + ": " + t + " " + d
		date_time = None
		if not (t == None or d == None):
			#print t + " " + d
			date_time = datetime.datetime.strptime(d + " " + t,'%B %d, %Y %I:%M%p')
			#print date_time

			#writer.writerow(map(lambda x: x.encode('utf-8'), [source, url, title, t, d, text, str(keywords), summary]))
			#print title
                try:
                    article = {
                        'headline': title,
                        'url': url,
                        'text': text,
                        'date': date_time
                    }
                    newspaper_article('Herald Sun', article, keywords=keywords)
                except Exception as ex:
                    print 'Article could not be created due to following error'
                    print ex



if __name__ == "__main__":
	main()

print 'DONE'
