from django.urls import path
from . import views
app_name = 'presenca'

urlpatterns = [
    path('', views.index, name='index'),
]