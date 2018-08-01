# coding: utf-8
from django.conf.urls import include, url
# from rest_framework import routers

from rebanho.api.views import (
    AnimalPesagemList,

)

urlpatterns = [
    url(r'^api-pesagens_list/(?P<cnpj>\d+)/$', AnimalPesagemList.as_view()),
]


# http://localhost:8000/api-token-auth/{ 'username': 'falmeidamelo@uol.com.br', 'password': '1' }/
# Authorization: Token 04d6f09894d03d6268e69240a597ba3ad9f7e1a0

# http://127.0.0.1:8000/ -H 'Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'

# http://localhost:8000/api-pesagens/61675372000102/