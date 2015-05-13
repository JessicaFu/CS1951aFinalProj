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

######################### create index #########################################
def get_words(text):	
	exclude = set(string.punctuation)
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
	row = PosIndex.objects.filter(word = word, article = article)
	if row != None:
		newRow = PosIndex(word = word, article = article, count = weight)
		newRow.save()
	else:
		row.count += weight
		row.save()


def add_to_index(article):
	total_count = 0
	id = article.id
	text = article.headline.encode('utf-8') + article.date.strftime("%B %d")
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

	article.word_count = total_count
	article.save()

def get_index(article):
	if article == None:
		articles = Article.objects.all()
		
		
		count = 0
		for art in articles: 
			print count
			if len(art.text)>0 and count >= 2127:
				add_to_index(art)
			count +=1
			
	else:
		add_to_index(article)

##########################search functions #################################
def get_tf_idf(article, words):
	total_terms = article.word_count
	total_num_docs = Article.objects.count()
	score = 0

	for word in words:
		t_count = 0
		
		rows = PosIndex.objects.filter(word = word)
		d_count = rows.count()
                t_count = rows.filter(article=article).count()

		if rows:
			tf = t_count/total_terms
		
			idf = math.log(total_num_docs/d_count) 

			score += tf*idf

	return score

def search(query, begin_date, end_date):
	words = get_words(query)
	ranking = []
        print words
	articles = Article.objects.filter(
            posindex__word=words[0],
            date__gte=begin_date,
            date__lte=end_date)
	for art in articles: 
		if len(art.text) >0:
			tf_idf = get_tf_idf(art, words)
			ranking.append((art, tf_idf))
	
	ranking = sorted(ranking,key=lambda x: x[1], reverse=True)
	temp = []
	for art, tf_idf in ranking:
            if tf_idf > .1:
	        temp.append(art)
            else:
                break
	return temp

########################correlation functions###########################

def top_words(article, percent):
	ranked_words = []

	keywords = Keyword.objects.filter(article__id=article.id)
	text = ""
	for key in keywords:
		text += key.word+ " "
	words = get_words(text)
	for word in words:
		tf_idf = get_tf_idf(article, [word])
		ranked_words.append((word, tf_idf))

	text = article.headline.encode('utf-8')
	words = get_words(text)
	for word in words:
		tf_idf = get_tf_idf(article, [word])
		ranked_words.append((word, tf_idf))

	text = article.text.encode('utf-8')
	words = get_words(text)
	for word in words:
		tf_idf = get_tf_idf(article, [word])
		ranked_words.append((word, tf_idf))	


	ranked_words = sorted(top_words,key=lambda x: x[1], reverse = True)

	top = int(len(sorted_list) * percent)
	terms = []
	for i in range(0, top):
		word, weight = sorted_list[i]
		terms.append(word)
	
	return terms

##############################main function###############################
def main():

	#print PosIndex.objects.count()

	#get_index(None);

#	articles = Article.objects.all()
#	count = 0
#	for art in articles:
#		if count > 10:
#			break
#		if len(art.text) >0:
#			print art.id, art.headline,art.word_count, art.sentiment_score
#		count += 1

	query = "nepal survivors"
	ranking = search(query, datetime.datetime.strptime('20150418','%Y%m%d'), 
            datetime.datetime.now())
	for rank in ranking:
		print ranking[1], ranking[0].headline

if __name__ == "__main__":
    main()








