from django.shortcuts import render
from django.template import RequestContext
from django.http import Http404, HttpResponse

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


def timeline(request, search_params=None):
    if search_params is None:
        raise Http404('source not found')
    # TODO get articles from db, filter by params
    # TODO count articles per granularity
    # TODO build tsv
    return HttpResponse(search_params) 
