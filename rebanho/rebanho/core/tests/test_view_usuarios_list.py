from django.test import TestCase
from django.shortcuts import resolve_url

class UsuariosListTest(TestCase):
    """
    python manage.py test
    """

    def setUp(self):
        self.response = self.client.get(resolve_url('usuarios_list'))

    def test_get(self):
        """GET / retorna status code 200"""
        return self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """verifica se está usando o index.html"""
        self.assertTemplateUsed(self.response, 'core/usuarios_list.html')

    def test_pagination(self):
        """verifica se está usando o pagination.html"""
        self.assertTemplateUsed(self.response, 'pagination.html')

    def test_usuario_form_link(self):
        """verifica se tem o link para o formulário de usuário"""
        expected = 'href="{}"'.format(resolve_url('usuario_form'))
        self.assertContains(self.response, expected)

    def test_textos_no_html(self):
        """verifica os textos no html"""
        contents = [
            'Usuários',
            'Novo Usuário',
            'Nome',
            'Email',
            'Nenhum usuário encontrado'
        ]
        for expected in contents:
            with self.subTest():
                self.assertContains(self.response, expected)
 