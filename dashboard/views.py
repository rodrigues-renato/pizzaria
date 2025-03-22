from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from pedidos.models import ItemPedido
from menu.models import Produto
from datetime import datetime
from django.db.models import Count,Sum


def graph(request):
    return render(request, 'graph.html')



# def retorna_total_vendido(request):
#     total = ItemPedido.objects.all().aggregate(Sum('total'))['total__sum']
#     if request.method == "GET":
#         return JsonResponse({'total': total})



def relatorio_faturamento(request):
    x = ItemPedido.objects.all()
    
    meses = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
    data = []
    labels = []
    cont = 0
    mes = 0
    ano = datetime.now().year
    for m in range(0,12): 
        
        # if mes == 0:
        #     mes = 12
        #     ano -= 1
        
        y = sum([i.produto.preco * i.quantidade for i in x if i.data.month == m+1 and i.data.year == ano])
        
        labels.append(meses[m])
        data.append(y)
        cont += 1
        print(data, labels)
    data_json = {'data': data[::], 'labels': labels[::]}
     
    return JsonResponse(data_json)


def relatorio_vendas(request):
    x = ItemPedido.objects.all()
    
    meses = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
    data = []
    labels = []
    cont = 0
    mes = 0
    ano = datetime.now().year
    for m in range(0,12): 
        
        # if mes == 0:
        #     mes = 12
        #     ano -= 1
        
        y = sum([i.quantidade for i in x if i.data.month == m+1 and i.data.year == ano])
        
        labels.append(meses[m])
        data.append(y)
        cont += 1
        print(data, labels)
    data_json = {'data': data[::], 'labels': labels[::]}
     
    return JsonResponse(data_json)

def relatorio_produtos(request):
    produtos = (ItemPedido.objects
          .select_related('produto')  # Fazendo a junção com a tabela Produto
          .values('produto__categoria')  # Incluindo a categoria do produto
          .annotate(total=Count('id')))  
    print(produtos)
    label = []
    data = []
    for produto_unico in produtos:
        # quantidade_vendas = ItemPedido.objects.filter(produto=produto_unico).aggregate(Count('id'))
        # print(quantidade_vendas)
        if not produto_unico['total']:
            produto_unico['total'] = 0
        label.append(produto_unico['produto__categoria'])
        data.append(produto_unico['total'])

    x = list(zip(label, data))

    x.sort(key=lambda x: x[1], reverse=True)
    x = list(zip(*x))
    print(x)
    return JsonResponse({'labels': x[0][:], 'data': x[1][:]})




