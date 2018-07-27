from django.db import models
from django.utils import timezone

class Propriedade(models.Model):
     
    cnpj = models.CharField(max_length=14, unique=True)  # *****
    nome = models.CharField(max_length=150)
    nirf = models.CharField(max_length=12,null=True,blank=True)
    incra= models.CharField(max_length=12, null=True,blank=True)
    
    endereco = models.CharField(max_length=150,null=True, blank=True)
    bairro = models.CharField(max_length=50,null=True, blank=True)
    municipio = models.CharField(max_length=60,null=True, blank=True)
    referencia = models.CharField(max_length=200,null=True, blank=True)
    area_total = models.FloatField(max_length=5,null=True, blank=True)
    telefone = models.CharField(max_length=12,null=True, blank=True)
    nome_contato = models.CharField(max_length= 30,null=True, blank=True)

    class Meta:
        verbose_name = 'propriedade'
        verbose_name_plural = 'propriedades'
        ordering = ('nome',)

    def __str__(self):
        return self.nome

class PropriedadeUser(models.Model):
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
