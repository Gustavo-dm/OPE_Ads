function valida_dados (boxpedido){
    if (boxpedido.cliente.value=="Selecione"){
        alert ("Por favor selecione a clínica para prosseguir.");
        boxpedido.cliente.focus();
        return false;
    }
}