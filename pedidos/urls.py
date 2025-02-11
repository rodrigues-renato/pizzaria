from django.urls import path
from . import views
app_name = 'pedidos'

urlpatterns = [
    path('finalizar_pedido/<str:id>/', views.finalizar_pedido, name='finalizar_pedido'),
]