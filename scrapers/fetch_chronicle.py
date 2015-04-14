import newspaper
import re
import csv
import datetime

def main():
	source = 'http://www.thechronicle.com.au/'
	#file_name = 'thechronicle.csv'
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
			date_time = datetime.datetime.strptime(dt,'%d %b %Y %I:%M %p').strftime('%c')
			#print date_time

		#writer.writerow(map(lambda x: x.encode('utf-8'), [source, url, title, t, d, text, str(keywords), summary]))

if __name__ == "__main__":
	main()

print 'DONE'
