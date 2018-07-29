from django.test import TestCase
from django.shortcuts import resolve_url
from django.urls import reverse
from rebanho.propriedades.models import Animal, AnimalPesagem, Propriedade, PropriedadeUser
from rebanho.core.models import User

class AnimalPesagemFormTest(TestCase):
    """
    python manage.py test
    """
    def setUp(self):
        self.user1 = User.objects.create(id = 1,
                                         email = 'falmeidamelo@uol.com.br',
                                         username = 'user1',
                                         nome = 'Fabiano Almeida')
        self.user1.set_password('12345')
        self.user1.save()
        self.propriedade1 = Propriedade.objects.create(id=1,
                                                       cnpj="61.675.372/0001-02",
                                                       nome="Fazenda Vera Cruz",
                                                       nirf="123",
                                                       incra="345",
                                                       telefone="12982239764",
                                                       nome_contato="Fabiano Almeida")
        self.animal = Animal.objects.create(propriedade=self.propriedade1,
                                            sexo=1,
                                            brinco = 'A123456',
                                            motivo_saida=2)



    def test_get(self):
        """GET / retorna status code 302"""
        animal = Animal.objects.create(propriedade=self.propriedade1,
                                                    sexo=1,
                                                    brinco = 'A123452',
                                                    )
        response = self.client.get(reverse('animal_pesagem_form', kwargs={'animal_pk': animal.pk}))
        return self.assertEqual(302, response.status_code)

    def test_get_autenticado(self):
        """GET / retorna status code 404"""
        login = self.client.login(username='user1', password='12345')
        animal = Animal.objects.create(propriedade=self.propriedade1,
                                                    sexo=1,
                                                    brinco = 'A113456',
                                                    )
        response = self.client.get(reverse('animal_pesagem_form', kwargs={'animal_pk': animal.pk}))
        return self.assertEqual(404, response.status_code)

    def test_template(self):
        """verifica se está usando o animal_pesagem_form.html"""
        PropriedadeUser.objects.create(propriedade=self.propriedade1,
                                       user=self.user1,
                                       owner=True)
        login = self.client.login(username='user1', password='12345')
        response = self.client.get(reverse('animal_pesagem_form', kwargs={'animal_pk': self.animal.pk,}))
        self.assertTemplateUsed(response, 'propriedades/animal_pesagem_form.html')

    def test_animais_list_link(self):
        """verifica se tem o link para voltar para a listagem de animais"""
        PropriedadeUser.objects.create(propriedade=self.propriedade1,
                                       user=self.user1,
                                       owner=True)
        login = self.client.login(username='user1', password='12345')
        response = self.client.get(reverse('animal_pesagem_form', kwargs={'animal_pk': self.animal.pk,}))
        expected = 'href="{}"'.format(reverse('animais_list', kwargs={'propriedade_pk': self.animal.propriedade.pk,}))
        self.assertContains(response, expected)

    def test_textos_no_html(self):
        """verifica os textos no html"""
        PropriedadeUser.objects.create(propriedade=self.propriedade1,
                                       user=self.user1,
                                       owner=True)
        login = self.client.login(username='user1', password='12345')
        response = self.client.get(reverse('animal_pesagem_form', kwargs={'animal_pk': self.animal.pk}))
        contents = [
            'Peso',
            'Data', # Pesagem animal brinco A123456, / Propriedade Fazenda Vera Cruz: 61.675.372/0001-02
            'Pesagens:',
            'Pesagem animal brinco', # / Propriedade Fazenda Vera Cruz: 61.675.372/0001-02',
            'A123456',
            'Propriedade Fazenda Vera Cruz: 61.675.372/0001-02',
        ]
        for expected in contents:
            with self.subTest():
                self.assertContains(response, expected)
