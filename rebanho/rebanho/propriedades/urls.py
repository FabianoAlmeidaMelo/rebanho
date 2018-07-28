# coding: utf-8
from django.conf.urls import include, url

from rebanho.propriedades.views import (
    animal_form,
    animais_list,
    propriedade_form,
    propriedades_list,
)

urlpatterns = [
    # Animais
    url(r'^jetbov/animal_form/(?P<propriedade_pk>\d+)/$', animal_form, name='animal_form'),
    url(r'^jetbov/animal_form/(?P<propriedade_pk>\d+)/(?P<animal_pk>\d+)/$',animal_form, name='animal_form'),
    url(r'^jetbov/animais_list/(?P<propriedade_pk>\d+)/$', animais_list, name='animais_list'),
    # Propriedades
    url(r'^jetbov/propriedade_form/$', propriedade_form, name='propriedade_form'),
    url(r'^jetbov/propriedade_form/(?P<pk>\d+)/$',propriedade_form, name='propriedade_form'),
    url(r'^jetbov/propriedades_list/$', propriedades_list, name='propriedades_list'),
]
