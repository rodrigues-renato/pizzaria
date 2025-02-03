from django.shortcuts import render, HttpResponse
from django.contrib import messages
from menu.models import Produto

# Create your views here.

def index(request):
    """
    Primeira tela do site.
    Exibe os itens do cardápio
    """

    messages.success(request, 'Usuário criado com sucesso')
    messages.error(request, 'Usuário deletado com sucesso')
    messages.info(request, 'Usuário informado com sucesso')
    messages.warning(request, 'Usuário avisado com sucesso')

    context = {
        'dataset': Produto.objects.all()
    }
    print(request)
    return render(request, 'menu/index.html', context)