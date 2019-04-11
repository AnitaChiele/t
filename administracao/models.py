from django.db import models
from django.utils.translation import gettext as _l


class Pais(models.Model):

    class Meta:
        verbose_name = 'País'
        verbose_name_plural = 'Países'

    def __str__(self):
        return str(self.nome)

    sigla = models.CharField(
        max_length=4
    )

    nome = models.CharField(
        max_length=150
    )


class UF(models.Model):

    class Meta:
        verbose_name = 'UF'
        verbose_name_plural = 'UF'

    def __str__(self):
        return str(self.sigla)

    pais = models.ForeignKey(
        Pais,
        verbose_name=_l('País'),
        on_delete=models.PROTECT
    )

    sigla = models.CharField(
        max_length=2
    )

    nome = models.CharField(
        max_length=150
    )


class Cidade(models.Model):

    class Meta:
        verbose_name = 'Cidade'
        verbose_name_plural = 'Cidades'

    def __str__(self):
        return str(self.nome)

    uf = models.ForeignKey(
        UF,
        verbose_name=_l('UF'),
        on_delete=models.PROTECT
    )

    nome = models.CharField(
        max_length=255
    )
