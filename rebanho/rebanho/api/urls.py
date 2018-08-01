# coding: utf-8
from django.conf.urls import include, url
# from rest_framework import routers

from rebanho.api import views


urlpatterns = [
    url(r'^api-brinco_token_pesagens_list/(?P<brinco>[\w\-]+)/$', views.AnimalBrincoTokenPesagemList.as_view()),
    url(r'^api-brinco_auth_pesagens_list/(?P<brinco>[\w\-]+)/$', views.AnimalBrincoAuthPesagemList.as_view()),
    url(r'^api-cnpj_pesagens_list/(?P<cnpj>\d+)/$', views.AnimalCnpjPesagemList.as_view()),
]
