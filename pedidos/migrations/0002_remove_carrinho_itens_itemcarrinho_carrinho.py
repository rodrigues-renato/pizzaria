# Generated by Django 5.1.4 on 2025-02-05 22:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carrinho',
            name='itens',
        ),
        migrations.AddField(
            model_name='itemcarrinho',
            name='carrinho',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='pedidos.carrinho'),
            preserve_default=False,
        ),
    ]
