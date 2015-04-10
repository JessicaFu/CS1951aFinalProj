from django.db import models

# Create your models here.

class Source(models.Model):
    name = models.CharField(max_length=16)


class Article(models.Model):
    source = models.ForeignKey(Source)
    date = models.DateTimeField('date published')
    url = models.URLField()
    text = models.TextField()

class Keyword(models.Model):
    article = models.ForeignKey(Article)
    word = models.CharField(max_length=24)

class RedditPost(models.Model):
    article = models.ForeignKey(Article)
    votes = models.Integer()

class RedditComment(models.Model):
    reddit_post = models.ForeignKey(RedditPost)
    text = models.CharField(max_length=200)
    parent_comment = models.ForeignKey(RedditComment)
