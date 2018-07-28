
from django.test import TestCase
from django.shortcuts import resolve_url
from django.urls import reverse
from rebanho.propriedades.models import Propriedade, PropriedadeUser
from rebanho.core.models import User

class PropriedadeFormTest(TestCase):
    """
    python manage.py test
    """
    def setUp(self):
        self.response = self.client.get(resolve_url('propriedades_list'))
        self.user1 = User.objects.create(id = 1,
                                         email = 'falmeidamelo@uol.com.br',
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
        response = self.client.get(reverse('propriedade_form'))
        return self.assertEqual(200, response.status_code)

    def test_template(self):
        """verifica se está usando o propriedade_form.html"""
        login = self.client.login(username='user1', password='12345')
        response = self.client.get(reverse('propriedade_form'))
        self.assertTemplateUsed(response, 'propriedades/propriedade_form.html')

    def test_propriedades_list_link(self):
        """verifica se tem o link para voltar para a listagem de propriedades"""
        login = self.client.login(username='user1', password='12345')
        response = self.client.get(reverse('propriedade_form'))
        expected = 'href="{}"'.format(resolve_url('propriedades_list'))
        self.assertContains(response, expected)

    def test_textos_no_html(self):
        """verifica os textos no html"""
        login = self.client.login(username='user1', password='12345')
        response = self.client.get(reverse('propriedade_form'))
        contents = [
            'Propriedades',
            'Nome da Propriedade',
            'Nirf',
            'Cnpj',
            'Telefone',
            'Incra',
            'Nome contato',
        ]
        for expected in contents:
            with self.subTest():
                self.assertContains(response, expected)

    def test_propriedade_form_user_loged_in(self):
        """ 200 - propriedade.can_edit return True"""
        propriedade1 = Propriedade.objects.create(id=1,
                                                  cnpj="61.675.372/0001-02",
                                                  nome="Fazenda Vera Cruz",
                                                  nirf="123",
                                                  incra="345",
                                                  telefone="12982239764",
                                                  nome_contato="Fabiano Almeida")

        # ESSA o user não pode acessar, propriedade.can_edit return False
        propriedade2 = Propriedade.objects.create(cnpj="22.994.777/0001-51",
                                                  nome="Fazenda Pingo D`água",
                                                  nirf="12123",
                                                  incra="32345",
                                                  telefone="12999888321",
                                                  nome_contato="Luciano de Melo")
        prop_user = PropriedadeUser.objects.create(propriedade=propriedade1,
                                                   user=self.user1,
                                                   owner=True)
        login = self.client.login(username='user1', password='12345')

        response = self.client.get(reverse('propriedade_form', kwargs={'pk':propriedade2.pk,}) )
        return self.assertEqual(200, response.status_code)
 
    def test_propriedade_form_user_loged_in(self):
        """ 404 - user tenta acessar uma propriedade que não tem permissão"""
        propriedade1 = Propriedade.objects.create(id=1,
                                                  cnpj="61.675.372/0001-02",
                                                  nome="Fazenda Vera Cruz",
                                                  nirf="123",
                                                  incra="345",
                                                  telefone="12982239764",
                                                  nome_contato="Fabiano Almeida")

        # ESSA o user não pode acessar, propriedade.can_edit = False
        propriedade2 = Propriedade.objects.create(cnpj="22.994.777/0001-51",
                                                  nome="Fazenda Pingo D`água",
                                                  nirf="12123",
                                                  incra="32345",
                                                  telefone="12999888321",
                                                  nome_contato="Luciano de Melo")
        prop_user = PropriedadeUser.objects.create(propriedade=propriedade1,
                                                   user=self.user1,
                                                   owner=True)
        login = self.client.login(username='user1', password='12345')

        response = self.client.get(reverse('propriedade_form', kwargs={'pk':propriedade2.pk,}) )
        return self.assertEqual(404, response.status_code)
