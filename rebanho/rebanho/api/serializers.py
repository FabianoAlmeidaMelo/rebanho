# -*- coding: utf-8 -*-
from rebanho.propriedades.models import AnimalPesagem
from rest_framework import serializers


class AnimalPesagemSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = AnimalPesagem
        fields = ('id',  'animal', 'data', 'peso')

