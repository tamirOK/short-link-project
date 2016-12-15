from django.conf.urls import url
from . import views
__author__ = 'nezumi'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^serve$', views.serve, name='serve'),
    url(r'^(?P<query>[^/]+)/$', views.open, name='open'),
    url(r'^get_uri$', views.get_uri, name='get_uri'),
]
