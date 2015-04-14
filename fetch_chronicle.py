import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "data_science_project.settings")

from django.db import models
from news.models import *

import newspaper
import re
import datetime

def main():
	source = 'http://www.thechronicle.com.au/'

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

		source_name = 'The Chronicle'
		date_time = None
		title = article.title
		html = article.html.replace('\r','').replace('\n','')
		url = article.url
		summary = article.summary
		keywords = article.keywords
		text = article.text

		m = re.search('class="auth-details">(.+?)</div>', html)
		if not m == None:
			auth_list = m.group(1).strip().split('|')
			if len(auth_list) > 1:
				dt = auth_list[1].strip()
			else:
				dt = auth_list[0]
			dt = dt.split('  ')[0]
			dt_parts = dt.split()
			dt_parts[0] = dt_parts[0][0:len(dt_parts[0])-2]
			dt = ' '.join(dt_parts)


		if not dt == None:
			date_time = datetime.datetime.strptime(dt,'%d %b %Y %I:%M %p')
			#print date_time
                
                try:
                    article = {
                        'headline': title,
                        'url': url,
                        'text': text,
                        'date': date_time
                    }
                    newspaper_article('The Chronicle', article, keywords=keywords)
                except Exception as ex:
                    print 'Article could not be created due to following error'
                    print ex

		#writer.writerow(map(lambda x: x.encode('utf-8'), [source, url, title, t, d, text, str(keywords), summary]))

if __name__ == "__main__":
	main()

print 'DONE'
