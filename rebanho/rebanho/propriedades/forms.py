# coding: utf-8
from django import forms

from django.db.models import Q

from localbr.formfields import BRCNPJField

from rebanho.propriedades.models import (
    Propriedade,
)


class PropriedadeForm(forms.ModelForm):
    '''
    #7 Cadastro e Edição de Propriedade
    '''
    cnpj = BRCNPJField(always_return_formated=True)
    nome = forms.CharField(max_length=150)

    class Meta:
        model = Propriedade
        fields = ('cnpj',
                  'nome',
                  'nirf',
                  'incra',
                  'telefone',
                  'nome_contato')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PropriedadeForm, self).__init__(*args, **kwargs)



class PropriedadeSearchForm(forms.Form):
    '''
    #7 Filtro na listagem de propriedades
    '''
    nome = forms.CharField(label=u'Nome', required=False)
    cnpj = forms.CharField(label=u'CNPJ', required=False)

    def __init__(self, *args, **kargs):
        self.user = kargs.pop('user', None)
        super(PropriedadeSearchForm, self).__init__(*args, **kargs)
       

    def get_result_queryset(self):
        qs = self.user.propriedadeuser_set.all().values_list('propriedade__id', flat=True)
        q = Q(id__in=qs)
        if self.is_valid():
            nome = self.cleaned_data['nome']
            if nome:
                q = q & Q(nome__icontains=nome)
            cnpj = self.cleaned_data['cnpj']
            if cnpj:
                q = q & Q(cnpj__icontains=cnpj)

        return Propriedade.objects.filter(q)