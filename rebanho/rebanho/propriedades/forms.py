# coding: utf-8
from django import forms

from django.db.models import Q

from localbr.formfields import BRCNPJField

from rebanho.propriedades.models import (
    Propriedade,
)


class PropriedadeForm(forms.ModelForm):
    '''
    #7 Cadstro e Edição de Propriedade
    '''
    cnpj = BRCNPJField()  # *****
    nome = models.CharField(max_length=150)

    class Meta:
        model = Propriedade
        fields = ('cnpj',
                  'nome',
                  'nirf',
                  'incra',
                  'telefone',
                  'nome_contato')

