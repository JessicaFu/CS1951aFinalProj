from django.shortcuts import render
from django.template import RequestContext
from django.http import Http404, HttpResponse
import datetime
import csv

from models import *
# Create your views here.

def home(request):
    context = RequestContext(request, {})
    return render(request, 'home.html', context)

def source(request, source_id=None):

    if source_id is None:
        raise Http404('source not found')

    articles = []
    source = Source.objects.get(id=source_id).name
    for art in Article.objects.all().filter(source_id=source_id):
        articles.append((art.headline, art.date))

    context = RequestContext(request, {
        'source_name' : source,
        'articles' : articles
    })
    return render(request, 'source.html', context)

def timeline(request, keyword=None, begin_date=None, end_date=None):
    if not (request and begin_date and end_date):
        raise Http404('endpoint not properly formatted')

    time_convert_str = "%Y%m%d"
    begin_date = datetime.datetime.strptime(begin_date, time_convert_str)

    end_date = datetime.datetime.strptime(end_date, time_convert_str)
    articles = Article.objects.filter(keyword__word=keyword,
            date__gte=begin_date,
            date__lte=end_date)

    response = HttpResponse(content_type='text/tsv')
    response['Content-Disposition'] = 'attachment; filename="linedata.tsv"'

    writer = csv.writer(response, delimiter='\t')
    header = ['date', 'headline', 'url', 'source']
    writer.writerow(header)
    for article in articles:
        row = [article.date.strftime(time_convert_str),
                article.headline,
                article.url,
                article.source.name]
        writer.writerow([s.encode("utf-8") for s in row])

    return response

