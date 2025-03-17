from django.shortcuts import render, get_object_or_404, redirect
from pedidos.models import Pedido, Carrinho, ItemCarrinho, ItemPedido
from clientes.models import CustomUser, EnderecoUser
from utils.utils import calcula_valor_total_carrinho
from django.http import HttpResponse
from clientes.forms import AddressForm
from django.contrib import messages
from django.core.paginator import Paginator


def finalizar_pedido(request):
    address_form = AddressForm()

    if request.method == 'POST':
        usuario = get_object_or_404(CustomUser, username=request.user)
        carrinho_vinculado = get_object_or_404(Carrinho, cliente=usuario)
        item_carrinho = ItemCarrinho.objects.filter(carrinho=carrinho_vinculado)
        total = calcula_valor_total_carrinho(item_carrinho)
        metodo_pagamento = request.POST.get('metodo_pagamento')
        entrega = request.POST.get('retirada_ou_entrega')
        pedido_esta_correto = True
        # Itens para retirada ficarão como R no banco de dados
        endereco = 'R'

        tempo_de_espera = '20 minutos'
        if entrega == 'entrega':
            endereco = request.POST.get('endereco')
            tempo_de_espera = '40 minutos'

        if not entrega:
            pedido_esta_correto = False

        if not metodo_pagamento:
            pedido_esta_correto = False

        if metodo_pagamento == 'dinheiro':
            troco = float(request.POST.get('dinheiro'))
            if troco < total:
                messages.error(request, f'Seu pedido custa R${total}')
                pedido_esta_correto = False

        # print(request.POST.get)
        if pedido_esta_correto:
            pedido = Pedido.objects.create(
                cliente=usuario,
                carrinho=carrinho_vinculado,
                total=total,
                endereco_envio=endereco,
                metodo_pagamento=metodo_pagamento,
            )

            pedido.finalizar_pedido()
            context = {
                'item_carrinho': item_carrinho,
                'pedido': pedido,
                'tempo_de_espera': tempo_de_espera,
            }
            return render(request, 'pedidos/status_pedido.html', context)
        else:
            messages.error(request, f'Preencha todos os campos')

    usuario = get_object_or_404(CustomUser, username=request.user)
    enderecos = EnderecoUser.objects.filter(user=usuario).all()
    carrinho_vinculado = get_object_or_404(Carrinho, cliente=usuario)
    item_carrinho = ItemCarrinho.objects.filter(carrinho=carrinho_vinculado)
    qtd_itens_carrinho = item_carrinho.count()
    if qtd_itens_carrinho == 0:
        return redirect('menu:index')

    total = calcula_valor_total_carrinho(item_carrinho)

    context = {
        'usuario': usuario,
        'carrinho': carrinho_vinculado,
        'enderecos': enderecos,
        'item_carrinho': item_carrinho,
        'qtd_item_carrinho': qtd_itens_carrinho,
        'subtotal': total,
        'address_form': address_form,
    }

    return render(request, 'pedidos/finalizar_pedido.html', context)


# O usuário pode escolher não se registrar, porém ele deve informar o nome
# e o telefone. Ambos serão armazenados no banco de dados. Os outros dados
# podem ser definidos como null=True, como não obrigatórios
def historico_de_pedidos(request):
    usuario = get_object_or_404(CustomUser, username=request.user)
    pedidos = Pedido.objects.filter(cliente=usuario).all().order_by('-criado_em')
    paginator = Paginator(pedidos, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    itens_pedidos = ItemPedido.objects.filter(cliente=usuario).all()
    context = {
        'itens_pedidos': itens_pedidos,
        'page_obj': page_obj,
    }
    return render(request, 'pedidos/historico.html', context)
