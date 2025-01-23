from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    cpf = models.CharField(max_length=14, unique=True)
    endereco = models.TextField()
    nome = models.CharField(max_length=150)
    sobrenome = models.CharField(max_length=150, blank=True, null=True)
    telefone = models.CharField(max_length=15)
