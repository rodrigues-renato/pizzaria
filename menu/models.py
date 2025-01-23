from django.db import models

# Create your models here.

class Produto(models.Model):
    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
    
    nome = models.CharField(max_length=30)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    descricao = models.TextField()
    categoria = models.CharField(max_length=50, choices=[("Pizza", "Pizza"), ("Bebida", "Bebida")])
