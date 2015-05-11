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


def get_tf_idf(id, words):
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
			id = art.id
			name = art.headline.encode('utf-8')
			idf = get_tf_idf(id, words)
			weights.append((id, name, idf, art.text))
			
	
def get_words(text):	
	words = text.split()
	proc_words = []
	for word in words:
		word = ''.join(ch for ch in word if ch not in exclude and ch.isalnum())
		word = word.lower()
		#if not word in stop_words:
		word = porter_stemmer.PorterStemmer().stem(word, 0,len(word)-1)
		if len(word) > 0 and word != "\n" and word != "\r":
			proc_words.append(word)
	return proc_words

def add_to_table(word, article, weight):
	row = PosIndex.objects.filter(word = word, article = article, weight = weight)
	if row != None:
		PosIndex(word = word, article = article, count = 1, weight = weight)	
	else:
		row.count += row.count

	row.save


def add_to_index(article):
	#TODO need to be able to quantify date metadata
	global inverted_index 
	inverted_index = {}
	global exclude 
	exclude = set(string.punctuation)
	global word_count
	word_count = {}


	total_count = 0
	id = article.id
	text = article.headline.encode('utf-8')
	words = get_words(text)
	total_count += len(words)
	for word in words:
		add_to_table(word, article, 2)

	text = article.text.encode('utf-8') 
	words = get_words(text)
	total_count += len(words)
	for word in words:
		add_to_table(word, article, 1)
	
	keywords = Keyword.objects.filter(article__id=id)
	text = ""
	for key in keywords:
		text += key.word+ " "

	words = get_words(text)
	total_count += len(words)
	for word in words:
		add_to_table(word, article, 5)

	article.count = total_count
	article.save()

"""
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
		put_in_index(word, id, 8)

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
		put_in_index(word, id, 8)

	word_count[id] = total_count
"""

def get_index():
	articles = Article.objects.all()

	for art in articles: 
		if len(art.text) >0:
			add_to_index(article)

def main():
	#TODO fix duplicate article entries
	get_index();

if __name__ == "__main__":
    main()

