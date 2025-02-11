from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm  
from pedidos.models import Carrinho
from clientes.models import CustomUser
from django.shortcuts import get_object_or_404


def registrar_cliente(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário criado com sucesso')

            # Quando uma conta é registrada, um carrinho é vinculado a ela
            custom_user = get_object_or_404(CustomUser, email=form.cleaned_data['email'])
            criar_carrinho = Carrinho.objects.create(cliente=custom_user)
            criar_carrinho.save()

            return redirect('clientes:registrar_cliente')

    return render(request, 'clientes/registrar.html', {'form':form})


def logar_cliente(request):
    form = AuthenticationForm(request)

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Logado com sucesso')
            return redirect('menu:index')
        
    return render(request, 'clientes/logar.html', {'form':form})


@login_required(login_url='clientes:login_cliente')
def deslogar_cliente(request):
    logout(request)
    messages.success(request, 'Deslogado com sucesso')
    return redirect('clientes:login_cliente')