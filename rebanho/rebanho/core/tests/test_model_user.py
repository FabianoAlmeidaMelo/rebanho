from django.test import TestCase
from django.shortcuts import resolve_url

from rebanho.core.models import User
from rebanho.propriedades.models import Propriedade, PropriedadeUser

class PropriedadeModelTest(TestCase):
    """
    python manage.py test

    Sem rodar as migrações:
    python manage.py test --nomigrations
    """
    def setUp(self):
        self.user = User.objects.create(email = 'falmeidamelo@uol.com.br',
                                        username = 'falmeidamelo@uol.com.br',
                                        nome = 'Fabiano Almeida',
                                        password='12345')

    def test_create(self):
        self.assertTrue(User.objects.exists())

    def test_str(self):
        self.assertEqual('Fabiano Almeida', str(self.user))

    def test_email_unique(self):
        field = User._meta.get_field('email')
        self.assertTrue(field.unique)

    def test_username_unique(self):
        field = User._meta.get_field('username')
        self.assertTrue(field.unique)

    def test_is_active_true(self):
        self.assertTrue(self.user.is_active)

    def test_date_joined_not_none(self):
        self.assertTrue(self.user.date_joined is not None)

    def test_get_propriedades(self):
        '''
        self.user não tem propriedade
        []
        '''
        self.assertEqual([], self.user.get_propriedades())

    def test_get_propriedades_1(self):
        '''
        self.user não tem propriedade
        [tem uma]
        '''
        propriedade1 = Propriedade.objects.create(cnpj="61.675.372/0001-02",
                                                  nome="Fazenda Vera Cruz",
                                                  nirf="123",
                                                  incra="345",
                                                  telefone="12982239764",
                                                  nome_contato="Fabiano Almeida")
        # ESSA o user não pode acessar, propriedade.can_edit return False
        propriedade2 = Propriedade.objects.create(cnpj="22.994.777/0001-51",
                                                  nome="Fazenda Pingo D`água",
                                                  nirf="12123",
                                                  incra="32345",
                                                  telefone="12999888321",
                                                  nome_contato="Luciano de Melo")
        prop_user = PropriedadeUser.objects.create(propriedade=propriedade1,
                                                   user=self.user,
                                                   owner=True)

        self.assertEqual(1, len(self.user.get_propriedades()))