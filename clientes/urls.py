from django.urls import path
from . import views
app_name = 'clientes'

urlpatterns = [
    path('registrar/', views.registrar_cliente, name='registrar_cliente'),
    path('login/', views.logar_cliente, name='logar_cliente'),
]
