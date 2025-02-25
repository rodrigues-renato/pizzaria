from django.urls import path
from . import views
app_name = 'clientes'

urlpatterns = [
    path('registrar/', views.registrar_cliente, name='registrar_cliente'),
    path('login/', views.logar_cliente, name='login_cliente'),
    path('logout/', views.deslogar_cliente, name='logout_cliente'),
    path('salvar_endereco/', views.salvar_endereco, name='salvar_endereco')
]
