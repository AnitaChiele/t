function write_pedido(pedido, id){
    // carrega dados do pedido:
    $(".pedido_"+id+"_licenca").html(pedido['licenca']);
    $(".pedido_"+id+"_status").html(pedido['status']);
    $(".pedido_"+id+"_preco").html(pedido['preco_total']);
    $(".pedido_"+id+"_data_criacao").html(pedido['data_criacao']);
    $(".pedido_"+id+"_cnpj").html(pedido['cnpj']);
    $(".pedido_"+id+"_uf").html(pedido['uf']);
    $(".pedido_"+id+"_cidade").html(pedido['cidade']);
    $(".pedido_"+id+"_cep").html(pedido['cep']);
    $(".pedido_"+id+"_endereco").html(pedido['endereco']);
    $(".pedido_"+id+"_pais").html(pedido['pais']);
    $(".pedido_"+id+"_comentario").html(pedido['comentario']);
    $(".pedido_"+id+"_executivo_vendas").html(pedido['executivo_vendas']);
    $(".pedido_"+id+"_num_hardware").html(pedido['pedido_num_hardware']);
    $(".pedido_"+id+"_nfe").html(pedido['nfe']);
    $(".pedido_"+id+"_data_emissao_nfe").html(pedido['data_emissao_nfe']);
    $(".pedido_"+id+"_telefone").html(pedido['telefone']);
}

function write_produtos(prod, id){
    // carrega dados dos produtos do pedido:
    const prod_length = prod.length
    let html = "";
    let i = 0;

    for(i; i < prod_length; i++){
        html += `
          <li>
            <div class="col-xl-11 col-md-11 col-sm-11 col-11 ">
        `

        if(prod[i]['img_url']){
          html += '<image src="'+prod[i]['img_url']+'"  height=50 >'
        }

        html += prod[i]['nome_produto'] + `
          </div>
          <div class="col-md-1 col-sm-1 col-1">
          <i class="fas fa-times"></i>
        ` + prod[i]['qtd'] + `
          </div>
          </li>
        `
    }

    $(".p_produtos_"+id).html(html);
}

function write_historico(h, id){
    // carrega dados do histórico do pedido:
    const h_length = h.length
    let i = 0;

    for(i; i < h_length; i++){
        $(".tbody_history_"+id).append('<tr>')
        $(".tbody_history_"+id).append('<th scope="row">'+h[i]['data_hr']+'</th>')
        $(".tbody_history_"+id).append('<td>'+h[i]['msg']+'</td>')
    }
}

function apply_masks(id){
    // aplica as máscaras:
    $(".pedido_"+id+"_cnpj").mask("00.000.000/0000-00");
    $(".pedido_"+id+"_cep").mask("00000-000");
    $(".pedido_"+id+"_telefone").mask("(00) 00000-0000");
}

$('#detalhes_pedido').on('show.bs.collapse', function (e) {
    const id = $(e.target).siblings('.card-header').find('.pedido_detalhe').attr("data-pedido-id")
    const csrf = $(".token").find('input[name=csrfmiddlewaretoken]').val()


    $.ajax({
        type: "POST",
        url: '/admin/pedido/detalhes/full/',
        data: {
          "pedido_detalhe": id,
          "csrfmiddlewaretoken": csrf,
        },
        success:function(data){
          write_pedido(data['pedido'], id)
          write_produtos(data['produtos'], id)
          write_historico(data['historico'], id)
          apply_masks(id)
        },
        beforeSend: function(){
          // manipular os loaders de acordo com a necessidade
          // de exibí-los ou não.
          // $('.loader').css({display:"block"});
        },
        complete: function(){
          // manipular os loaders de acordo com a necessidade
          // de exibí-los ou não.
          // $('.loader').css({display:"none"});
        }
    })
})