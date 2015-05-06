import sys, os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "data_science_project.settings")
sys.path.append('/home/ubuntu/CS1951aFinalProj/')

from django.db import models
from news.models import *

import newspaper
import re
import datetime

def main():
    articles = Article.objects.all()
    for i in xrange(10):
        print articles[i].text
        print articles[i].headline
        print articles[i].source.name

if __name__ == "__main__":
    main()

print 'DONE'
