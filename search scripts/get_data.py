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

with open('search_data.csv', 'w') as csvfile:
	csv_writer = csv.writer(csvfile)
	csv_writer.writerow([])

articles = Article.objects.all()
count = 0
for art in articles: 	
	print art
###################################################################
################# Find Trending cities/countries ##################
###################################################################

#output = open('results.csv', 'w+')
#output.write('lat,lon,name,radius,color')

source_names = {}
country_counts = {}
city_counts = {}

articles = Article.objects.all()
for art in articles: #i in xrange(1000):
    txt = art.text.encode('utf-8') #articles[i].text
    title = art.headline.encode('utf-8') #articles[i].headline
    source = art.source.name.encode('utf-8') #articles[i].source.name
    #print title
    if not source in source_names:
    	source_names[source] = 0
    source_names[source] += 1
    for country in countries:
        if country in title.lower() or country in txt.lower():
            if not country in country_counts:
                country_counts[country] = 0
            country_counts[country] += 1
    for city in cities:
        #for word in title.split(' '):        
            #if city in title.lower()
        if city in title.lower().split() or city in txt.lower().split():
            if not city in city_counts:
                city_counts[city] = 0
            city_counts[city] += 1

sorted_countries = sorted(country_counts.items(), key=lambda x:x[1], reverse=True)
sorted_cities = sorted(city_counts.items(), key=lambda x:x[1], reverse=True)
print len(city_counts)
if 'baltimore' in city_counts:
    print 'baltimore: ' + str(city_counts['baltimore'])
for i in range(10):
    print sorted_countries[i]
for i in range(10):
    print sorted_cities[i]
print source_names

print '-------------------------'
print sorted_countries
print '-------------------------'
print sorted_cities

print 'DONE'
