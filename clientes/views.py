from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, AddressForm
from pedidos.models import Carrinho
from clientes.models import CustomUser, EnderecoUser
from django.shortcuts import get_object_or_404
from django.http import HttpResponse


def registrar_cliente(request):
    if request.user.is_authenticated:
        return redirect('menu:index')
    
    user_form = RegisterForm()

    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            # messages.success(request, 'Usuário criado com sucesso')

            # Quando uma conta é registrada, um carrinho é vinculado a ela
            custom_user = get_object_or_404(
                CustomUser, email=user_form.cleaned_data['email']
            )
            criar_carrinho = Carrinho.objects.create(cliente=custom_user)
            criar_carrinho.save()

            return redirect('clientes:login_cliente')

    context = {'user_form': user_form}
    return render(request, 'clientes/registrar.html', context)


def logar_cliente(request):
    if request.user.is_authenticated:
        return redirect('menu:index')
    
    form = AuthenticationForm(request)

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # messages.success(request, 'Logado com sucesso')
            return redirect('menu:index')

    return render(request, 'clientes/logar.html', {'form': form})


@login_required(login_url='clientes:login_cliente')
def deslogar_cliente(request):
    logout(request)
    # messages.success(request, 'Deslogado com sucesso')
    return redirect('clientes:login_cliente')


def salvar_endereco(request):
    rua = request.POST.get('rua')
    bairro = request.POST.get('bairro')
    numero = request.POST.get('numero')
    count = EnderecoUser.objects.filter(user=request.user, rua=rua, bairro=bairro, numero=numero).count()
    if count > 0:
        messages.error(request, 'Este endereço já está cadastrado')
    else:
        form = AddressForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            return redirect(request.META.get('HTTP_REFERER', 'pedidos:finalizar_pedido'))
        return HttpResponse(form)
