# coding: utf-8
from django.conf.urls import include, url

from rebanho.propriedades.views import (
    propriedade_form,
    propriedades_list,
)

urlpatterns = [
    # Propriedades
    url(r'^jetbov/propriedade_form/$', propriedade_form, name='propriedade_form'),
    url(r'^jetbov/propriedade_form/(?P<pk>\d+)/$',propriedade_form, name='propriedade_form'),
    url(r'^jetbov/propriedades_list/$', propriedades_list, name='propriedades_list'),
]
