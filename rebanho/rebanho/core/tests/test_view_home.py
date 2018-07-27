from django.test import TestCase
from django.shortcuts import resolve_url
from django.urls import reverse
from rebanho.core.models import User

class HomeTest(TestCase):
    """
    python manage.py test
    """

    def setUp(self):
        #Create user
        self.user1 = User.objects.create(email = 'falmeidamelo@uol.com.br',
                                              username = 'user1',
                                              nome = 'Fabiano Almeida')
        self.user1.set_password('12345')
        self.user1.save()
        self.response = self.client.get(resolve_url('home'))

    ### SEM AUTENTICAR ini  #########
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
            'Gestão de rebanhos de Corte',
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

    def test_nav_bar_login_link(self):
        """verifica se tem o link para voltar ao topo da página"""
        expected = 'href="{}"'.format(resolve_url('login'))
        self.assertContains(self.response, expected)

    ### SEM AUTENTICAR fim  #########

    ### AUTENTICADO   #########
    def test_get(self):
        """GET / retorna status code 200"""
        login = self.client.login(username='user1', password='12345')
        response = self.client.get(reverse('home'))
        return self.assertEqual(200, response.status_code)

    def test_template(self):
        """verifica se está usando o index.html"""
        login = self.client.login(username='user1', password='12345')
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'index.html')

    def test_nav_bar_topo_link(self):
        """verifica se tem o link para voltar ao topo da página"""
        login = self.client.login(username='user1', password='12345')
        response = self.client.get(reverse('home'))
        expected = 'href="{}"'.format(resolve_url('home'))
        self.assertContains(response, expected)

    def test_titulos_no_html(self):
        """verifica os títulos"""

        login = self.client.login(username='user1', password='12345') # usuário nome: Fabiano Almeida
        response = self.client.get(reverse('home'))
        contents = [
            'Bem vindo ao sistema Gestão de Pecuária 4.0',
            'Trabalhamos para otmizar seu tempo e os lucros da sua propriedade',
            'Fabiano Almeida, mantenha seus dados atualizados e lhe ajudaremos a tomar as melhores decisões',
        ]
        for expected in contents:
            with self.subTest():
                self.assertContains(response, expected)

    def test_nav_bar_login_link(self):
        """verifica se tem o link para voltar ao topo da página"""
        login = self.client.login(username='user1', password='12345')
        response = self.client.get(reverse('home'))
        expected = 'href="{}"'.format(resolve_url('logout'))
        self.assertContains(response, expected)
 