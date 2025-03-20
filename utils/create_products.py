import os
import sys
from datetime import datetime
from pathlib import Path
from random import uniform, sample, randint, choice

import django
from django.conf import settings

DJANGO_BASE_DIR = Path(__file__).parent.parent
NUMBER_OF_OBJECTS = 40

sys.path.append(str(DJANGO_BASE_DIR))
os.environ['DJANGO_SETTINGS_MODULE'] = 'pizzaria.settings'
settings.USE_TZ = False

django.setup()

if __name__ == '__main__':
    import faker

    from menu.models import Produto

    Produto.objects.all().delete()
    produtos = []
    fake = faker.Faker('pt_BR')
    ingredientes_base = [
        "mussarela",
        "calabresa",
        "tomate",
        "cebola",
        "azeitona",
        "orégano",
        "presunto",
        "bacon",
        "frango",
        "catupiry",
        "parmesão",
        "pimentão",
        "alho",
        "rúcula",
        "palmito",
    ]

    for _ in range(NUMBER_OF_OBJECTS):
        nome = "Pizza de" + " " + f"{choice(ingredientes_base).capitalize()}"
        descricao = sample(ingredientes_base, k=randint(3, 6))
        preco = round(uniform(25.0, 70.0), 2)
        produtos.append(
            Produto(
                nome=nome, preco=preco, descricao=", ".join(descricao), categoria="Pizza"
            )
        )

    if len(produtos) > 0:
        Produto.objects.bulk_create(produtos)
