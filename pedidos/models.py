from django.db import models
from clientes.models import CustomUser
from menu.models import Produto


class Carrinho(models.Model):
    cliente = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"Carrinho de {self.cliente.username}"


class ItemCarrinho(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome}"


class Pedido(models.Model):
    cliente = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    carrinho = models.OneToOneField(
        Carrinho, on_delete=models.SET_NULL, null=True, blank=True
    )
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pendente', 'Pendente'),
            ('em preparo', 'Em Preparo'),
            ('entregue', 'Entregue'),
        ],
        default='pendente',
    )
    endereco_envio = models.TextField()
    metodo_pagamento = models.CharField(
        max_length=20,
        choices=[('cartao', 'Cartão'), ('dinheiro', 'Dinheiro'), ('pix', 'Pix')],
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    def salvar_total(self):
        if self.carrinho:
            self.total = self.carrinho.calcular_total()

    def save(self, *args, **kwargs):
        self.salvar_total()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.username}"
