def calcula_valor_total_carrinho(carrinho):
    """
    Recebe todos os itens de determinado carrinho e retorna o valor total.
   
    Exemplo: 

    carrinho = ItemCarrinho.objects.filter(carrinho=ID)
   
    total = calcula_valor_total_carrinho(carrinho)
    """
    subtotal = 0
    if carrinho:
        for item in carrinho:
            subtotal += item.quantidade * item.produto.preco
    return subtotal