from __future__ import division
import sys, os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "data_science_project.settings")
sys.path.append('/home/ubuntu/CS1951aFinalProj/')
import django
django.setup()
from django.db import models
from news.models import *

import string
import datetime
import operator
import math
import csv
from nltk.corpus import stopwords

def get_sentiment_list():
	afinnfile = open("./AFINN-111.txt")
	for line in afinnfile:
		term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
		sentiment_scores[term] = float(score)      # Convert the score to a float.

def get_words(text):	
	exclude = set(string.punctuation)
	stop_words = stopwords.words('english')
	words = text.split()
	proc_words = []
	for word in words:
		word = ''.join(ch for ch in word if ch not in exclude and ch.isalnum())
		word = word.lower()
		if not word in stop_words and len(word) > 0 and word != "\n" and word != "\r":
			proc_words.append(word)
	return proc_words

def calc_sent(text):
	words = get_words(text)
	sent = 0
	for word in words:
		if word in sentiment_scores:
			sent += sentiment_scores[word]
	return sent

def get_sentiment(article):
	global sentiment_scores
	sentiment_scores = {}
	get_sentiment_list()

	if article == None:
		articles = Article.objects.all()

		for art in articles: 
			if len(art.text) >0:
				text_keywords = ""
				keywords = Keyword.objects.filter(article__id=art.id)
				for key in keywords:
					text_keywords += key.word.encode('utf-8')+ " "
				headline = art.headline.encode('utf-8')
				text = text_keywords + headline + " " + art.text.encode('utf-8') + " "
				

				if len(text) > 0:
					art.sentiment_score = calc_sent(text)
					art.save()
	else:
		text_keywords = ""
		keywords = Keyword.objects.filter(article__id=article.id)
		for key in keywords:
			text_keywords+= key.word.encode('utf-8')+ " "
		headline = article.headline.encode('utf-8')
		text = text_keywords + headline + " " + article.text.encode('utf-8')
		
		if len(text) > 0:
			art.sentiment_score = calc_sent(text)
			art.save()

def main():

	get_sentiment(None)


if __name__ == "__main__":
    main()

######################## correlation function ###############################
def get_article_sentiment(article):
	text_keywords = ""
	keywords = Keyword.objects.filter(article__id=art.id)
	for key in keywords:
		text_keywords += key.word.encode('utf-8')+ " "

	headline = art.headline.encode('utf-8')
	text = text_keywords + headline + " " + art.text.encode('utf-8') + " "

	return calc_sent(text)
