from django.urls import path
from . import views
app_name = 'pedidos'

urlpatterns = [
    path('finalizar_pedido/', views.finalizar_pedido, name='finalizar_pedido'),
]