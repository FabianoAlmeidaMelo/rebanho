# coding: utf-8
from django.conf.urls import include, url

from rebanho.core.views import home

urlpatterns = [
    url(r'^$', home, name='home'),
]