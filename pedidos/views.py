from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from pedidos.models import Pedido


def get_pedidos(request, pedido_id):
    """
        Seleciona o pedido do usuário.
        Se for um superadmin acessando libera a visualização
        dos pedidos.
    """
    usuario_logado = request.user
    pedido = None

    if not usuario_logado.is_superuser:
        pedido = Pedido.objects.filter(
            pk=pedido_id,
            cliente=usuario_logado.pk,
        )
    else:
        pedido = Pedido.objects.filter(
            pk=pedido_id,
        )

    return pedido


def lista_resumo_pedido(request):
    """
        função acessada pela URL

        Seleciona todos os pedidos do usuário logado.
        Se o usuário for um superusuário, ele seleciona
        todos os pedidos.
    """
    usuario_logado = request.user
    html = 'admin/pedidos/detalhes.html'
    usuario_logado = request.user

    if not usuario_logado.is_superuser:
        pedidos = Pedido.objects.filter(
            cliente=usuario_logado.pk,
        )
    else:
        pedidos = Pedido.objects.all()

    if not pedidos:
        html = 'admin/pedidos/detalhes_not_found.html'

        return render(request, html, {})

    # limita para os 10 mais recentes
    pedidos = pedidos.order_by("-pk")[:10]
    dados = []

    for p in pedidos:
        titulo_pedido = "Pedido %d - %s - %s - %s" % (
            p.pk,
            p.licenca,
            p.status,
            p.data_atualizacao.strftime("%d/%m/%Y %H:%M:%S")
        )

        dados.append({
            'pedidos': {
                'titulo': titulo_pedido,
                'id': p.pk
            }
        })

    context = {
        'results': dados
    }

    print(dados)

    return render(request, html, context)


def get_content_type(obj):
    """
        Retorna o content type do objeto.
    """
    return ContentType.objects.get_for_model(
        obj, for_concrete_model=False
    )


def get_history(pedido):
    """
        Retorna todo o histórico do objeto.

        Returns:
            [QuerySet] -- [queryset do objeto]
    """
    return LogEntry.objects.filter(
        object_id=pedido.pk,
        content_type=get_content_type(pedido)
    ).select_related().order_by('action_time')


def get_json_pedido(pedido):
    data_emissao_nfe = None
    executivo_vendas = None

    if pedido.data_emissao_nfe:
        data_emissao_nfe = pedido.data_emissao_nfe.strftime(
            "%d/%m/%Y %H:%M:%S"
        )

    if pedido.executivo_vendas:
        executivo_vendas = "%s %s (%s)" % (
            pedido.executivo_vendas.first_name,
            pedido.executivo_vendas.last_name,
            str(pedido.executivo_vendas)
        )

    return {
        'cep': pedido.cep,
        'uf': pedido.uf.sigla,
        'cidade': pedido.cidade.nome,
        'pais': pedido.pais.nome,
        'cnpj': pedido.cnpj,
        'comentario': pedido.comentario,
        'data_atualizacao': pedido.data_atualizacao.strftime(
            "%d/%m/%Y %H:%M:%S"
        ),
        'data_criacao': pedido.data_criacao.strftime(
            "%d/%m/%Y"
        ),
        'data_emissao_nfe': data_emissao_nfe,
        'endereco': pedido.endereco,
        'executivo_vendas': executivo_vendas,
        'licenca': pedido.licenca.nome,
        'nfe': pedido.nfe,
        'pedido_num_hardware': pedido.num_pedido_hardware,
        'telefone': pedido.telefone,
        'preco_total': pedido.preco_total,
        'status': pedido.status.nome,
    }


def get_json_history_pedido(pedido):
    historys = get_history(pedido)

    return [{
        'data_hr': h.action_time.strftime(
            "%d/%m/%Y %H:%M:%S"
        ),
        'msg': h.get_change_message().replace(". ", ". <br />")
    } for h in historys]


def get_json_produtos_pedido(pedido):
    produtos = pedido.itens.all()

    return [{
        'img_url': '/media/uploads/%s' % str(
            p.produto.imagem
        ) if p.produto.imagem else None,
        'nome_produto': str(p),
        'qtd': p.quantidade
    } for p in produtos]


def detalhes_pedido(request):
    """
        chamada pelo ajax para carregar as informações
        completa sobre o pedido.
    """
    pedido_id = request.POST.get('pedido_detalhe')
    pedido = get_pedidos(request, pedido_id)

    if pedido:
        pedido = pedido.first()

        return JsonResponse({
            'pedido': get_json_pedido(pedido),
            'produtos': get_json_produtos_pedido(pedido),
            'historico': get_json_history_pedido(pedido)
        })

    return HttpResponse(status=204)
