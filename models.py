from db import db
import datetime


class Contatos():
    __tablename__ = "contatos"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone
        self.date = datetime.datetime.now()


class Pedidos(db.Model):
    __tablename__ = "pedidos"

    id = db.Column(db.Integer, primary_key=True)
    data_criacao = db.Column(db.DateTime, nullable=False)
    clinica = db.Column(db.String(100), nullable=False)
    paciente = db.Column(db.String(100), default='')
    servico = db.Column(db.String(100), default='')
    valor = db.Column(db.Float, default=0.0)
    status = db.Column(db.Boolean, default=0)
    data_finalizacao = db.Column(db.Date)

    def __init__(self, clinica, paciente, servico, valor):
        self.data_criacao = datetime.datetime.now()
        self.clinica = clinica
        self.paciente = paciente
        self.servico = servico
        self.valor = valor
        self.status = 0


class Clientes(db.Model):
    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True)
    nome_clinica = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(150), default='')
    numero = db.Column(db.Integer, default=0)
    complemento = db.Column(db.String(150), default='')
    bairro = db.Column(db.String(150), default='')
    cidade = db.Column(db.String(150), default='')
    estado = db.Column(db.String(150), default='')
    telefone = db.Column(db.String(150), default='')

    def __init__(self, nome_clinica, endereco, numero,
                 complemento, bairro, cidade, estado, telefone):
        self.nome_clinica = nome_clinica
        self.endereco = endereco
        self.numero = numero
        self.complemento = complemento
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.telefone = telefone


class Servicos(db.Model):
    __tablename__ = "servicos"

    id = db.Column(db.Integer, primary_key=True)
    servico = db.Column(db.String(100), nullable=False, default='')
    valor = db.Column(db.String(100), default=0.0)

    def __init__(self, servico, valor):
        self.servico = servico
        self.valor = valor


class Fornecedores(db.Model):
    __tablename__ = "fornecedores"

    id = db.Column(db.Integer, primary_key=True)
    nome_forne = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(150), default='')
    numero = db.Column(db.Integer, default=0)
    complemento = db.Column(db.String(150), default='')
    bairro = db.Column(db.String(150), default='')
    cidade = db.Column(db.String(150), default='')
    estado = db.Column(db.String(150), default='')
    telefone = db.Column(db.String(150), default='')

    def __init__(self, nome_forne, endereco, numero, complemento,
                 bairro, cidade, estado, telefone):
        self.nome_forne = nome_forne
        self.endereco = endereco
        self.numero = numero
        self.complemento = complemento
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.telefone = telefone


class Compras(db.Model):
    __tablename__ = "compras"

    id = db.Column(db.Integer, primary_key=True)
    nome_forne = db.Column(db.String(100), default='')
    descricao = db.Column(db.String(300), nullable=False)

    def __init__(self, nome_forne, descricao):
        self.nome_forne = nome_forne
        self.descricao = descricao


class Pagamentos(db.Model):
    __tablename__ = "pagamentos"

    id = db.Column(db.Integer, primary_key=True)
    nome_clinica = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.String(100), default=0.0)
    data_finalizacao = db.Column(db.Date)

    def __init__(self, nome_clinica, valor, data_finalizacao):
        self.nome_clinica = nome_clinica
        self.valor = valor
        self.data_finalizacao = data_finalizacao


class Usuarios(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=True)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
