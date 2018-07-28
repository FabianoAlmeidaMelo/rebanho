from django.test import TestCase
from django.shortcuts import resolve_url
from rebanho.core.models import User
from rebanho.propriedades.models import Propriedade, PropriedadeUser

class UserModelTest(TestCase):
    """
    python manage.py test

    Sem rodar as migrações:
    python manage.py test --nomigrations
    """
    def setUp(self):
        self.user = User.objects.create(email = 'falmeidamelo@uol.com.br',
                                        username = 'user1',
                                        nome = 'Fabiano Almeida')
        self.propriedade = Propriedade.objects.create(cnpj = '12345678912345',
                                                      nirf = '123456',
                                                      nome = 'Fazenda Vera Cruz',
                                                      incra='incr4')
        self.prop_user = PropriedadeUser.objects.create(propriedade=self.propriedade,
                                                        user=self.user,
                                                        owner=True)

    def test_create(self):
        "verifca se tem um ID"
        self.assertTrue(self.propriedade.id)

    def test_str(self):
        self.assertEqual('Fazenda Vera Cruz', str(self.propriedade))

    def test_cnpj_unique(self):
        field = self.propriedade._meta.get_field('cnpj')
        self.assertTrue(field.unique)

    def test_nirf(self):
        # field = self.propriedade._meta.get_field('nirf')
        self.assertEqual('123456', str(self.propriedade.nirf))

    def test_incra(self):
        # field = self.propriedade._meta.get_field('incra')
        self.assertEqual('incr4', str(self.propriedade.incra))

    def test_can_edit(self):
        # True
        self.assertTrue(self.propriedade.can_edit(self.user))
