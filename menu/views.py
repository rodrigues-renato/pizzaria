from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.contrib import messages
from menu.models import Produto
from pedidos.models import ItemCarrinho, Carrinho, Pedido
from clientes.models import CustomUser
from utils.utils import calcula_valor_total_carrinho
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator


@login_required(login_url='clientes:login_cliente')
def index(request):
    """
    Primeira tela do site.
    Exibe os itens do cardápio
    """
    produtos = Produto.objects.all()
    paginator = Paginator(produtos, 10)  # 10 produtos por pagina
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    usuario = get_object_or_404(CustomUser, username=request.user)
    carrinho_vinculado = get_object_or_404(Carrinho, cliente=usuario)
    
    #Incorporacao da view carrinho_detalhado
    item_carrinho = ItemCarrinho.objects.filter(carrinho=carrinho_vinculado)
    subtotal = calcula_valor_total_carrinho(item_carrinho)

    itens_carrinho = ItemCarrinho.objects.filter(carrinho=carrinho_vinculado).count()

    context = {
        'page_obj': page_obj,
        'carrinho': carrinho_vinculado,
        'qtd_item_carrinho': itens_carrinho,
        'item_carrinho': item_carrinho,
        'produtos': produtos,
        'subtotal': subtotal,
    }

    return render(request, 'menu/index.html', context)


@login_required(login_url='clientes:login_cliente')
def buscar(request):
    usuario = get_object_or_404(CustomUser, username=request.user)
    carrinho_vinculado = get_object_or_404(Carrinho, cliente=usuario)
    itens_carrinho = ItemCarrinho.objects.filter(carrinho=carrinho_vinculado).count()

    query = request.GET.get("q", '').strip()
    if query == "":
        return redirect('menu:index')

    produtos = Produto.objects.filter(
        Q(nome__icontains=str(query))
        | Q(descricao__icontains=str(query))
        | Q(categoria__icontains=str(query))
    ).order_by('-nome')
    paginator = Paginator(produtos, 10)  # 10 produtos por pagina
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'carrinho': carrinho_vinculado,
        'qtd_item_carrinho': itens_carrinho,
    }

    return render(request, 'menu/index.html', context)


@login_required(login_url='clientes:login_cliente')
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


@login_required(login_url='clientes:login_cliente')
def remover_do_carrinho(request, id):
    usuario = get_object_or_404(CustomUser, username=request.user)

    produto = get_object_or_404(Produto, id=id)
    carrinho_vinculado = get_object_or_404(Carrinho, cliente=usuario)
    consulta = ItemCarrinho.objects.filter(
        produto=produto, carrinho=carrinho_vinculado
    ).first()
    if consulta.quantidade > 1:
        consulta.quantidade -= 1
        consulta.save()
    elif consulta.quantidade == 1:
        consulta.delete()

    messages.warning(request, f'{produto.nome} removido do carrinho')
    return redirect(request.META.get('HTTP_REFERER', 'menu:index'))


@login_required(login_url='clientes:login_cliente')
def excluir_do_carrinho(request, id):
    usuario = get_object_or_404(CustomUser, username=request.user)

    produto = get_object_or_404(Produto, id=id)
    carrinho_vinculado = get_object_or_404(Carrinho, cliente=usuario)
    consulta = ItemCarrinho.objects.filter(
        produto=produto, carrinho=carrinho_vinculado
    ).first()
    if consulta.quantidade >= 1:
        consulta.delete()

    messages.error(request, f'{produto.nome} excluído do carrinho')
    return redirect(request.META.get('HTTP_REFERER', 'menu:index'))


@login_required(login_url='clientes:login_cliente')
def carrinho_detalhado(request, id):
    item_carrinho = ItemCarrinho.objects.filter(carrinho=id)
    carrinho = Carrinho.objects.filter(cliente=request.user)
    permite_view = True
    if item_carrinho.first():
        # Nao permite visualizar o carrinho de outro user
        if item_carrinho.first().carrinho != carrinho.first():
            permite_view = False
    # Nao permite ver carrinho detalhado sem itens no carrinho
    if item_carrinho.count() == 0:
        permite_view = False

    if not permite_view:
        return redirect('menu:index')

    subtotal = calcula_valor_total_carrinho(item_carrinho)
    carrinho = Carrinho.objects.filter(id=id)
    context = {
        'item_carrinho': item_carrinho,
        'carrinho': carrinho,
        'produtos': Produto.objects.all(),
        'subtotal': subtotal,
    }
    return render(request, 'menu/carrinho.html', context)
