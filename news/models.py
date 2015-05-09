import sys

sys.path.append('/home/ubuntu/CS1951aFinalProj/')

from django.db import models, IntegrityError
import datetime
import django.utils.timezone as timezone

from paper_scraper import *
# Create your models here.

class Source(models.Model):
    name = models.CharField(max_length=64)
    url = models.URLField()

class Article(models.Model):
    source = models.ForeignKey(Source)
    date = models.DateTimeField(default=timezone.now)
    url = models.CharField(unique=True, max_length=255)
    text = models.TextField()
    headline = models.CharField(max_length=255)
    word_count = models.IntegerField()
    sentiment_score = models.FloatField()

class Keyword(models.Model):
    article = models.ForeignKey(Article)
    word = models.CharField(max_length=32)

class RedditPost(models.Model):
    date = models.DateTimeField(default=timezone.now)
    url = models.URLField()
    text = models.TextField()
    headline = models.CharField(max_length=255)
   
    subreddit = models.ForeignKey(Source, related_name='subreddit') 
    post_title = models.CharField(unique=True, max_length=255)
    votes = models.IntegerField()
    submission_time = models.DateTimeField(default=timezone.now)

class RedditComment(models.Model):
    reddit_post = models.ForeignKey(RedditPost)
    text = models.CharField(max_length=200)
    creation_time = models.DateTimeField(default=timezone.now)

class RedditKeyword(models.Model):
    post = models.ForeignKey(RedditPost)
    word = models.CharField(max_length=64)

class PosIndex(models.Model):
    word = models.CharField(max_length=64)
    article = models.ForeignKey(Article)
    position_list = models.IntegerField()
    weight = models.FloatField()

class LastUpdate(models.Model):
    value = models.IntegerField()

#############################################################

#       Factory Methods

#############################################################

def make_keywords(art, keywords):
    """
        turns a list of keywords into database entries

        art
            article model
        keywords
            list of keywords
    """
    for kw in keywords:
        try:
            keyword = Keyword(article=art, word=kw)
            keyword.save()
        except Exception as ex:
            print ex
            print 'keyword ' + kw + ' could not be saved to db'

def make_reddit_keywords(post, keywords):
    """
        turns a list of keywords into database entries

        art
            article model
        keywords
            list of keywords
    """
    for kw in keywords:
        try:
            keyword = RedditKeyword(post=post, word=kw)
            keyword.save()
        except Exception as ex:
            print ex
            print 'keyword ' + kw + ' could not be saved to db'

def newspaper_article(source, article, keywords=[]):
    """
        creates and save an article database entry 
        
        minimal error handling is performed, so make sure fields is specified exactly
        Args:
        source - string name for source, should be exact
                if source is not in DB will create an entry for the source
            
        keywords - a list of all keywords found in the article

        article - a dictionary containing the following keys:
            date - datetime object of article creation
            url - full url path to the article
            text - the text of the article
            headline - the headline to the article
        
    """

    src = None
    try:
        src = Source.objects.get(name=source)
    except Source.DoesNotExist:
        #This is jank but can be touched up manually
        src = Source(name=source, url=article['url'])
        src.save()
        print 'source added to db with name: ' + source
   
    #unpacks article into article constructor
    try: 
        art = Article(source=src, **article)
        art.save()
        make_keywords(art, keywords)
    except IntegrityError:
        print 'not unique headline for ' + article['headline'] + ' skipping.'

def make_comments(post, comments):
    """
        puts all the reddit comments into the db
        
        Args:
        post - the RedditPost the comment belongs to

        comments - a list of dictionaries with the following keys
            text - the text of the comment
            creation_time - the time the comment was created
    """
    for comment in comments:
        try:
            com = RedditComment(reddit_post=post, **comment)
            com.save()
        except Exception as ex:
            print 'comment could not be created'
            print ex

def reddit_post(data, comments):
    """
        makes a reddit post and associated db entries

        Args:
        data - a dictionary with the following keys
            article - the url of the article
            subreddit - name of subreddit, eg. 'news'
            post_title - the title of the post as it appears on reddit
            votes - the votes as counted when the api is run
            submission_time - the time the post is submitted
            
        comments - a list of dictionaries with each dictionary having entries as specified by the make_comments procedure
    """

    sub = None
    try:
        sub = Source.objects.get(name=data['subreddit'])
    except Source.DoesNotExist:
        #This is jank but can be touched up manually
        sub = Source(name=data['subreddit'], url='reddit.com')
        sub.save()
        print 'source added to db with name: ' + data['subreddit']
   
    data['subreddit'] = sub
    
    (article, keywords) = scrape_article(data['url'], lambda x: timezone.now()) 
    data['text'] = article['text']
    data['date'] = article['date']
    data['headline'] = article['headline']

    try:
        post = RedditPost(**data)
        post.save()
        make_reddit_keywords(post, keywords)
        make_comments(post, comments)
    except IntegrityError as ex:
        print ex
        print 'not unique reddit post for ' + data['post_title']
