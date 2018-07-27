
from django.test import TestCase
from django.shortcuts import resolve_url
from dete import datetime
from rebanho.propriedades.models import Propriedade, PropriedadeUser
from rebanho.core.models import User

class PropriedadeUserModelTest(TestCase):
    """
    python manage.py test

    Sem rodar as migrações:
    python manage.py test --nomigrations
    """
    def setUp(self):
        self.propriedade = Propriedade.objects.create(cnpj = '12345678912345',
                                                      nirf = '123456',
                                                      nome = 'Fazenda Vera Cruz',
                                                      incra='incr4')
        self.user = User.objects.create(email = 'falmeidamelo@uol.com.br',
                                        username = 'falmeidamelo@uol.com.br',
                                        nome = 'Fabiano Almeida',
                                        password='12345')
        self.propriedade_user = PropriedadeUser.objects.create(propriedade=self.propriedade,
                                                               user=self.user)


    def test_create(self):
        "verifca se tem um ID"
        self.assertTrue(self.propriedade_user.id)

    def test_str(self):
        self.assertEqual('Fabiano Almeida - Fazenda Vera Cruz', str(self.propriedade_user))

    def test_owner_false(self):
        self.assertFalse(self.propriedade_user.owner)

    def test_date_joined(self):
        field = self.propriedade_user._meta.get_field('date_joined')
        self.assertEqual(type(self.propriedade_user.date_joined), datetime)

    def test_ativo_true(self):
        field = self.propriedade_user._meta.get_field('ativo')
        self.assertTrue(field)

