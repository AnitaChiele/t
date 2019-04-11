from django.contrib import admin
from django.urls import reverse
from django.utils.translation import gettext as _l
from django.utils.html import mark_safe
from .models import(
    Pedido, StatusPedido, TipoLicenca, PedidoItem
)
from .forms import PedidoForm

admin.site.register(StatusPedido)
admin.site.register(TipoLicenca)


class PedidoItemInline(admin.TabularInline):
    model = PedidoItem
    extra = 1
    min_num = 1


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    inlines = [PedidoItemInline]
    list_display = (
        'numero_pedido', 'cliente', 'status',
        'data_atualizacao',
    )

    ordering = ('-data_atualizacao',)
    readonly_fields = ['data_criacao']

    fieldsets = (
        (
            '', {
                'fields': (
                    'data_criacao', 'cliente', 'licenca', 'status',
                    'data_atualizacao'
                )
            },
        ),
        (
            _l('Nota fiscal eletrônica'), {
                'fields': (
                    'nfe', 'data_emissao_nfe'
                )
            },
        ),
        (
            _l('Geral'), {
                'fields': (
                    'num_pedido_hardware', 'executivo_vendas', 'comentario'
                )
            },
        ),
        (
            _l('Dados de envio'), {
                'fields': (
                    'cnpj', 'pais', 'uf', 'cidade', 'telefone', 'cep',
                    'endereco'
                )
            },
        ),
    )

    form = PedidoForm

    def numero_pedido(self, obj):
        return obj.pk
    numero_pedido.short_description = _l('Número do pedido')
    numero_pedido.admin_order_field = 'pk'

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        pedido = form.instance
        preco_total = 0
        itens_pedido = Pedido.objects.get(pk=pedido.pk).itens.all()

        for item in itens_pedido:
            preco_total += item.produto.preco * item.quantidade

        pedido.preco_total = preco_total
        pedido.save()
