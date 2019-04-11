import re
from datetime import datetime
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from administracao.models import Pais, UF, Cidade
from produtos.models import Produto
from pedidos.models import(
    Pedido, TipoLicenca, StatusPedido
)


def write_html_with_test_error(response):
    """
        Gera um html da tela com o erro do teste unitário. É como se
        o erro tivesse ocorrido durante o uso do sistema.

        Caso não haja erros, o arquivo fica em branco.

        Para visualizar o arquivo basta abrí-lo no navegador.
    """
    content = response.content.decode("UTF-8")

    with open('teste-unitario.html', 'w') as static_file:
        static_file.write(content)

    return content


def dt_hr_now():
    now = datetime.now()

    date = "%d/%d/%d" % (
        now.day,
        now.month,
        now.year
    )

    hora = "%d:%d:%d" % (
        now.hour,
        now.minute,
        now.second
    )

    return date, hora


class PedidoTestCase(TestCase):
    fixtures = ['all.json', ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.cl = Client()

        cls.produtos = Produto.objects.all()
        cls.cliente1 = User.objects.filter(pk=2).first()
        cls.licenca1 = TipoLicenca.objects.first()

        cls.status_em_andamento = StatusPedido.objects.filter(
            nome='Aguardando aprovação'
        ).first()

        cls.pais_bra = Pais.objects.filter(
            sigla='BRA'
        ).first()

        cls.uf_rs = UF.objects.filter(
            pais=cls.pais_bra,
            sigla='RS'
        ).first()

        cls.cidade_poa = Cidade.objects.filter(
            uf=cls.uf_rs,
            nome="Porto Alegre"
        ).first()

        cls.p_tablet = cls.produtos[0]
        cls.p_suporte = cls.produtos[1]
        cls.p_gaveta = cls.produtos[2]
        cls.p_software1 = cls.produtos[3]
        cls.p_mp = cls.produtos[4]
        cls.p_leitor = cls.produtos[5]
        cls.p_software2 = cls.produtos[6]

    def test_pedido_add(self):
        """
            Cadastra um pedido válido.
        """
        self.cl.login(username='anita', password='2w3e4r5t')

        date, hora = dt_hr_now()

        data = {
            'cliente': self.cliente1.pk,
            'data_criacao': date + " " + hora,
            'data_atualizacao_0': date,
            'data_atualizacao_1': hora,
            'licenca': self.licenca1.pk,
            'status': self.status_em_andamento.pk,
            'cnpj': '08.081.235/0001-67',
            'pais': self.pais_bra.pk,
            'uf': self.uf_rs.pk,
            'cidade': self.cidade_poa.pk,
            'telefone': '(51) 000000000',
            'cep': '90610-380',
            'endereco': 'Rua Olívio Bernardes Machado',

            'itens-TOTAL_FORMS': 3,
            'itens-INITIAL_FORMS': 0,
            'itens-MIN_NUM_FORMS': 1,
            'itens-MAX_NUM_FORMS': 1000,

            'itens-0-produto': self.p_tablet.pk,
            'itens-0-quantidade': '1',

            'itens-1-produto': self.p_gaveta.pk,
            'itens-1-quantidade': '1',

            'itens-2-produto': self.p_software1.pk,
            'itens-2-quantidade': '2'
        }

        url = reverse('admin:pedidos_pedido_add')
        response = self.cl.post(url, data)
        write_html_with_test_error(response)

        p = Pedido.objects.last()

        self.assertTrue(p.data_criacao)

    def test_pedido_edit(self):
        """
            Edição válida.
        """
        self.cl.login(username='anita', password='2w3e4r5t')

        date, hora = dt_hr_now()
        p = Pedido.objects.last()

        if not p:
            # cadastra o pedido que vai ser atualizado.
            self.test_pedido_add()
            p = Pedido.objects.last()

        prods = p.itens.all()

        data = {
            'cliente': p.cliente.pk,
            'data_criacao': p.data_criacao,

            # update data atualização
            'data_atualizacao_0': date,
            'data_atualizacao_1': hora,

            'licenca': p.licenca.pk,
            'status': p.status.pk,
            'cnpj': p.cnpj,
            'pais': p.pais.pk,
            'uf': p.uf.pk,
            'cidade': p.cidade.pk,

            # update telefone
            'telefone': '(51) 405000000',

            'cep': p.cep,
            'endereco': p.endereco,

            'itens-TOTAL_FORMS': 3,
            'itens-INITIAL_FORMS': 0,
            'itens-MIN_NUM_FORMS': 1,
            'itens-MAX_NUM_FORMS': 1000,

            'itens-0-produto': prods[0].produto.pk,
            'itens-0-quantidade': prods[0].quantidade,

            'itens-1-produto': prods[1].produto.pk,
            'itens-1-quantidade': prods[1].quantidade,

            'itens-2-produto': prods[2].produto.pk,
            'itens-2-quantidade': prods[2].quantidade
        }

        url = reverse('admin:pedidos_pedido_change', args=(p.pk,))
        response = self.cl.post(url, data)
        write_html_with_test_error(response)

        p = Pedido.objects.last()

        self.assertEquals(p.telefone, '51405000000')

    def test_pedido_edit_data_atualizacao(self):
        """
            Edição inválida. Busca por msg de erro:
            A data de atualização não pode ser posterior ao dia de hoje.
        """
        self.cl.login(username='anita', password='2w3e4r5t')

        _, hora = dt_hr_now()
        now = datetime.now()

        date = "%d/%d/%d" % (
            now.day,
            now.month,
            (now.year + 1)
        )

        p = Pedido.objects.last()

        if not p:
            # cadastra o pedido que vai ser atualizado.
            self.test_pedido_add()
            p = Pedido.objects.last()

        prods = p.itens.all()

        data = {
            'cliente': p.cliente.pk,
            'data_criacao': p.data_criacao,

            # update data atualização
            'data_atualizacao_0': date,
            'data_atualizacao_1': hora,

            'licenca': p.licenca.pk,
            'status': p.status.pk,
            'cnpj': p.cnpj,
            'pais': p.pais.pk,
            'uf': p.uf.pk,
            'cidade': p.cidade.pk,

            # update telefone
            'telefone': '(51) 405000000',

            'cep': p.cep,
            'endereco': p.endereco,

            'itens-TOTAL_FORMS': 3,
            'itens-INITIAL_FORMS': 0,
            'itens-MIN_NUM_FORMS': 1,
            'itens-MAX_NUM_FORMS': 1000,

            'itens-0-produto': prods[0].produto.pk,
            'itens-0-quantidade': prods[0].quantidade,

            'itens-1-produto': prods[1].produto.pk,
            'itens-1-quantidade': prods[1].quantidade,

            'itens-2-produto': prods[2].produto.pk,
            'itens-2-quantidade': prods[2].quantidade
        }

        url = reverse('admin:pedidos_pedido_change', args=(p.pk,))
        response = self.cl.post(url, data)
        content = write_html_with_test_error(response)

        search = re.compile(
            'A data de atualização não pode ser posterior '
            'ao dia de hoje.'
        )
        match = re.search(search, content)

        self.assertEquals(response.status_code, 200)
        self.assertTrue(match)
