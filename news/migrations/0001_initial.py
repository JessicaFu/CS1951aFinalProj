# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('url', models.CharField(max_length=255)),
                ('text', models.TextField()),
                ('headline', models.CharField(unique=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('word', models.CharField(max_length=32)),
                ('article', models.ForeignKey(to='news.Article')),
            ],
        ),
        migrations.CreateModel(
            name='RedditComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=200)),
                ('creation_time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='RedditPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('url', models.URLField()),
                ('text', models.TextField()),
                ('headline', models.CharField(max_length=255)),
                ('post_title', models.CharField(max_length=255)),
                ('votes', models.IntegerField()),
                ('submission_time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('url', models.URLField()),
            ],
        ),
        migrations.AddField(
            model_name='redditpost',
            name='subreddit',
            field=models.ForeignKey(related_name='subreddit', to='news.Source'),
        ),
        migrations.AddField(
            model_name='redditcomment',
            name='reddit_post',
            field=models.ForeignKey(to='news.RedditPost'),
        ),
        migrations.AddField(
            model_name='article',
            name='source',
            field=models.ForeignKey(to='news.Source'),
        ),
    ]
