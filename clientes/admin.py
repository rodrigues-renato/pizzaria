from django.contrib import admin
from clientes.models import CustomUser
from django.contrib.auth import admin as admin_auth
from .forms import UserChangeForm, UserCreationForm


@admin.register(CustomUser)
class ClienteAdmin(admin_auth.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = CustomUser 
    fieldsets = admin_auth.UserAdmin.fieldsets + (
        ('Aditional', {'fields': ('cpf', 'rua', 'bairro', 'numero', 'telefone',)}),
    )
    ordering = '-id',