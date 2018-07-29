from django.db import models
from django.utils import timezone


CHOICE_MOTIVO_SAIDA = (
        (None, '---'),
        (1, 'venda'),
        (2, 'troca'),
        (3, 'abate'),
        (4, 'morte'),
        (5, 'outros'),
)

CHOICE_SEXO =(
    (None, '---'),
    (1, 'macho'),
    (2, 'fêmea'),
)

class Propriedade(models.Model):
    """
    ref #7
    """
    cnpj = models.CharField(max_length=18, unique=True)
    nome = models.CharField(max_length=150)
    nirf = models.CharField(max_length=12,null=True,blank=True)
    incra= models.CharField(max_length=12, null=True,blank=True)
    
    # endereco = tabela do core, usando o django municipios, #TODO

    telefone = models.CharField(max_length=12,null=True, blank=True)
    nome_contato = models.CharField(max_length= 30,null=True, blank=True)

    class Meta:
        verbose_name = 'propriedade'
        verbose_name_plural = 'propriedades'
        ordering = ('nome',)

    def __str__(self):
        return self.nome

    def can_edit(self, user):
        """
        TODO: teste
        test_can_edit
        """
        return self.id in user.propriedadeuser_set.all().values_list('propriedade__id', flat=True)


class PropriedadeUser(models.Model):
    """
    ref #7
    """
    propriedade = models.ForeignKey(Propriedade)
    user = models.ForeignKey('core.User')
    owner = models.BooleanField(default=False)
    date_joined = models.DateTimeField(
        'data de cadastro', default=timezone.now
        )
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'propriedade_user'
        verbose_name_plural = 'propriedades_users'

    def __str__(self):
        return '%s - %s' % (self.user, self.propriedade.nome)


class Animal(models.Model):
    """
    ref #8
    """
    propriedade = models.ForeignKey(Propriedade)
    sexo = models.SmallIntegerField("Sexo", choices=CHOICE_SEXO)
    brinco = models.CharField("Brinco", max_length=25)
    nascimento = models.DateTimeField('Data de Nascimento', null=True, blank=True)
    entrada = models.DateTimeField('Data de Entrada no Estoque', null=True, blank=True)
    # ## Raça: Nelore, Guzerá, Gir, Brahman, Tabapuã, Cangaian, Angus, ...
    # raca = models.ForeignKey(Raca, null=True, blank=True)
    saida = models.DateTimeField('Data de Saída do Estoque', null=True, blank=True)
    # ## Sai por venda, troca, abate p comsumo, morte
    motivo_saida = models.SmallIntegerField("Motivo da saída", choices=CHOICE_MOTIVO_SAIDA, null=True, blank=True)

    date_joined = models.DateTimeField(
        'data de cadastro', default=timezone.now
        )

    class Meta:
        verbose_name = 'animal'
        verbose_name_plural = 'animais'
        unique_together = ('propriedade', 'brinco')

    def __str__(self):
        return '%s - %s' % (self.propriedade, self.brinco)

    def can_edit(self, user):
        """
        retorna True or False
        """
        return self.propriedade_id in user.propriedadeuser_set.all().values_list('propriedade__id', flat=True)


    def get_ultima_pesagem(self):
        """
        retorna a pesagem mais recente
        ou None
        """
        return self.animalpesagem_set.all().order_by('data').last()


    def get_data_status(self):
        """
        TODO: teste
        test_get_data_status
        retorna uma das Datas, seguindo a prioridade:
        Saída, entrada, nascimento, None 
        """
        data = (self.nascimento, "nascimento" if self.nascimento else '')
        if self.entrada:
            data = (self.entrada, "entr. estoque" if self.entrada else '')
        if self.saida:
            data = (self.saida, "%s" % self.get_motivo_saida_display())
        return data


class AnimalPesagem(models.Model):
    """
    ref #8
    """
    animal = models.ForeignKey(Animal)
    data = models.DateTimeField('Data')
    peso = models.DecimalField('Peso',
                               max_digits=7,
                               decimal_places=3)
    class Meta:
        verbose_name = 'pesagem'
        verbose_name_plural = 'pesagens'
        ordering = ('-data',)

    def __str__(self):
        return '%s - %s - %s' % (self.animal.brinco, self.data.date(), self.peso)