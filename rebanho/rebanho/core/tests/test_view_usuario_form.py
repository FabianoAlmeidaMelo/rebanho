
from django.test import TestCase
from django.shortcuts import resolve_url

class UsuariosFormTest(TestCase):
    """
    python manage.py test
    """

    def setUp(self):
        self.response = self.client.get(resolve_url('usuario_form'))

    def test_get(self):
        """GET / retorna status code 200"""
        return self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """verifica se está usando o index.html"""
        self.assertTemplateUsed(self.response, 'core/usuario_form.html')

    def test_usuarios_list_link(self):
        """verifica se tem o link para voltar para a listagem de usuários"""
        expected = 'href="{}"'.format(resolve_url('usuarios_list'))
        self.assertContains(self.response, expected)

    def test_textos_no_html(self):
        """verifica os textos no html"""
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
                self.assertContains(self.response, expected)
 