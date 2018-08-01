from django.shortcuts import render
from rebanho.propriedades.models import AnimalPesagem
from localbr.formfields import BRCNPJField
#### REST
from rest_framework import viewsets
from rebanho.api.serializers import AnimalPesagemSerializer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import serializers, generics


class AnimalPesagemList(generics.ListAPIView):
    """
    ref #14 consulta pesagens de Animais
    que estão no estoque, passando apenas o CNPJ da
    Fazenda
    """
    model = AnimalPesagem
    serializer_class = AnimalPesagemSerializer

    def get_queryset(self):
        cnpj = self.kwargs['cnpj']
        cnpj_valdate = BRCNPJField(always_return_formated=True)
        cnpj_validado = cnpj_valdate.clean(cnpj)
        queryset = self.model.objects.filter(animal__propriedade__cnpj=cnpj_validado,
                                             animal__saida=None)

        return queryset.order_by('-data')

