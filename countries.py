import sys, os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "data_science_project.settings")
sys.path.append('/home/ubuntu/CS1951aFinalProj/')

from django.db import models
from news.models import *

import datetime
import operator

##########################################################################
################# Build a collection of cities/countries #################
##########################################################################

# Create a dictionary of countries along w/ their (lat,lon) coordinates
country_coords = {}
country_file = open('countries.tsv')
country_file.next()
country_file.next()
for line in country_file:
	elts = line.split('\t')
	country_coords[elts[3].lower().strip('\n')] = (float(elts[1]), float(elts[2]))

# Set of countries set to be keys of dictionary
countries = country_coords.keys()

# Dictionary of cities in the world along w/ their (lat,lon) coordinates
city_coords = {}
city_file = open('cities_big.csv')
city_file.next()
for line in city_file:
    elts = line.split(',')
    if elts[2].lower().strip('\n') == 'man':
        print line
    city_coords[elts[2].lower().strip('\n')] = (float(elts[0]), float(elts[1]))

# City set is the keys of this dictionary
cities = city_coords.keys()
cities.remove('')
cities.remove('man')
#for city in cities:
#	print city
print str(len(cities)) + ' cities'

##########################
# Add some more cities from another file
# This has a mapping from city to country if desired
#city_coords = {}
#cities = []
#new_cities = 0
#cc_file = open('more_cities.csv')
#cc_file.next()
#for line in cc_file:
#	elts = line.split(',')
#	country = elts[1].lower().strip('"')
#	city = elts[2].lower().strip('"')
#	lat = float(elts[3].strip('"'))
#	lon = float(elts[4].strip('"'))
#	if not city in cities:
#		city_coords[city] = (lat, lon)
#		new_cities += 1

#print 'man' in cities 
#cities = city_coords.keys()
#print new_cities
#print str(len(cities)) + ' cities'

#for city in cities:
#	if 'x' in city:
#		print city


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
