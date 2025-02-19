from django.shortcuts import render, get_object_or_404, redirect
from pedidos.models import Pedido, Carrinho, ItemCarrinho
from clientes.models import CustomUser
from utils.utils import calcula_valor_total_carrinho
from django.http import HttpResponse


def finalizar_pedido(request, id):
    if request.method == 'POST':
        usuario = get_object_or_404(CustomUser, username=request.user)
        carrinho_vinculado = get_object_or_404(Carrinho, cliente=usuario)
        item_carrinho = ItemCarrinho.objects.filter(carrinho=carrinho_vinculado)
        total = calcula_valor_total_carrinho(item_carrinho)
        metodo_pagamento = request.POST.get('metodo_pagamento')
        entrega = request.POST.get('retirada_ou_entrega')
        
        print(request.POST.get)

        # pedido = Pedido.objects.create(
        #     cliente=usuario,
        #     carrinho=carrinho_vinculado,
        #     total=total,
        #     endereco_envio=f'{usuario.rua}, {usuario.numero}, {usuario.bairro}',
        #     metodo_pagamento=metodo_pagamento,
        # )
        # # Terminar template para conferir status do pedido
        # return render(request, 'pedidos/status_pedido.html', {})
    usuario = get_object_or_404(CustomUser, username=request.user)
    endereco = UserEndereco.objects.filter(user=usuario)
    carrinho_vinculado = get_object_or_404(Carrinho, cliente=usuario)
    item_carrinho = ItemCarrinho.objects.filter(carrinho=carrinho_vinculado)
    total = calcula_valor_total_carrinho(item_carrinho)

    context = {
        'usuario': usuario,
        'carrinho': carrinho_vinculado,
        'rua': usuario.rua,
        'bairro': usuario.bairro,
        'numero': usuario.numero,
        'item_carrinho': item_carrinho,
        'subtotal': total,
    }

    return render(request, 'pedidos/finalizar_pedido.html', context)


# O usuário pode escolher não se registrar, porém ele deve informar o nome
# e o telefone. Ambos serão armazenados no banco de dados. Os outros dados
# podem ser definidos como null=True, como não obrigatórios
# boa garotinhoooo
def ver_pedido(request, id): ...
