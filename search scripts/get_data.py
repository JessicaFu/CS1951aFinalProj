import sys, os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "data_science_project.settings")
sys.path.append('/home/ubuntu/CS1951aFinalProj/')

from django.db import models
from news.models import *

import datetime
import operator
import csv

##########################################################################
################# Retrieve Article metadata ##############################
##########################################################################
index = {}

def get_inverted_index(article):
	print art.headline
	print art.source.name

	index = art.id
	name = art.source.name
	name.split(" ")
	if 

def main():
	
	with open('search_data.csv', 'w') as csvfile:
		csv_writer = csv.writer(csvfile)
		csv_writer.writerow([])

	articles = Article.objects.all()
	count = 0 #TESTING 
	for art in articles: 
		if count > 10:
			break	
		get_inverted_index(art)
		count += 1

if __name__ == "__main__":
    main()