from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.utils.translation import gettext as _l
from administracao.models import UF, Cidade, Pais
from produtos.models import Produto


class StatusPedido(models.Model):

    class Meta:
        verbose_name = 'Status'
        verbose_name_plural = 'Status'

    def __str__(self):
        return self.nome

    nome = models.CharField(
        max_length=200
    )

    descricao = models.TextField(
        blank=True,
        null=True
    )


class TipoLicenca(models.Model):

    class Meta:
        verbose_name = 'Tipo da licença'
        verbose_name_plural = 'Tipos de licença'

    def __str__(self):
        return self.nome

    nome = models.CharField(
        max_length=255
    )

    descricao = models.TextField(
        blank=True,
        null=True
    )


class Pedido(models.Model):

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self):
        return "%d" % self.pk

    cliente = models.ForeignKey(
        User,
        verbose_name=_l('Cliente'),
        on_delete=models.PROTECT
    )

    data_criacao = models.DateTimeField(
        default=timezone.now,
        verbose_name=_l('Data de criação'),
    )

    licenca = models.ForeignKey(
        TipoLicenca,
        on_delete=models.PROTECT
    )

    status = models.ForeignKey(
        StatusPedido,
        on_delete=models.PROTECT
    )

    preco_total = models.DecimalField(
        verbose_name=_l('Preço'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        null=True,
        blank=True
    )

    data_atualizacao = models.DateTimeField(
        default=timezone.now,
        verbose_name=_l('Data atualização'),
    )

    comentario = models.TextField(
        null=True,
        blank=True
    )

    executivo_vendas = models.ForeignKey(
        'auth.User',
        verbose_name=_l('Executivo de vendas'),
        on_delete=models.PROTECT,
        related_name='executivo_venda',
        null=True,
        blank=True
    )

    num_pedido_hardware = models.IntegerField(
        verbose_name=_l('Número pedido hardware'),
        validators=[MinValueValidator(1)],
        null=True,
        blank=True
    )

    nfe = models.IntegerField(
        verbose_name=_l('NFe número'),
        null=True,
        blank=True
    )

    data_emissao_nfe = models.DateTimeField(
        verbose_name=_l('Data emissão NFe'),
        null=True,
        blank=True
    )

    cnpj = models.CharField(
        max_length=14
    )

    uf = models.ForeignKey(
        UF,
        on_delete=models.PROTECT
    )

    cidade = models.ForeignKey(
        Cidade,
        on_delete=models.PROTECT
    )

    telefone = models.CharField(
        max_length=11
    )

    cep = models.CharField(
        max_length=8
    )

    endereco = models.CharField(
        max_length=1000
    )

    pais = models.ForeignKey(
        Pais,
        on_delete=models.PROTECT
    )


class PedidoItem(models.Model):

    class Meta:
        verbose_name = 'Item do pedido'
        verbose_name_plural = 'Item do pedido'

    def __str__(self):
        return str(self.produto)

    pedido = models.ForeignKey(
        Pedido,
        related_name='itens',
        on_delete=models.PROTECT
    )

    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT
    )

    quantidade = models.IntegerField(
        validators=[MinValueValidator(1)],
        default=1
    )
