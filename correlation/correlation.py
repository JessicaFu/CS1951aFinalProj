from __future__ import division
import sys, os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "data_science_project.settings")
sys.path.append('/home/ubuntu/CS1951aFinalProj/')
import django
import create_index
django.setup()
from django.db import models
from news.models import *
import operator
import get_sentiment
from sets import Set
import string
import datetime
import operator
import csv
import porter_stemmer
import math
from nltk.corpus import stopwords

##### Metric Functions ############################################################################
VIRTUAL_COUNT = 5
PRIOR_CORRELATION = 0.0
		
def correlation(n, sum_x, sum_y, sum_xx, sum_yy, sum_xy):
	# http://en.wikipedia.org/wiki/Correlation_and_dependence
	numerator = n * sum_xy - sum_x * sum_y
	denominator = math.sqrt(n * sum_xx - sum_x * sum_x) * math.sqrt(n * sum_yy - sum_y * sum_y)
	if denominator == 0:
		return 0.0
	return numerator / denominator

def regularized_correlation(n, sum_x, sum_y, sum_xx, sum_yy, sum_xy, virtual_count, prior_correlation):
	unregularized_correlation_value = correlation(n, sum_x, sum_y, sum_xx, sum_yy, sum_xy)
	weight = n / (n + virtual_count)
	return weight * unregularized_correlation_value + (1 - weight) * prior_correlation

def cosine_similarity(sum_xx, sum_yy, sum_xy):
	# http://en.wikipedia.org/wiki/Cosine_similarity
	numerator = sum_xy
	denominator = (math.sqrt(sum_xx) * math.sqrt(sum_yy))
	if denominator == 0:
		return 0.0
	return numerator / denominator

def jaccard_similarity(n_common, n1, n2):
	# http://en.wikipedia.org/wiki/Jaccard_index
	numerator = n_common
	denominator = n1 + n2 - n_common
	if denominator == 0:
		return 0.0
	return numerator / denominator
	
###################################################################################################

##### Find TF.IDF ############################################################################

def get_tf_idf(id, word):
	total_terms = word_count[id]
	weight = 0

	t_count = 0
	d_count = 0
	
	if word in inverted_index:
		d_count = len(inverted_index[word])
		if id in inverted_index[word]:
			t_count = inverted_index[word][id]

	tf = t_count/total_terms
	idf = math.log(total_num_docs/d_count) 

	return tf*idf

def stem(word):	
	word = ''.join(ch for ch in word if ch not in exclude and ch.isalnum())
	word = word.lower()
	if not word in stop_words:
		word = porter_stemmer.PorterStemmer().stem(word, 0,len(word)-1)
		if len(word) > 0 and word != "\n" and word != "\r":
			return word
	return None

	
def get_list_tf_idf(article):
	keywords = Keyword.objects.filter(article__id=id)
	text = ""
	for key in keywords:
		text += key.word+ " "
		
	text += article.headline.encode('utf-8') + " " + article.text.encode('utf-8')
	words = get_words(text)
	id = article.id
	dict = {}
	for word in words:
		word = stem(word)
		if word != None:
			tf_idf = get_tf_idf(id, word)
			dict[word] = tf_idf
	
	sorted_list = sorted(dict.items(), key=operator.itemgetter(1), reverse = True)
	#top 20% tf.idf
	top = int(len(sorted_list) * 0.2)
	terms = []
	for i in range(0, top):
		word, weight = sorted_list[i]
		terms.append(word)
	
	return terms

def get_corr_list(art_comp):
	
	terms_comp = Set(get_list_tf_idf(art_comp))

	corr_list = []
	articles = Article.objects.all()
	for art in articles: 
		art_terms = Set(get_list_tf_idf(article))
		terms_union = terms_comp | art_terms
		
		v_x = [] #this is the vector of art_comp
		v_y = [] #vector for comparison article
		for word in terms_union: # [boolean words vector, sentiment*0.5]
			if word in terms_comp:
				v_x.append(1)
			else:
				v_x.append(0)
			
			if word in art_terms:
				v_y.append(1)
			else:
				v_y.append(0)
		
		sent_x = get_sentiment.get_art_sent(art_comp)
		if sent_x != None:
			v_x.append(sent_x*0.5)
		else:
			v_x.append(0)
		
		sent_y = get_sentiment.get_art_sent(art)
		if sent_y != None:
			v_y.append(sent_x*0.5)
		else:
			v_y.append(0)
			
		#TODO add in news sources as well in vector
		
		n = len(v_x)
		sum_x, sum_y, sum_xx, sum_xy, sum_yy = 0,0,0,0,0
		for i in range(0, len(v_x)):
			sum_x += v_x[i]
			sum_y += v_y[i]
			sum_xx += v_x[i]*v_x[i]
			sum_yy += v_y[i]*v_y[i]
			sum_xy += v_x[i]*v_y[i]
			
		corr_val = regularized_correlation(n, sum_x, sum_y, sum_xx, sum_yy, sum_xy, VIRTUAL_COUNT, PRIOR_CORRELATION)
		
		corr_list.append((art.id, art.headline.encode('utf-8'), corr_val))
	
	return corr_list
		
def main():
	global inverted_index 
	inverted_index = create_index.get_index()
	global sentiment_scores
	sentiment_scores = get_sentiment.get_sentiment_list()
	
	art_comp = Article.objects.filter(id="22302L")
	corr_list = get_corr_list(art_comp)
	corr_list_sorted = sorted(weights,key=lambda x: x[2], reverse = True)
	for i in range(0, 10):
		print corr_list_sorted[i]
	
if __name__ == "__main__":
    main()