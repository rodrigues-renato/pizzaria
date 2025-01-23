from django.contrib import admin
from menu.models import Produto

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = 'id', 'preco'
    ordering = '-id',