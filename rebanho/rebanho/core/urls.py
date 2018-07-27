# coding: utf-8
from django.conf.urls import include, url

from rebanho.core.views import (
	home,
    usuarios_list,
    usuario_form,
)

urlpatterns = [
	url(r'^$', home, name='home'),
    # User
    url(r'^jetbov/usuario_form/$', usuario_form, name='usuario_form'),
    url(r'^jetbov/usuario_form/(?P<pk>\d+)/$',usuario_form, name='usuario_form'),
    url(r'^jetbov/usuarios_list/$', usuarios_list, name='usuarios_list'),
]
