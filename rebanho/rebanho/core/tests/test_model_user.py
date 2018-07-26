from django.test import TestCase
from django.shortcuts import resolve_url
from django.core.exceptions import ValidationError
from rebanho.core.models import User

class UserModelTest(TestCase):
    """
    python manage.py test
    
    Sem rodar as migrações:
    python manage.py test --nomigrations
    """
    def setUp(self):
        self.user = User.objects.create(
                                        email = 'falmeidamelo@uol.com.br',
                                        username = 'falmeidamelo@uol.com.br',
                                        nome = 'Fabiano Almeida',
                                    )

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
