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

def get_corr_list(article_x):
	terms_x = Set(create_index.top_words(article_x, 0.2))

	corr_list = []
	articles = Article.objects.all()
	count = 0
	for art in articles: 
		print count
		if count > 5:
			break;
		count +=1
		if len(art.text) > 0:
			terms_y = Set(create_index.top_words(art, 0.2))
			terms_union = terms_x | terms_y
		
			v_x = [] #this is the vector of art_comp
			v_y = [] #vector for comparison article
			for word in terms_union: # [boolean words vector, sentiment*0.2]
				if word in terms_x:
					v_x.append(1)
				else:
					v_x.append(0)
			
				if word in terms_y:
					v_y.append(1)
				else:
					v_y.append(0)
		
			sent_x = get_sentiment.get_article_sentiment(article_x)
			if sent_x != None:
				v_x.append(sent_x*0.5)
			else:
				v_x.append(0)
		
			sent_y = get_sentiment.get_article_sentiment(art)
			if sent_y != None:
				v_y.append(sent_x*0.5)
			else:
				v_y.append(0)
		
			n = len(v_x)
			sum_x, sum_y, sum_xx, sum_xy, sum_yy = 0,0,0,0,0
			for i in range(0, n):
				sum_x += v_x[i]
				sum_y += v_y[i]
				sum_xx += v_x[i]*v_x[i]
				sum_yy += v_y[i]*v_y[i]
				sum_xy += v_x[i]*v_y[i]
			
			corr_val = regularized_correlation(n, sum_x, sum_y, sum_xx, sum_yy, sum_xy, VIRTUAL_COUNT, PRIOR_CORRELATION)
		
			corr_list.append((art.id, art.headline.encode('utf-8'), corr_val))
	
	return corr_list

def get_related_articles(article):
	corr_list = get_corr_list(article)

	corr_list = sorted(corr_list,key=lambda x: x[2], reverse = True)
	temp = []
	for i in xrange(1):
		temp.append(corr_list[i][0])
	return temp

def main():
	article_x = Article.objects.get(id=11) 

	corr_list = get_corr_list(article_x)

	corr_list = sorted(corr_list,key=lambda x: x[2], reverse = True)
	for i in range(0, 10):
		print corr_list[i]
	
if __name__ == "__main__":
    main()
