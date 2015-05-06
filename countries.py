import sys, os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "data_science_project.settings")
sys.path.append('/home/ubuntu/CS1951aFinalProj/')

from django.db import models
from news.models import *

import datetime

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
	city_coords[elts[2].lower().strip('\n')] = (float(elts[0]), float(elts[1]))

# City set is the keys of this dictionary
cities = city_coords.keys()
#for city in cities:
#	print city
print str(len(cities)) + ' cities'

##########################
# Add some more cities from another file
# This has a mapping from city to country if desired
new_cities = 0
cc_file = open('more_cities.csv')
cc_file.next()
for line in cc_file:
	elts = line.split(',')
	country = elts[1].lower().strip('"')
	city = elts[2].lower().strip('"')
	lat = float(elts[3].strip('"'))
	lon = float(elts[4].strip('"'))
	if not city in cities:
		city_coords[city] = (lat, lon)
		new_cities += 1

print 'glendale' in cities 
cities = city_coords.keys()
print new_cities
print str(len(cities)) + ' cities'

#for city in cities:
#	if 'x' in city:
#		print city


###################################################################
################# Find Trending cities/countries ##################
###################################################################

#output = open('results.csv', 'w+')
#output.write('lat,lon,name,radius,color')

source_names = {}

articles = Article.objects.all()
for i in xrange(10):
    txt = articles[i].text
    title = articles[i].headline
    source = articles[i].source.name
    if not source in source_names:
    	source_names[source] = 0
    source_names[source] += 1

print source_names


print 'DONE'
