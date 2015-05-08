from django.shortcuts import render
from django.template import RequestContext
from django.http import Http404, HttpResponse, JsonResponse

from collections import defaultdict
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



def timeline(request, keywords=None, begin_date=None, end_date=None, type=None):
    if not (request and begin_date and end_date):
        raise Http404('endpoint not properly formatted')

    time_convert_str = "%Y%m%d"
    begin_date = datetime.datetime.strptime(begin_date, time_convert_str)
    end_date = datetime.datetime.strptime(end_date, time_convert_str)

    articles = set()
    for keyword in keywords.split():
        art_set = Article.objects.filter(keyword__word=keyword,
            date__gte=begin_date,
            date__lte=end_date)
        for art in art_set:
            articles.add(art)

    if type == "tsv":
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
    else:
        arts = [{'headline' : article.headline,
                     'url' : article.url,
                     'date' : article.date.strftime(time_convert_str),
                     'source' : article.source.name} for article in articles]
        
        sources = Source.objects.all()
        
        d3_data = defaultdict(lambda: {src.name : 0 for src in sources})

        date_delta = end_date - begin_date
        for i in xrange(date_delta.days + 1):
            d3_data[(begin_date + datetime.timedelta(days=i)).strftime(time_convert_str)][sources[0].name] = 0

        for article in articles:
            d3_data[article.date.strftime(time_convert_str)][article.source.name] += 1

        d3_data_list = []
        for key, value in d3_data.iteritems():
            value['date'] = key
            d3_data_list.append(value)

        d3_data_list.sort(key=lambda x: x['date'])

        res_dict = {
            'sources' : [src.name for src in sources],
            'articles' : arts,
            'd3' : d3_data_list
        } 

        response = JsonResponse(res_dict)
        return response

