# Documentação Arquesys

### Conexão com banco de dados
- **MYSQL_DATABASE_USER**: indica o usuário MySQL
- **MYSQL_DATABASE_PASSWORD**: indica a senha para conexão
- **MYSQL_DATABASE_DB**: indica o database (nesse caso ele precisa estar criado)
- **MYSQL_DATABASE_HOST**: host que será executado

### Rotas

#### Route _"/"_
- página de login para todos os usuários

#### Route _"/contato"_
- página para não-usuários com interesse no sistema

#### Route _"/inicial"_
- contém opções para navegar dentro do sistema, como:
  1. Criação de novos pedidos
  2. Criação de novos fornecedores
  3. Geração de relatórios

#### Route _"/inicial/pedido"_
>    **GET**
     - formulário para cadastro de pedido, tendo escolha da clínica e o serviço prestado
    **POST**
     - faz a inserção dos dados no banco e redireciona o usuário para a url "/pedido/<int\:nid>", substituindo **<int\:nid>** pelo ID do pedido

#### Route _"/inicial/pedido/<int\:nid>"_
>    **GET**
     - apresenta os dados cadastrados do pedido com os campos bloqueados
    **POST**
     - altera o status do pedido para finalizado, fazendo com que ele possa aparecer nos relatórios

#### Route _"/inicial/lista/pedidos"_
- Apresenta os pedidos cadastrados

#### Route _"/inicial/cliente"_
>    **GET**
     - formulário para cadastro de cliente
     **POST**
     - faz a inserção dos dados no banco e redireciona o usuário para a url "/cliente/<int\:nid>", substituindo **<int\:nid>** pelo ID do cliente

#### Route _"/inicial/cliente/<int\:nid>"_
>    **GET**
     - apresenta os dados cadastrados do pedido com os campos bloqueados
     
#### Route _"/inicial/lista/cliente"_
- Apresenta os clientes cadastrados

#### Route _"/inicial/servico"_
>    **GET**
     - formulário para cadastro do serviço
     **POST**
     - faz a inserção dos dados no banco e redireciona o usuário para a url "/servico/<int\:nid>", substituindo **<int\:nid>** pelo ID do serviço

#### Route _"/inicial/servico/<int\:nid>"_
>    **GET**
     - apresenta os dados cadastrados do serviço com os campos bloqueados

#### Route _"/inicial/lista/servico"_
- Apresenta os serviços cadastrados

#### Route _"/inicial/fornecedor"_
>    **GET**
     - formulário para cadastro de fornecedor
     **POST**
     - faz a inserção dos dados no banco e redireciona o usuário para a url "/fornecedor/<int\:nid>", substituindo **<int\:nid>** pelo ID do fornecedor

#### Route _"/inicial/fornecedor/<int\:nid>"_
>    **GET**
     - apresenta os dados cadastrados do fornecedor com os campos bloqueados

#### Route _"/inicial/lista/fornecedor"_
- Apresenta os fornecedores cadastrados

#### Route _"/inicial/compras"_
>    **GET**
     - formulário para cadastro de lista de compras
     **POST**
     - faz a inserção dos dados no banco e redireciona o usuário para a url "/compras/<int\:nid>", substituindo **<int\:nid>** pelo ID da lista

#### Route _"/inicial/compras/<int\:nid>"_
>    **GET**
     - apresenta os dados cadastrados da lista de compras com os campos bloqueados

#### Route _"/inicial/lista/compras"_
- Apresenta as listas de compras cadastradas

#### Route _"/inicial/relatorios"_
>    **GET**
     - apresenta em tela campos de calendário para selecionar o período desejado do fechamento
     **POST**
     - busca no banco de dados as informações recebidas no método GET e "imprime" um relatório com os pedidos finalizado
