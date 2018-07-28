# coding: utf-8
from django import forms

from django.db.models import Q
from django.forms.utils import ErrorList
from localbr.formfields import BRCNPJField

from rebanho.propriedades.models import (
    CHOICE_SEXO,
    Animal,
    Propriedade,
    PropriedadeUser,
)


class AnimalForm(forms.ModelForm):
    '''
    #8 Cadastro e Edição de Animais
    '''

    class Meta:
        model = Animal
        exclude = ('propriedade',
                   'date_joined')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.propriedade = kwargs.pop('propriedade', None)
        super(AnimalForm, self).__init__(*args, **kwargs)
        #
        self.fields['sexo'].initial = 1

    def clean(self):
        cleaned_data = super(AnimalForm, self).clean()
        saida = cleaned_data['saida']
        motivo_saida = cleaned_data['motivo_saida']
        brinco = self.cleaned_data['brinco']

        if Animal.objects.filter(brinco=brinco, propriedade=self.propriedade).exclude(pk=self.instance.pk).count():
            self.errors['brinco'] = ErrorList([u'Esse brinco já consta nos seus registros'])
        if saida and not motivo_saida:
            self.errors['motivo_saida'] = ErrorList([u'Se preencher a Data de Saída, o Motivo será requerido'])
        
        return cleaned_data


    def save(self, *args, **kwargs):
        self.instance.propriedade = self.propriedade
        instance = super(AnimalForm, self).save(*args, **kwargs)
        instance.save()

        return instance


class AnimalSearchForm(forms.Form):
    '''
    #8 Filtro na listagem de propriedades
    '''
    brinco = forms.CharField(label=u'Nr Brinco', required=False)
    sexo = forms.ChoiceField(label="Sexo", choices=CHOICE_SEXO[1:], widget=forms.RadioSelect(), required=False)
    mostrar = forms.BooleanField(label="Mostra somente animais que já não estão no estoque", required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.propriedade = kwargs.pop('propriedade', None)
        super(AnimalSearchForm, self).__init__(*args, **kwargs)
       

    def get_result_queryset(self):

        q = Q(propriedade=self.propriedade)
        if self.is_valid():
            sexo = self.cleaned_data['sexo']
            if sexo:
                q = q & Q(sexo=sexo)
            brinco = self.cleaned_data['brinco']
            if brinco:
                q = q & Q(brinco__icontains=brinco)
            mostrar = self.cleaned_data['mostrar']
            if mostrar:
                q = q & Q(motivo_saida__isnull=False)
            else:
                q = q & Q(motivo_saida=None)
            return Animal.objects.filter(q)

        return Animal.objects.filter(q, motivo_saida=None)


class PropriedadeForm(forms.ModelForm):
    '''
    #7 Cadastro e Edição de Propriedade
    '''
    cnpj = BRCNPJField(always_return_formated=True)
    nome = forms.CharField(label="Nome da Propriedade", max_length=150)

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

    def save(self, *args, **kwargs):
        is_new = False
        if not self.instance.pk:
            is_new = True
        instance = super(PropriedadeForm, self).save(*args, **kwargs)
        if is_new:
            PropriedadeUser.objects.get_or_create(propriedade=instance,
                                                  user=self.user,
                                                  owner=True)

        instance.save()

        return instance


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