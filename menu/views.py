from django.shortcuts import render, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from menu.models import Produto
from pedidos.models import ItemCarrinho, Carrinho, Pedido
from clientes.models import CustomUser
from utils.utils import calcula_valor_total_carrinho


def index(request):
    """
    Primeira tela do site.
    Exibe os itens do cardápio
    """

    usuario = get_object_or_404(CustomUser, username=request.user)
    carrinho_vinculado = get_object_or_404(Carrinho, cliente=usuario)
    itens_carrinho = ItemCarrinho.objects.filter(carrinho=carrinho_vinculado).count()
    
    context = {
        'produtos': Produto.objects.all(),
        'carrinho': carrinho_vinculado,
        'item_carrinho': itens_carrinho,
    }

    return render(request, 'menu/index.html', context)


def adicionar_ao_carrinho(request, id):
    usuario = get_object_or_404(CustomUser, username=request.user)

    produto = get_object_or_404(Produto, id=id)
    carrinho_vinculado = get_object_or_404(Carrinho, cliente=usuario)
    consulta = ItemCarrinho.objects.filter(produto=produto, carrinho=carrinho_vinculado)
    if consulta.first():
        item = consulta.first()
        item.quantidade += 1
        item.save()

    else:
        item_carrinho = ItemCarrinho.objects.create(
            produto=produto,
            carrinho=carrinho_vinculado,
            quantidade=1,
        )
        item_carrinho.save()

    messages.info(request, f'{produto.nome} adicionado ao carrinho')
    return redirect(request.META.get('HTTP_REFERER', 'menu:index'))


def remover_do_carrinho(request, id):
    usuario = get_object_or_404(CustomUser, username=request.user)

    produto = get_object_or_404(Produto, id=id)
    carrinho_vinculado = get_object_or_404(Carrinho, cliente=usuario)
    consulta = ItemCarrinho.objects.filter(produto=produto, carrinho=carrinho_vinculado).first()
    if consulta.quantidade > 1:
        consulta.quantidade -= 1
        consulta.save()
    elif consulta.quantidade == 1:
        consulta.delete()

    messages.warning(request, f'{produto.nome} removido do carrinho')
    return redirect(request.META.get('HTTP_REFERER', 'menu:index'))


def excluir_do_carrinho(request, id):
    usuario = get_object_or_404(CustomUser, username=request.user)

    produto = get_object_or_404(Produto, id=id)
    carrinho_vinculado = get_object_or_404(Carrinho, cliente=usuario)
    consulta = ItemCarrinho.objects.filter(produto=produto, carrinho=carrinho_vinculado).first()
    if consulta.quantidade >= 1:
        consulta.delete()
        
    messages.error(request, f'{produto.nome} excluído do carrinho')
    return redirect(request.META.get('HTTP_REFERER', 'menu:index'))


def carrinho_detalhado(request, id):
    item_carrinho = ItemCarrinho.objects.filter(carrinho=id)
    subtotal = calcula_valor_total_carrinho(item_carrinho)
    if item_carrinho.count() == 0:
        return redirect('menu:index')
    carrinho = Carrinho.objects.filter(id=id)
    context = {
        'item_carrinho': item_carrinho,
        'carrinho': carrinho,
        'produtos': Produto.objects.all(),
        'subtotal': subtotal,
    }
    return render(request, 'menu/carrinho.html', context)
