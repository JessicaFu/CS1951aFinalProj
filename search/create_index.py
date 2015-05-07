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
import csv
import porter_stemmer
import math
from nltk.corpus import stopwords


def get_idf(id, words):
	total_terms = word_count[id]
	weight = 0

	for word in words:
		t_count = 0
		d_count = 0
		
		if word in inverted_index:
			d_count = len(inverted_index[word])
			if id in inverted_index[word]:
				t_count = inverted_index[word][id]

		tf = t_count/total_terms
		
		idf = math.log(total_num_docs/d_count) 

		weight += tf*idf

	return weight

def search(text):
	words = get_words(text)
	
	articles = Article.objects.all()
	for art in articles: 
		if len(art.text) >0:
			name = art.headline.encode('utf-8')
			idf = get_idf(id, words)
			weights.append((id, name, idf))
			
	
def get_words(text):	
	words = text.split()
	proc_words = []
	for word in words:
		word = ''.join(ch for ch in word if ch not in exclude and ch.isalnum())
		word = word.lower()
		if not word in stop_words:
			word = porter_stemmer.PorterStemmer().stem(word, 0,len(word)-1)
			if len(word) > 0 and word != "\n" and word != "\r":
				proc_words.append(word)
	return proc_words

def put_in_index(word, id, weight):
	#TODO put in positional index instead!

	if not word in inverted_index:
		inverted_index[word] = [];
		inverted_index[word] = {id: weight}
	elif not id in inverted_index[word]:
		inverted_index[word][id] = weight
	else:
		inverted_index[word][id] = inverted_index[word][id] + weight

def create_inverted_index(article):
	id = article.id

	#TODO need to be able to quantify date metadata
	#TODO need to quantify keyword data

	total_count = 0

	text = article.headline.encode('utf-8')
	words = get_words(text)
	total_count += len(words)
	for word in words:
		put_in_index(word, id, 2)

	text = article.text.encode('utf-8') 
	words = get_words(text)
	total_count += len(words)
	for word in words:
		put_in_index(word, id, 1)
	
	keywords = Keyword.objects.filter(article__id=id)
	text = ""
	for key in keywords:
		text += key.word+ " "

	words = get_words(text)
	total_count += len(words)
	for word in words:
		put_in_index(word, id, 5)

	word_count[id] = total_count

def index():
	articles = Article.objects.all()
	global total_num_docs
	total_num_docs = 0

	for art in articles: 
		if len(art.text) >0:
			create_inverted_index(art)
			
def main():
	global inverted_index 
	inverted_index = {}
	global exclude 
	exclude = set(string.punctuation)
	global word_count
	word_count = {}
	global stop_words
	stop_words = stopwords.words('english')
	global weights
	weights = []

	#TODO fix duplicate article entries
	index();
	text = "nepal survivors"
	search(text);
	weights = sorted(weights,key=lambda x: x[2], reverse = True)

	with open('search_data.csv', 'w') as csvfile:
		csv_writer = csv.writer(csvfile)
		csv_writer.writerow([text])
		for weight in weights:
			csv_writer.writerow([weight])

if __name__ == "__main__":
    main()