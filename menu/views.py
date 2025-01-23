from django.shortcuts import render, HttpResponse
from menu.models import Produto

# Create your views here.

def index(request):
    """
    Primeira tela do site.
    Exibe os itens do cardápio
    """
    context = {
        'dataset': Produto.objects.all()
    }
    print(request)
    return render(request, 'menu/index.html', context)