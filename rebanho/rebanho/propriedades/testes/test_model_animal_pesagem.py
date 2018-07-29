from decimal import Decimal
from django.test import TestCase
from django.shortcuts import resolve_url
from django.utils import timezone

from rebanho.propriedades.models import Animal, AnimalPesagem, Propriedade

class UserModelTest(TestCase):
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

        self.animal = Animal.objects.create(propriedade=self.propriedade,
                                            sexo=1,
                                            brinco = 'A123456')
        self.data = timezone.datetime(2018, 7, 28, 11, 24, 20, 104074)
        self.pesagem = AnimalPesagem.objects.create(animal=self.animal,
                                                    data=self.data,
                                                    peso= Decimal('430.450'))

    def test_create(self):
        "verifca se tem um ID"
        self.assertTrue(self.pesagem.id)

    def test_str(self):
        self.assertEqual('A123456 - 2018-07-28 - 430.450', str(self.pesagem))

    def test_animal_required(self):
        # required
        field = self.pesagem._meta.get_field('animal')
        self.assertEqual(False, field.null)

    def test_data_required(self):
        # required
        field = self.pesagem._meta.get_field('data')
        self.assertEqual(False, field.null)

    def test_peso_required(self):
        # required
        field = self.pesagem._meta.get_field('peso')
        self.assertEqual(False, field.null)
