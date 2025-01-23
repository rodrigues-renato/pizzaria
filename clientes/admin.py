from django.contrib import admin
from clientes.models import CustomUser
# Register your models here.


@admin.register(CustomUser)
class ClienteAdmin(admin.ModelAdmin):
    list_display = 'cpf', 'first_name'
    ordering = '-id',