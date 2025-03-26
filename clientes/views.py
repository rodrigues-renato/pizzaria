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
from .forms import UserUpdateForm, EnderecoUpdateForm, CustomPasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .models import EnderecoUser

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

def atualizar_dados(request):
    user = request.user
    enderecos = EnderecoUser.objects.filter(user=user)  # Obtém os endereços do usuário

    endereco_selecionado = request.GET.get('endereco_id')
    endereco = enderecos.filter(id=endereco_selecionado).first() if endereco_selecionado else None

    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=user)
        endereco_form = EnderecoUpdateForm(request.POST, instance=endereco) if endereco else None
        password_form = CustomPasswordChangeForm(user, request.POST) if 'update_password' in request.POST else CustomPasswordChangeForm(user)

        if 'update_user' in request.POST:
            if user_form.is_valid():
                user_form.save()
                messages.success(request, "Telefone atualizado com sucesso!")
                return redirect('clientes:atualizar_dados')

        elif 'update_endereco' in request.POST and endereco:
            if endereco_form and endereco_form.is_valid():
                endereco_form.save()
                messages.success(request, "Endereço atualizado com sucesso!")
                return redirect('clientes:atualizar_dados')

        elif 'update_password' in request.POST:
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Senha alterada com sucesso!")
                return redirect('clientes:atualizar_dados')

    else:
        user_form = UserUpdateForm(instance=user)
        endereco_form = EnderecoUpdateForm(instance=endereco) if endereco else None
        password_form = CustomPasswordChangeForm(user)

    return render(request, 'clientes/atualizar_dados.html', {
        'user_form': user_form,
        'endereco_form': endereco_form,
        'password_form': password_form,
        'enderecos': enderecos,
        'endereco_selecionado': endereco_selecionado
    })

