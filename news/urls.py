from django.conf.urls import include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', 'news.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^source/(?P<source_id>[0-9]+)/{0,1}$', 'news.views.source', name='source'),
    url(r'^timeline/(?P<search_params>[^/]+)/{0,1}$', 'news.views.timeline', name='timeline'),
]
