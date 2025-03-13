from django.contrib import admin
from .models import Vendas


@admin.register(Vendas)
class VendasAdmin(admin.ModelAdmin):
    list_display = []