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
from rest_framework import serializers


@csrf_exempt
def pesagens_list(request, cnpj):
    """
    ref #14
    Lista todas pesagens de uma Propriedade,
    filtra pelo CNPJ:
    exemplos:
    browser:
    http://localhost:8000/api-pesagens/61675372000102/
    Terminal:
    http http://localhost:8000/api-pesagens/61675372000102/
    """
    cnpj_valdate = BRCNPJField(always_return_formated=True)
    try:
        cnpj_validado = cnpj_valdate.clean(cnpj)
    except Exception as e:
        raise serializers.ValidationError(str(e))

    if request.method == 'GET' and cnpj_validado:
        pesagens = AnimalPesagem.objects.filter(animal__propriedade__cnpj=cnpj_validado).order_by('-data')
        serializer = AnimalPesagemSerializer(pesagens, many=True)
        return JsonResponse(serializer.data, safe=False)
