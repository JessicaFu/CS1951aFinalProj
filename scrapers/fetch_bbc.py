import newspaper
from newspaper import news_pool, Config, Article, Source
import re
from time import sleep

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
        date = str(a.publish_date).split()[0].split("-")
        date[0], date[1], date[2] = date[1], date[2], date[0]
        date = "/".join(date)
        time = re.search(r'<span data-datetime="content__dateline-time">(.*)</span>' , html).group(1).replace(".",":").split()[0]
        date_time = date + " " + time

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