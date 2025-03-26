from django.contrib import admin
from .models import *


@admin.register(ItemCarrinho)
class ItemCarrinhoAdmin(admin.ModelAdmin):
    list_display = 'produto', 'quantidade', 'carrinho'


@admin.register(Carrinho)
class CarrinhoAdmin(admin.ModelAdmin):
    list_display = ('cliente',)


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = 'cliente', 'total', 'metodo_pagamento', 'criado_em'


@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = 'cliente', 'pedido', 'produto', 'quantidade'
