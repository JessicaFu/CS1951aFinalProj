from django.db import models, IntegrityError
import datetime
import django.utils.timezone as timezone

# Create your models here.

class Source(models.Model):
    name = models.CharField(max_length=16)
    url = models.URLField()

class Article(models.Model):
    source = models.ForeignKey(Source)
    date = models.DateTimeField(default=timezone.now)
    url = models.CharField(max_length=255)
    text = models.TextField()
    headline = models.CharField(unique=True, max_length=255)

class Keyword(models.Model):
    article = models.ForeignKey(Article)
    word = models.CharField(max_length=24)

class RedditPost(models.Model):
    source = models.ForeignKey(Source)
    date = models.DateTimeField(default=timezone.now)
    url = models.URLField()
    text = models.TextField()
    headline = models.CharField(max_length=255)
    
    post_title = models.CharField(max_length=255)
    votes = models.IntegerField()

class RedditComment(models.Model):
    reddit_post = models.ForeignKey(RedditPost)
    text = models.CharField(max_length=200)
    parent_comment = models.ForeignKey('self')



#############################################################

#       Factory Methods

#############################################################


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
    except IntegrityError:
        print 'not unique headline for ' + article['headline'] + ' skipping.'

    for kw in keywords:
        try:
            keyword = Keyword(article=art, word=kw)
            keyword.save()
        except:
            print 'keyword ' + kw + ' could not be saved to db'

