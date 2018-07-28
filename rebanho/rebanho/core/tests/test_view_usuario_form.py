
from django.test import TestCase
from django.shortcuts import resolve_url
from django.urls import reverse
from rebanho.core.models import User

class UsuariosFormTest(TestCase):
    """
    python manage.py test
    """

    def setUp(self):
        self.response = self.client.get(resolve_url('usuario_form'))
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
        response = self.client.get(reverse('usuario_form'))
        return self.assertEqual(200, response.status_code)

    def test_template(self):
        """verifica se está usando o usuario_form.html"""
        login = self.client.login(username='user1', password='12345')
        response = self.client.get(reverse('usuario_form'))
        self.assertTemplateUsed(response, 'core/usuario_form.html')

    def test_usuarios_list_link(self):
        """verifica se tem o link para voltar para a listagem de usuários"""
        login = self.client.login(username='user1', password='12345')
        response = self.client.get(reverse('usuario_form'))
        expected = 'href="{}"'.format(resolve_url('usuarios_list'))
        self.assertContains(response, expected)

    def test_textos_no_html(self):
        """verifica os textos no html"""
        login = self.client.login(username='user1', password='12345')
        response = self.client.get(reverse('usuario_form'))
        contents = [
            'Rebanho',
            'Usuários',
            'nome',
            'email',
            'Senha',
            'Confirmação da Senha',
            'Salvar',
            'Cancelar'
        ]
        for expected in contents:
            with self.subTest():
                self.assertContains(response, expected)
 # 