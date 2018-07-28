# coding: utf-8
from django.db import models
from django.utils import timezone
from datetime import date
from django.contrib.auth.models import(
    AbstractBaseUser,
    BaseUserManager,
)

from django.contrib.auth.models import User, Group
from django.conf import settings
from municipios.models import Municipio


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError(u'Email é obrigatório')
        email = UserManager.normalize_email(email)
        user = self.model(email=email, is_active=True, is_superuser=False,
                          last_login=now, date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField('e-mail', unique=True)
    username = models.CharField('username', max_length=100, unique=True)
    nome = models.CharField(verbose_name=u'Nome', max_length=100)
    is_active = models.BooleanField('ativo', default=True,)
    date_joined = models.DateTimeField(
        'data de cadastro', default=timezone.now
        )

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('nome', 'email', )

    class Meta:
        verbose_name = u'Usuário'
        verbose_name_plural = u'Usuários'

    def __str__(self):
        return self.nome

    def get_propriedades(self):
        """
        retorna uma lista de Propriedades
        que tem vínculo com o user
        """
        return [p.propriedade for p in self.propriedadeuser_set.all()]
