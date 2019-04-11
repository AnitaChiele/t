# Generated by Django 2.0.13 on 2019-04-10 19:35

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('administracao', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('produtos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_criacao', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data de criação')),
                ('preco_total', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='Preço')),
                ('data_atualizacao', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data atualização')),
                ('comentario', models.TextField(blank=True, null=True)),
                ('num_pedido_hardware', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Número pedido hardware')),
                ('nfe', models.IntegerField(blank=True, null=True, verbose_name='NFe número')),
                ('data_emissao_nfe', models.DateTimeField(blank=True, null=True, verbose_name='Data emissão NFe')),
                ('cnpj', models.CharField(max_length=14)),
                ('telefone', models.CharField(max_length=11)),
                ('cep', models.CharField(max_length=8)),
                ('endereco', models.CharField(max_length=1000)),
                ('cidade', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='administracao.Cidade')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Cliente')),
                ('executivo_vendas', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='executivo_venda', to=settings.AUTH_USER_MODEL, verbose_name='Executivo de vendas')),
            ],
            options={
                'verbose_name': 'Pedido',
                'verbose_name_plural': 'Pedidos',
            },
        ),
        migrations.CreateModel(
            name='PedidoItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='itens', to='pedidos.Pedido')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='produtos.Produto')),
            ],
            options={
                'verbose_name': 'Item do pedido',
                'verbose_name_plural': 'Item do pedido',
            },
        ),
        migrations.CreateModel(
            name='StatusPedido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('descricao', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Status',
                'verbose_name_plural': 'Status',
            },
        ),
        migrations.CreateModel(
            name='TipoLicenca',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('descricao', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Tipo da licença',
                'verbose_name_plural': 'Tipos de licença',
            },
        ),
        migrations.AddField(
            model_name='pedido',
            name='licenca',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pedidos.TipoLicenca'),
        ),
        migrations.AddField(
            model_name='pedido',
            name='pais',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='administracao.Pais'),
        ),
        migrations.AddField(
            model_name='pedido',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pedidos.StatusPedido'),
        ),
        migrations.AddField(
            model_name='pedido',
            name='uf',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='administracao.UF'),
        ),
    ]