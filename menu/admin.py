from django.contrib import admin
from menu.models import Cardapio

# Register your models here.

@admin.register(Cardapio)
class CardapioAdmin(admin.ModelAdmin):
    list_display = 'id', 'preco'
    ordering = '-id',