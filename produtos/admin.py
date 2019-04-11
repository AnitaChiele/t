from django.contrib import admin
from django.utils.translation import gettext as _l
from .models import TipoProduto, Produto

admin.site.register(TipoProduto)


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            _l('Campos obrigatórios'), {
                'fields': (
                    'nome', 'tipo', 'codigo', 'preco'
                )
            }
        ),
        (
            'Imagem do produto', {
                'fields': ('imagem',)
            }
        ),
    )
