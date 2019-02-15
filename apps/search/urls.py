from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^query_api$', views.query_api, name='query_api'),
    url(r'^filter_search$', views.filter_search, name='filter_search'),
    url(r'^needs_search/(?P<term>[\w\-]+)/(?P<location>[\w\-]+)/$', views.needs_search, name='needs_search'),
    url(r'^query_business/(?P<id>[\w\-]+)/$', views.query_business, name='query_business'),
]