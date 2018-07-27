from django.test import TestCase
from django.shortcuts import resolve_url
from django.urls import reverse
from rebanho.propriedades.models import Propriedade
from rebanho.core.models import User

class PropriedadeListTest(TestCase):
    """
    python manage.py test
    """

    def setUp(self):
        self.response = self.client.get(resolve_url('propriedades_list'))
        self.user1 = User.objects.create(email = 'falmeidamelo@uol.com.br',
                                         username = 'user1',
                                         nome = 'Fabiano Almeida')
        self.user1.set_password('12345')
        self.user1.save()

    def test_get(self):
        """GET / retorna status code 302"""
        return self.assertEqual(302, self.response.status_code)

    def test_get_autenticado(self):
        """GET / retorna status code 200"""
        login = self.client.login(username='user1', password='12345')
        response = self.client.get(reverse('propriedades_list'))
        return self.assertEqual(200, response.status_code)

    def test_template(self):
        """verifica se está usando o propriedades_list.html"""
        login = self.client.login(username='user1', password='12345')
        response = self.client.get(reverse('propriedades_list'))
        self.assertTemplateUsed(response, 'propriedades/propriedades_list.html')

    def test_pagination(self):
        """verifica se está usando o pagination.html"""
        login = self.client.login(username='user1', password='12345')
        response = self.client.get(reverse('propriedades_list'))
        self.assertTemplateUsed(response, 'pagination.html')

    def test_propriedade_form_link(self):
        """verifica se tem o link para o formulário de usuário"""
        login = self.client.login(username='user1', password='12345')
        response = self.client.get(reverse('propriedades_list'))
        expected = 'href="{}"'.format(resolve_url('propriedade_form'))
        self.assertContains(response, expected)

    def test_textos_no_html(self):
        """verifica os textos no html"""
        login = self.client.login(username='user1', password='12345')
        response = self.client.get(reverse('propriedades_list'))

        contents = [
            'Propriedades',
            'CNPJ',
            'Nome',
            'NIRF',
            'Incra',
            'Nenhuma propriedade encontrada'
        ]
        for expected in contents:
            with self.subTest():
                self.assertContains(response, expected)
