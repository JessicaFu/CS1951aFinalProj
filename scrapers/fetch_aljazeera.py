import newspaper
from newspaper import news_pool, Config, Article, Source
import re
from time import sleep
from datetime import datetime

def fetch_data(aj):
	aj.build()
	for article in [x for x in aj.articles]:
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

        	date = re.search(r'<span class="date">(.*)<\/span>' , html)
		if date != None:
			date  = date.group(1).replace("'","")
		time = re.search(r'<span class="time">(.*)<\/span>' , html)
		if time != None:
			time = time .group(1).replace("'","")

		if date == None or time == None:
			datetime_obj = datetime.now()
		else:
			date_time = date + " " + time[:-3]
			datetime_obj=datetime.strptime(date_time,'%B %d, %Y %I:%M%p')
		print datetime_obj	

def main():
    source="Al Jazeera"
    aj = Source("http://america.aljazeera.com/topics/topic/categories/international.html", memoize_articles=False)
    fetch_data(aj)

if __name__ == "__main__":
    main()

# source #
# url #
# text #
# time/date
# keywords #
# summary