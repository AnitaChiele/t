from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext as _l
from .models import Pedido


class PedidoForm(forms.ModelForm):

    class Media:
        js = (
            'js/jquery-3.3.1.min.js',
            'js/jquery.mask.min.js',
            'js/pedidos.js'
        )

    class Meta:
        model = Pedido
        fields = "__all__"

    def clean_data_atualizacao(self):
        """
            Não permite que a data informada seja menor que a última data
            de atualização cadastrada.
            Não permite que a data de atualização seja superior ao dia
            atual.
        """
        ultima_atualizacao = None

        if self.instance.pk:
            ultima_atualizacao = self.instance.data_atualizacao

        data_atualizacao = self.cleaned_data.get('data_atualizacao')
        hoje = timezone.now()

        if ultima_atualizacao and data_atualizacao < ultima_atualizacao:
            raise ValidationError(_l(
                'A data de atualização não pode ser anterior da '
                'última atualização. A última data de atualização '
                'foi: %s'
            ) % ultima_atualizacao.strftime("%d/%m/%Y %H:%M:%S"))

        elif data_atualizacao > hoje:
            raise ValidationError(_l(
                'A data de atualização não pode ser posterior ao dia de '
                'hoje.'
            ))

        return data_atualizacao

    def clean_cnpj(self):
        """
            Remove a máscara do campo
        """
        cnpj = self.cleaned_data.get('cnpj')

        if cnpj:
            cnpj = cnpj.replace(".", "")
            cnpj = cnpj.replace("/", "")
            cnpj = cnpj.replace("-", "")

            return cnpj

        raise ValidationError(_l(
            'O campo de CNPJ é de preenchimento obrigatório.'
        ))

    def clean_cep(self):
        """
            Remove a máscara do campo
        """
        cep = self.cleaned_data.get('cep')

        if cep:
            return cep.replace("-", "")

        raise ValidationError(_l(
            'O campo de CEP é de preenchimento obrigatório.'
        ))

    def clean_telefone(self):
        """
            Remove a máscara do campo
        """
        telefone = self.cleaned_data.get('telefone')

        if telefone:
            telefone = telefone.replace("-", "")
            telefone = telefone.replace("(", "")
            telefone = telefone.replace(")", "")
            return telefone.replace(" ", "")

    cnpj = forms.CharField(
        max_length=18
    )

    cep = forms.CharField(
        max_length=9
    )

    telefone = forms.CharField(
        max_length=15
    )
