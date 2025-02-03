from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import RegisterForm  


def registrar_cliente(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():          
            form.save()
            messages.success(request, 'Usuário criado com sucesso')
            return redirect('clientes:registrar_cliente')
    
    return render(request, 'clientes/registrar.html', {'form':form})


def logar_cliente(request):
    ...