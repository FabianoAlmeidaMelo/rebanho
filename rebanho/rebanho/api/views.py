from django.shortcuts import render
from rebanho.propriedades.models import Animal, AnimalPesagem
from localbr.formfields import BRCNPJField
#### REST
from rest_framework import viewsets
from rebanho.api.serializers import AnimalPesagemSerializer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import serializers, generics


class AnimalCnpjPesagemList(generics.ListAPIView):
    """
    ref #14
    Consulta pesagens de Animais que estão no estoque,
    passando apenas o CNPJ da Fazenda
    """
    model = AnimalPesagem
    serializer_class = AnimalPesagemSerializer
    http_method_names = [u'get']

    def get_queryset(self):
        cnpj = self.kwargs['cnpj']
        cnpj_valdate = BRCNPJField(always_return_formated=True)
        try:
            cnpj_validado = cnpj_valdate.clean(cnpj)
        except:
            cnpj_validado=None
        queryset = self.model.objects.filter(animal__propriedade__cnpj=cnpj_validado,
                                             animal__saida=None)

        return queryset.order_by('-data')


class AnimalBrincoPesagemList(AnimalCnpjPesagemList):
    """
    ref #15
    Consulta as pesagens de um Animal
    passando o brinco e o Token
    """

    def get_queryset(self):
        brinco = self.kwargs['brinco']
        queryset = self.model.objects.filter(animal__brinco=brinco)

        return queryset.order_by('-data')
