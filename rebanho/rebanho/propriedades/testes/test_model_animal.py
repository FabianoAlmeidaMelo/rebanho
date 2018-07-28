from django.test import TestCase
from django.shortcuts import resolve_url

from rebanho.propriedades.models import Animal, Propriedade

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

