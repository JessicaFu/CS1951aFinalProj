from __future__ import division
import sys, os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "data_science_project.settings")
sys.path.append('/home/ubuntu/CS1951aFinalProj/')

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
	return sentiment_scores

def get_words(text):	
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

def get_art_sent(art):
	id = art.id
	name = art.headline.encode('utf-8')
	text = name + " " + art.text.encode('utf-8')
	if len(text) > 0:
		return calc_sent(text)
	
	return None
	
def gen_sent():
	articles = Article.objects.all()

	count = 0 #TESTING 
	for art in articles:
		id = art.id
		name = art.headline.encode('utf-8')
		text = name + " " + art.text.encode('utf-8')
		if len(text) > 0:
			sentiments.append((id, name, calc_sent(text)))
			
def main():
	global exclude 
	exclude = set(string.punctuation)
	global stop_words
	stop_words = stopwords.words('english')

	global sentiment_scores
	sentiment_scores = {}
	global sentiments
	sentiments = []

	get_sentiment_list()
	gen_sent()
	scores = sorted(sentiments,key=lambda x: x[2], reverse = True)
	with open('sentiment.csv', 'w') as csvfile:
		csv_writer = csv.writer(csvfile)
		for score in scores:
			csv_writer.writerow([score])

if __name__ == "__main__":
    main()