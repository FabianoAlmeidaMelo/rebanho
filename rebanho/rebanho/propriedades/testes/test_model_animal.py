from django.test import TestCase
from django.shortcuts import resolve_url
from django.utils import timezone
import pytz
from rebanho.core.models import User
from rebanho.propriedades.models import (
    Animal,
    AnimalPesagem,
    Propriedade,
    PropriedadeUser,
)

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

        self.animal = Animal.objects.create(propriedade=self.propriedade,
                                            sexo=1,
                                            brinco = 'A123456',
                                            motivo_saida=2)

    def test_create(self):
        "verifca se tem um ID"
        self.assertTrue(self.animal.id)

    def test_str(self):
        self.assertEqual('Fazenda Vera Cruz - A123456', str(self.animal))

    def test_propriedade_required(self):
        field = self.animal._meta.get_field('propriedade')
        self.assertEqual(False, field.null)

    def test_sexo_required(self):
        field = self.animal._meta.get_field('sexo')
        self.assertEqual(False, field.null)

    def test_brinco_required(self):
        field = self.animal._meta.get_field('brinco')
        self.assertEqual(False, field.null)

    def test_entrada_null_true(self):
        field = self.animal._meta.get_field('entrada')
        self.assertEqual(True, field.null)

    def test_motivo_saida_null_true(self):
        field = self.animal._meta.get_field('motivo_saida')
        self.assertEqual(True, field.null)

    def test_can_edit(self):
        # True
        self.assertTrue(self.animal.can_edit(self.user))

    def test_can_edit_false(self):
        user = User.objects.create(email = 'joaquim@uol.com.br',
                                   username = 'outro_user',
                                   nome = 'Joaquim da Silva') 
        self.assertFalse(self.animal.can_edit(user))

    def test_get_ultima_pesagem(self):
        """
        retorna None
        ainda não tem pesagem
        """
        self.assertEqual(None, self.animal.get_ultima_pesagem())

    def test_get_ultima_pesagem_1(self):
        """
        retorna a pesagem mais recente
        """
        data_1 = timezone.datetime(2018, 3, 28, 0, 30, 20, 104074)
        data_2 = timezone.datetime(2018, 7, 28, 0, 30, 20, 104074)
        pesagem_primeira = AnimalPesagem.objects.create(animal=self.animal,
                                                        data=data_1,
                                                        peso="430.348")
        pesagem_segunda = AnimalPesagem.objects.create(animal=self.animal,
                                                       data=data_2,
                                                       peso="470.348")

        self.assertEqual("2018-07-28 03:30:20.104074+00:00", str(self.animal.get_ultima_pesagem().data))

    def test_get_data_status(self):
        """
        TODO: teste
        test_get_ultima_pesagem
        retorna a Data da pesagem mais recente
        ou None
        """
        get_data_status = self.animal.get_data_status()
        data = str(get_data_status[0])
        status = get_data_status[1]
        self.assertEqual("None", data)
        self.assertEqual("", status)
