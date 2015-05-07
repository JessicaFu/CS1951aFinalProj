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
source_city = {'Huffington Post': {},
               'Al Jazeera': {}, 
               'BBC': {}, 
               'The Chronicle': {}, 
               'CNN': {}, 
               'Herald Sun': {}, 
               'The Onion': {}, 
               'The Washington Post': {} }
source_country = {'Huffington Post': {},
                  'Al Jazeera': {}, 
                  'BBC': {}, 
                  'The Chronicle': {}, 
                  'CNN': {}, 
                  'Herald Sun': {}, 
                  'The Onion': {}, 
                  'The Washington Post': {} }

articles = Article.objects.all()
for art in articles: 
    txt = art.text.encode('utf-8') 
    title = art.headline.encode('utf-8') 
    source = art.source.name.encode('utf-8') 

    if not source in source_names:
    	source_names[source] = 0
    source_names[source] += 1
    # Look through the article's text for country names
    for country in countries:
        if country in title.lower() or country in txt.lower():
            if not country in country_counts:
                country_counts[country] = 0
            country_counts[country] += 1
            if not country in source_country[source]:
                source_country[source][country] = 0
            source_country[source][country] += 1
    # Repeat the process for cities
    for city in cities:
        if city in title.lower().split() or city in txt.lower().split():
            if not city in city_counts:
                city_counts[city] = 0
            city_counts[city] += 1
            if not city in source_city[source]:
                source_city[source][city] = 0
            source_city[source][city] += 1

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
print '-------------------------'
print source_city
print '-------------------------'
print source_country
<<<<<<< HEAD

######################################################################
#################### Write CSV Files #################################
######################################################################

all_cities = open('all_cities.csv', 'w+')
all_cities.write('lat,lon,name,count\n')
for city in city_counts.keys():
    (lat,lon) = city_coords[city]
    count = city_counts[city]
    all_cities.write(str(lat)+','+str(lon)+','+city+','+str(count)+'\n')

all_countries = open('all_countries.csv', 'w+')
all_countries.write('lat,lon,name,count\n')
for country in country_counts.keys():
    (lat,lon) = country_coords[country]
    count = country_counts[country]
    all_countries.write(str(lat)+','+str(lon)+','+country+','+str(count)+'\n')

sep_cities = open('separate_cities.csv', 'w+')
sep_cities.write('lat,lon,name,city,source\n')
for source in source_city.keys():
    for city in (source_city[source]).keys():
        (lat,lon) = city_coords[city]
        count = source_city[source][city]
        sep_cities.write(str(lat)+','+str(lon)+','+city+','+str(count)+','+source+'\n') 

sep_countries = open('separate_countries.csv', 'w+')
sep_countries.write('lat,lon,name,count,source\n')
for source in source_country.keys():
    for country in (source_country[source]).keys():
        (lat,lon) = country_coords[country]
        count = source_country[source][country]
        sep_countries.write(str(lat)+','+str(lon)+','+country+','+str(count)+','+source+'\n')

source_counts = open('source_counts.csv', 'w+')
source_counts.write('name,count\n')
for source in source_names.keys():
    count = source_names[source]
    source_counts.write(source+','+str(count)+'\n')
=======
>>>>>>> 2e565a8586cb925bbc4203fee33f632df439bfac

print 'DONE'
