var excluir = boxpedidocadastrado.querySelector(".excluir")
        var alterar = boxpedidocadastrado.querySelector(".alterar")
        var reabrir = boxpedidocadastrado.querySelector(".reabrir")
        reabrir.disabled = true;
        function finalizar_pedido(boxpedidocadastrado){
            var fin = confirm('Deseja finalizar o pedido?');
            if (fin==true){
                excluir.disabled = true;
                alterar.disabled = true;
                reabrir.disabled = false;
            }
            else{
                excluir.disabled = false;
                alterar.disabled = false;
                reabrir.disabled = true;
            }
        }