function valida_dados(boxcliente) {
    if (boxcliente.clinica.value == "") {
        alert("Por favor digite o nome da clínica para prosseguir.");
        boxcliente.clinica.focus();
        return false;
    }
}
