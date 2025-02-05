from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
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
    form = AuthenticationForm(request)

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Logado com sucesso')
            return redirect('menu:index')
        
    return render(request, 'clientes/logar.html', {'form':form})


@login_required(login_url='contact:login')
def deslogar_cliente(request):
    logout(request)
    messages.success(request, 'Deslogado com sucesso')
    return redirect('clientes:logar_cliente')