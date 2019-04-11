from django.db import models
from django.utils.translation import gettext as _l
from django.core.validators import MinValueValidator


class TipoProduto(models.Model):

    class Meta:
        verbose_name = 'Tipo do produto'
        verbose_name_plural = 'Tipos do produto'

    def __str__(self):
        return self.nome

    nome = models.CharField(
        max_length=200
    )


class Produto(models.Model):

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def __str__(self):
        return "%s %d" % (self.nome, self.codigo)

    nome = models.CharField(
        max_length=200
    )

    codigo = models.IntegerField(
        unique=True,
        validators=[MinValueValidator(1)]
    )

    preco = models.DecimalField(
        verbose_name=_l('Preço'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )

    imagem = models.FileField(
        upload_to='produtos/',
        blank=True,
        null=True
    )

    tipo = models.ForeignKey(
        TipoProduto,
        on_delete=models.PROTECT
    )
