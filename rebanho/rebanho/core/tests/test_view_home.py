from django.test import TestCase
from django.shortcuts import resolve_url

class HomeTest(TestCase):
    """
    python manage.py test
    """

    def setUp(self):
        self.response = self.client.get(resolve_url('home'))

    def test_get(self):
        """GET / retorna status code 200"""
        return self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """verifica se está usando o index.html"""
        self.assertTemplateUsed(self.response, 'index.html')

    def test_nav_bar_topo_link(self):
        """verifica se tem o link para voltar ao topo da página"""
        expected = 'href="{}"'.format(resolve_url('home'))
        self.assertContains(self.response, expected)

    def test_titulos_no_html(self):
        """verifica os títulos"""
        contents = [
            'Agilidade no Manejo',
            'Velocidade na pesagem',
            'Fluxo de Caixa da Fazenda',
            'Controle das Vacinas',
            'Aplicativo para Controles no Campo',
            'Atende a Rastreabilidade',
            'Integra com várias balanças e leitores RFID'
        ]
        for expected in contents:
            with self.subTest():
                self.assertContains(self.response, expected)

    # def test_nav_bar_login_link(self):
    #     """verifica se tem o link para voltar ao topo da página"""
    #     expected = 'href="{}"'.format(resolve_url('login'))
    #     self.assertContains(self.response, expected)
 