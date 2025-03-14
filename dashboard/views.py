from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Produto, Vendas
from datetime import datetime
from django.db.models import Count,Sum


def graph(request):
    return render(request, 'graph.html')



def retorna_total_vendido(request):
    total = Vendas.objects.all().aggregate(Sum('total'))['total__sum']
    if request.method == "GET":
        return JsonResponse({'total': total})
    


def relatorio_faturamento(request):
    x = Vendas.objects.all()
    
    meses = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
    data = []
    labels = []
    cont = 0
    mes = datetime.now().month + 1
    ano = datetime.now().year
    for i in range(12): 
        mes -= 1
        if mes == 0:
            mes = 12
            ano -= 1
        
        y = sum([i.total for i in x if i.data.month == mes and i.data.year == ano])
        labels.append(meses[mes-1])
        data.append(y)
        cont += 1

    data_json = {'data': data[::-1], 'labels': labels[::-1]}
     
    return JsonResponse(data_json)


def relatorio_produtos(request):
    produtos = Produto.objects.all()
    print(produtos)
    label = []
    data = []
    for produto in produtos:
        quantidade_vendas = Vendas.objects.filter(nome_produto=produto).aggregate(Count('id'))
        print(quantidade_vendas)
        if not quantidade_vendas['id__count']:
            quantidade_vendas['id__count'] = 0
        label.append(produto.nome)
        data.append(quantidade_vendas['id__count'])

    x = list(zip(label, data))

    x.sort(key=lambda x: x[1], reverse=True)
    x = list(zip(*x))
    print(x)
    return JsonResponse({'labels': x[0][:], 'data': x[1][:]})




