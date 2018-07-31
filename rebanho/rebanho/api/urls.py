# coding: utf-8
from django.conf.urls import include, url
# from rest_framework import routers

from rebanho.api.views import (
    pesagens_list, 
)

urlpatterns = [
    url(r'^api-pesagens/(?P<cnpj>\d+)/$', pesagens_list),
]
