
from django.test import TestCase
from django.shortcuts import resolve_url
from django.urls import reverse
from rebanho.core.models import User

class UserViewTest(TestCase):
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


    def test_login_template(self):
        # GET /  sem autenticacao
        response = self.client.get(reverse('login'))

        #Check that we got a response "success"
        self.assertEqual(response.status_code, 200)
        #Check we used correct template
        self.assertTemplateUsed(response, 'login.html')
        #Check our user is logged in
        self.assertEqual(str(response.context['user']), 'AnonymousUser')

    def test_redirects_home_on_success_login(self):
        login = self.client.login(username='user1', password='12345')

        response = self.client.post(reverse('home', kwargs={}), {})
        self.assertEqual(response.request['PATH_INFO'], '/')
        self.assertEqual(response.status_code, 200)

    def test_redirects_home_on_success_logout(self):
        # Log in
        login = self.client.login(username='user1', password='12345')
        self.assertEqual(login, True)
        
        # Check response code
        response = self.client.get('/')   # Home
        self.assertEquals(response.status_code, 200)

        # Check 'Log out' in response
        expected = 'href="{}"'.format(resolve_url('logout'))
        self.assertContains(response, expected)

        # # Log out
        self.client.post(reverse('logout', kwargs={}), {})

        # # # Check response code
        response = self.client.get('/')  # Home
        self.assertEquals(response.status_code, 200)

        # # Check 'Log in' in response
        expected = 'href="{}"'.format(resolve_url('login'))
        self.assertContains(response, expected)

    def test_usuarios_list_not_logged_in(self):
        # testa o acesso sem autenticacao, deve redirecionar para o login
        response = self.client.get(reverse('usuarios_list'))
        self.assertRedirects(response, '/login/?next=/jetbov/usuarios_list/')

    def test_usuario_form_not_logged_in(self):
        # testa o acesso sem autenticacao, deve redirecionar para o login
        response = self.client.get(reverse('usuario_form'))
        self.assertRedirects(response, '/login/?next=/jetbov/usuario_form/')

    def test_usuarios_list_logged_in(self):
        # testa o acesso com autenticacao: retorna status code 200
        login = self.client.login(username='user1', password='12345')
        response = self.client.get(reverse('usuarios_list'))

        self.assertEqual(200, response.status_code)
        #response.request['PATH_INFO']

    def test_url_usuarios_list_logged_in(self):
        # testa o acesso com autenticacao: verifica se a url esperada está correta
        login = self.client.login(username='user1', password='12345')
        response = self.client.get(reverse('usuarios_list'))

        self.assertEqual(response.request['PATH_INFO'], '/jetbov/usuarios_list/')

    def test_usuario_form_logged_in(self):
        # testa o acesso com autenticacao
        login = self.client.login(username='user1', password='12345')
        response = self.client.get(reverse('usuario_form'))
        self.assertEqual(200, response.status_code)

    def test_url_usuario_form_logged_in(self):
        # testa o acesso com autenticacao: verifica se a url esperada está correta
        login = self.client.login(username='user1', password='12345')
        response = self.client.get(reverse('usuario_form'))
        self.assertEqual(response.request['PATH_INFO'], '/jetbov/usuario_form/')

    def test_logged_in_usuario_list_template(self):
        login = self.client.login(username='user1', password='12345')
        response = self.client.get(reverse('usuarios_list'))
        
        #Check our user is logged in
        self.assertEqual(str(response.context['user']), 'Fabiano Almeida')
        #Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        #Check we used correct template
        self.assertTemplateUsed(response, 'core/usuarios_list.html')

    def test_logged_in_usuario_form_template(self):
        login = self.client.login(username='user1', password='12345')
        response = self.client.get(reverse('usuario_form'))
        
        #Check our user is logged in
        self.assertEqual(str(response.context['user']), 'Fabiano Almeida')
        #Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        #Check we used correct template
        self.assertTemplateUsed(response, 'core/usuario_form.html')
