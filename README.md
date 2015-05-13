# CS1951aFinalProj
This is our CS1951a final project . Here is the proposal: https://docs.google.com/a/brown.edu/document/d/1i7cThgjF-G4haqI_lb8G3FVNm1OuJHfTlMfAjAYxiPI/edit?usp=sharing

Inside this directory you can find the following important files:

- news/models.py : The schema and some helper functions to interface with the database
- news/views.py : Responds to incoming urls to produce the web pages and json
- news/templates/home.html : The homepage html and javascript.
- news/templates/base.html : Html and javascript relevant to all pages (although we currently only have one, home.html).
- scrapers/ : Contains all the scraper scripts for the different news sources and reddit. Twitter is non-functional and unused.
- search/create_index.py : Creates a search index and provides the search function to search the index. Currently unused in favor of a faster table based lookup in the Keywords table.
- correlation/correlation.py : Creates recommendations based on the search index and other parameters.
- countries.py : Used to create the heat map.
- sentiment/get_sentiment.py : Adds sentiment scores to all the articles collected.
- dataScienceNormals.m : Used to generate the normal distributions for each source.

Database access:
Since the project was hosted publicly on github we shared the database username and password internally and without adding it to the directory. Feel free to email James Laskey if you would like database access.
