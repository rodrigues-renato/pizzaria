def calcula_valor_total_carrinho(carrinho):
    subtotal = 0
    if carrinho:
        for item in carrinho:
            subtotal += item.quantidade * item.produto.preco
    return subtotal