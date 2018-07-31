# coding: utf-8
from django.conf.urls import include, url

from rebanho.propriedades.views import (
    animal_form,
    animais_list,
    animal_pesagem_form,
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
    # # animal_pesagem_form
    url(r'^jetbov/animal_pesagem_form/(?P<animal_pk>\d+)/$', animal_pesagem_form, name='animal_pesagem_form'),

]

# http://localhost:8000/api-token-auth/{ 'username': 'falmeidamelo@uol.com.br', 'password': '1' }/
# Authorization: Token 04d6f09894d03d6268e69240a597ba3ad9f7e1a0

# http://127.0.0.1:8000/ -H 'Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'

# http://localhost:8000/api-pesagens/61675372000102/
