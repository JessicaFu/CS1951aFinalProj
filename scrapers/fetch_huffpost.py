import newspaper
from newspaper import news_pool, Config, Article, Source
import re
import datetime

def main():
    source="The Huffington Post"
    delivery_time="6:00"
    #config = Config()
    #config.memoize_articles = False
    hpost = Source("http://huffingtonpost.com/theworldpost", memoize_articles=False)
    hpost.download()
    hpost.parse()

    hpost.set_categories()
    
    hpost.categories = [hpost.categories[0]]
    hpost.categories[0].url = "http://huffingtonpost.com/theworldpost"
    hpost.download_categories()
    hpost.parse_categories()

    hpost.set_feeds()
    hpost.download_feeds()

    hpost.generate_articles()
    
    #for c in hpost.categories:
    #    print(c)
    #guardian = newspaper.build('http://theguardian.com/world', memoize_articles=False)
    #news_pool.set([guardian], threads_per_source=2)
    #news_pool.join()

    #print(hpost.size())

    for article in [x for x in hpost.articles if re.match(".*html.*world.*", x.url) is not None]:
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
        #print(html)
        #print(text)
        #print(summary)
        #print(keywords)
        #print(title)
        #print(a.publish_date)
        if source in title:
            title = None
        #print(title)
        findtime = re.search(r'Posted.*<time datetime="(.*?)">', html)
        if findtime is None:
            date=None
            time=None
        else:
            date,time = findtime.group(1).split("T")
            date = date.split("-")
            date[0], date[1], date[2] = date[1], date[2], date[0]
            date = "/".join(date)
            
            time = ":".join(time.split("-")[0].split(":")[0:2])
        date_time = str(date) + " " + str(time)
        #print(title)
        #print(date_time)
        date_obj = datetime.datetime.strptime(date_time,'%m/%d/%Y %H:%M')
        #print(date_obj.strftime('%Y/%m/%d %I:%M %p'))
        #TODO: Add stuff to the DB

if __name__ == "__main__":
    main()

# source #
# url #
# text #
# time/date
# keywords #
# summary
