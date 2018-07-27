# coding: utf-8
from django import forms
from django.contrib.auth.forms import AuthenticationForm as AuthAuthenticationForm
from django.db.models import Q
from rebanho.core.models import (
    User,
)

class AuthenticationForm(AuthAuthenticationForm):
    keep_me_logged_in = forms.BooleanField(
                                            label=u'Mantenha-me conectado',
                                            required=False
                                        )
class UserForm(forms.ModelForm):
    '''
    #4 Cadstyro e Edição de User
    '''
    email = forms.EmailField(label='email', required=True)
    nome = forms.CharField(label='nome', required=True)

    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='Confirmação da Senha', widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        exclude = ('date_joined', 'is_active', 'password', 'username')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(UserForm, self).__init__(*args, **kwargs)


    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords diferentes")
        elif password1 and not password2:
            raise forms.ValidationError("Confirme a senha")
        return password2


class UserSearchForm(forms.Form):
    '''
    #4 Filtro na listagem de usuários
    '''
    nome = forms.CharField(label=u'Nome', required=False)
    email = forms.CharField(label=u'email', required=False)

    def __init__(self, *args, **kargs):
        self.escola = kargs.pop('escola', None)
        super(UserSearchForm, self).__init__(*args, **kargs)
       

    def get_result_queryset(self):
        q = Q()
        if self.is_valid():
            nome = self.cleaned_data['nome']
            if nome:
                q = q & Q(nome__icontains=nome)
            email = self.cleaned_data['email']
            if email:
                q = q & Q(email__icontains=email)

        return User.objects.filter(q)