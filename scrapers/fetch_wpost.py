import newspaper
from newspaper import news_pool, Config, Article, Source
import re
import datetime

def main():
    source="The Washington Post"
    delivery_time="6:00"
    #config = Config()
    #config.memoize_articles = False
    wpost = Source("http://washingtonpost.com/world", memoize_articles=False)
    wpost.download()
    wpost.parse()

    wpost.set_categories()
    
    wpost.categories = [wpost.categories[0]]
    wpost.categories[0].url = "http://washingtonpost.com/world"
    wpost.download_categories()
    wpost.parse_categories()

    wpost.set_feeds()
    wpost.download_feeds()

    wpost.generate_articles()
    
    #for c in wpost.categories:
    #    print(c)
    #guardian = newspaper.build('http://theguardian.com/world', memoize_articles=False)
    #news_pool.set([guardian], threads_per_source=2)
    #news_pool.join()

    #print(wpost.size())

    for article in [x for x in wpost.articles if re.match(".*com/world/.*", x.url) is not None and re.match(".*gallery.html", x.url) is None]:
        url = article.url
        a = Article(url, language='en')
        a.download()
        a.parse()
        a.nlp()
        html = a.html
        summary = a.summary
        keywords = a.keywords
        title = a.title
        text = a.text
        #print(html)
        #print(text)
        #print(summary)
        #print(keywords)
        #print(title)
        #print(a.publish_date)
        if source in title:
            title = None
        #print(title)
        if a.publish_date is not  None:
            date = str(a.publish_date).split()[0].split("-")
            #print(date)
            date[0], date[1], date[2] = date[1], date[2], date[0]
            date = "/".join(date)
        else:
            date = None
        time = re.search(r'<span class="pb-timestamp">(.*?)</span>' , html)
        if time is None:
            print(url)
            date = None
        else:
            time = time.group(1)
            if ":" not in time:
                time = delivery_time
            else:
                time = time.split(" at ")[1]
                time = datetime.datetime.strptime(time,'%I:%M %p').strftime('%H:%M')
        date_time = str(date) + " " + str(time)
        #print(text)
        return
        #print(date_time)
        #TODO: Add stuff to the DB

if __name__ == "__main__":
    main()

# source #
# url #
# text #
# time/date
# keywords #
# summary
