from django.db import models

from typing import ClassVar
from django.db import models
import datetime
from menu.models import Produto



class Vendas(models.Model):
    nome_produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    total = models.FloatField()
    data = models.DateTimeField(default=datetime.datetime.now())


    class Meta:
        verbose_name_plural= 'Vendas'
    def __str__(self):
        return self.nome_produto.nome
    
    