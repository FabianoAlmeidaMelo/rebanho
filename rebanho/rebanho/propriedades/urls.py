# coding: utf-8
from django.conf.urls import include, url
from rest_framework import routers

from rebanho.propriedades.views import (
    animal_form,
    animais_list,
    animal_pesagem_form,
    propriedade_form,
    propriedades_list,
    # REST:
    pesagens_list, 
)

urlpatterns = [
    # ## REST
    url(r'^api-pesagens/(?P<cnpj>\d+)/$', pesagens_list),
    # ## django
    # Animais
    url(r'^jetbov/animal_form/(?P<propriedade_pk>\d+)/$', animal_form, name='animal_form'),
    url(r'^jetbov/animal_form/(?P<propriedade_pk>\d+)/(?P<animal_pk>\d+)/$',animal_form, name='animal_form'),
    url(r'^jetbov/animais_list/(?P<propriedade_pk>\d+)/$', animais_list, name='animais_list'),
    # Propriedades
    url(r'^jetbov/propriedade_form/$', propriedade_form, name='propriedade_form'),
    url(r'^jetbov/propriedade_form/(?P<pk>\d+)/$',propriedade_form, name='propriedade_form'),
    url(r'^jetbov/propriedades_list/$', propriedades_list, name='propriedades_list'),
    # # animal_pesagem_form
    url(r'^jetbov/animal_pesagem_form/(?P<animal_pk>\d+)/$', animal_pesagem_form, name='animal_pesagem_form'),

]
