from django.db import models

# Create your models here.

class Source(models.Model):
    id = models.CharField(primary_key=True)
    name = models.CharField(max_length=16)
    language = models.CharField(max_length=4)


class Article(models.Model):
    id = models.CharField(primary_key=True)
    source = models.ForeignKey(Source)
    date = models.DateTimeField('date published')
    url = models.URLField()
    text = models.TextField()

class Keyword(models.Model):
    id = models.CharField(primary_key=True)
    article = models.ForeignKey(Article)
    word = models.CharField(max_length=24)

class RedditPost(models.Model):
    id = models.CharField(primary_key=True)
    article = models.ForeignKey(Article)
    votes = models.IntegerField()

class RedditComment(models.Model):
    id = models.CharField(primary_key=True)
    reddit_post = models.ForeignKey(RedditPost)
    text = models.CharField(max_length=200)
    parent_comment = models.ForeignKey(RedditComment)
