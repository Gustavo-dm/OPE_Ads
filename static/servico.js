function valida_dados (boxservico){
    if (boxservico.servico.value==""){
        alert ("Por favor digite o nome do serviço para prosseguir.");
        boxservico.servico.focus();
        return false;
    }
}