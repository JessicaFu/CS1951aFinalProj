from django.shortcuts import render
from django.template import RequestContext
# Create your views here.

def home(request):
    context = RequestContext(request, {})
    return render(request, 'home.html', context)
