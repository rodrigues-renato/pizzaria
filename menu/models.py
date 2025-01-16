from django.db import models

# Create your models here.

class Cardapio(models.Model):
    class Meta:
        verbose_name = 'Cardápio'
        verbose_name_plural = 'Cardápios'
    
    nome = models.CharField(max_length=30)
    preco = models.FloatField()
    ingrediente = models.TextField()
    categoria = models.CharField(max_length=50, choices=[("Pizza", "Pizza"), ("Bebida", "Bebida")])
