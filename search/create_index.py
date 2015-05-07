import sys, os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "data_science_project.settings")
sys.path.append('/home/ubuntu/CS1951aFinalProj/')

from django.db import models
from news.models import *

import string
import datetime
import operator
import csv
import porter_stemmer
from nltk.corpus import stopwords

index = {}
stop_words = []

def get_stop_words():	
	stop_words = stopwords.words('english')
	
def get_words(article):
	words = article.headline + " "
			+ article.source.name + " "
			+ article.text
	
	#TODO need to be able to quantify date metadata
	
	words = words.split(" ")
	proc_words = []
	for word in words:
		if not word in stop_words:
			word = word.lower()
			word = porter_stemmer.PorterStemmer().stem(word, 0,len(word)-1)
			word = word.translate(word.maketrans("",""), string.punctuation)
			proc_words.append(word)
	
def create_inverted_index(article):
	id = article.id
	words = get_words(article)
	for word in words:
		if not word in inverted_index:
			inverted_index[word] = [];
			inverted_index[word].append({index: 1})
		else:
			inverted_index[word][index] = inverted_index[word][index] + 1
			
def main():
	get_stop_words()
	
	articles = Article.objects.all()
	
	count = 0 #TESTING 
	for art in articles: 
		if count > 10:
			break	
		create_inverted_index(art)
		count += 1
		
	#TESTING
	with open('search_data.csv', 'w') as csvfile:
		csv_writer = csv.writer(csvfile)
		for key in inverted_index:
			csv_writer.writerow([key,inverted_index[key]])

if __name__ == "__main__":
    main()