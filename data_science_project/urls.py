from django.conf.urls import include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', 'news.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
]
