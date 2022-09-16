function valida_dados(boxfornecedor) {
    if (boxfornecedor.fornecedor.value == "") {
        alert("Por favor digite o nome do fornecedor para prosseguir.");
        boxfornecedor.fornecedor.focus();
        return false;
    }
}
