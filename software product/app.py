import os
import pdfkit
from datetime import datetime
from flask import Flask, flash, session, render_template, request, redirect, make_response
from flask_sqlalchemy import SQLAlchemy
from models import *
from passlib.hash import sha256_crypt
import functools

app = Flask(__name__)
app.secret_key = 'askjdnaskjdnaksjdn'
app.config['SESSION_TYPE'] = 'memcached'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:ua-i&Crlo4s/@localhost/arquesys'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

def login_required(func):
    def secure_function(**kwargs):
        if not session.get('logged_in'):
            return redirect("/login")
        return func(**kwargs)
    return secure_function

@app.route('/')
def inicio():
  if not session.get('logged_in'):
    return redirect("/login")
  else:
    return redirect("/inicial")

@app.route('/login', methods=['GET'])
def login():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return redirect("/inicial")

@app.route('/login', methods=['POST'])
def do_admin_login():
  login = request.form

  username = login['email']
  password = login['password']

  usuario = Usuarios.query.filter_by(username=username).first()
  db.session.commit()

  account = False
  print(usuario)
  try:
    if sha256_crypt.verify(password, usuario.password):
        account = True
  except Exception as error:
    return 'Problema: '+ str(error)
    print('Problema: '+ str(error))

  if account:
    session['logged_in'] = True
  else:
    flash('Senha incorreta!')
  return inicio()

@app.route('/criar-usuario', methods=['GET', 'POST'], endpoint='criarusuario')
@login_required
def criarusuario():
    if request.method == 'GET':
        return render_template('criar_usuario.html')

    if request.method == 'POST':
        try:
            username = request.form['email']
            password = password = sha256_crypt.encrypt(request.form['password'])
            email = ""
            if username and password:
                usuario = Usuarios(username, password, email)
                db.session.add(usuario)
                db.session.commit()
            return render_template('criar_usuario.html')
        except Exception as error:
            return 'Problema de inserção no banco de dados: '+ str(error)
            print('Problema de inserção no banco de dados: '+ str(error))

@app.route('/logout', endpoint='logout')
@login_required
def logout():
  session['logged_in'] = False
  return redirect("/login")

@app.route('/contato', methods=['GET', 'POST'], endpoint='')
@login_required
def contato():
    if request.method == 'GET':
        return render_template('contato.html')

    if request.method == 'POST':
        try:
            _name = request.form['user_name']
            _email = request.form['user_email']
            _phone = request.form['user_phone']
            if _name and _email and _phone:
                contact = Contatos(_name, _email, _phone)
                db.session.add(contact)
                db.session.commit()
            return render_template('contato.html')
        except Exception as error:
            print('Problema de inserção no banco de dados: '+ str(error))
        
@app.route('/inicial', methods=['GET'], endpoint='inicial')
@login_required
def inicial():
    return render_template('inicial.html')

#pedido
@app.route('/inicial/pedido', methods=['GET'], endpoint='get_pedido')
@login_required
def get_pedido():
    servicos = Servicos.query.all()
    clientes = Clientes.query.all()
    return render_template('pedido.html', servicos=servicos, clientes=clientes)

@app.route('/inicial/pedido', methods=['POST'], endpoint='post_pedido')
@login_required
def post_pedido():
    cliente = request.form.get('cliente')
    paciente = request.form.get('paciente', '')
    servico_valor = request.form.get('servico')
    if servico_valor != 'Selecione':
        servico = servico_valor.split(';')[0]
        valor = servico_valor.split('; ')[1]
    if cliente:
        pedido = Pedidos(cliente, paciente, servico, valor)
        db.session.add(pedido)
        db.session.commit()
        db.session.flush()
        url = f"/inicial/pedido/{pedido.id}"
        return redirect(url, code=302)
    return render_template('show_pedido.html')

@app.route('/inicial/pedido/<int:nid>', methods=['GET'], endpoint='show_pedido')
@login_required
def show_pedido(nid):
    pedido = Pedidos.query.filter_by(id=nid).all()
    db.session.commit()
    return render_template('show_pedido.html', pedido=pedido)

@app.route('/inicial/pedido/<int:nid>', methods=['POST'], endpoint='finaliza_pedido')
@login_required
def finaliza_pedido(nid):
    db.session.query(Pedidos).filter_by(id=nid).update({
        'status': 1,
        'data_finalizacao': datetime.datetime.now()
    })
    db.session.commit()
    return show_pedido(nid)

@app.route('/inicial/lista/pedidos', methods=['GET'], endpoint='lista_pedido')
@login_required
def lista_pedido():
    data = Pedidos.query.all()
    return render_template('lista_pedidos.html', data=data)

@app.route('/inicial/pedido/<int:nid>/editar', methods=['POST'], endpoint='edita_pedido')
@login_required
def edita_pedido(nid):
    cliente = request.form.get('cliente')
    paciente = request.form.get('paciente', '')
    servico_valor = request.form.get('servico')
    if servico_valor != 'Selecione':
        servico = servico_valor.split(';')[0]
        valor = servico_valor.split('; ')[1]
    db.session.query(Pedidos).filter_by(id=nid).update({
        'clinica': cliente,
        'paciente': paciente,
        'servico': servico,
        'valor': valor
    })
    db.session.commit()
    return show_pedido(nid)

@app.route('/inicial/pedido/<int:nid>/deletar', methods=['POST'], endpoint='deleta_pedido')
@login_required
def deleta_pedido(nid):
    db.session.query(Pedidos).filter_by(id=nid).delete()
    db.session.commit()
    return redirect('/inicial/pedido', code=302)

#cliente
@app.route('/inicial/cliente', methods=['GET'], endpoint='get_cliente')
@login_required
def get_cliente():
    return render_template('cliente.html')

@app.route('/inicial/cliente', methods=['POST'], endpoint='post_cliente')
@login_required
def post_cliente():
    clinica = request.form.get('clinica', '')
    endereco = request.form.get('endereco', '')
    numero = request.form.get('numero', '')
    complemento = request.form.get('complemento', '')
    bairro = request.form.get('bairro', '')
    cidade = request.form.get('cidade', '')
    estado = request.form.get('estado', '')
    telefone = request.form.get('telefone', '')
    if clinica:
        cliente = Clientes(clinica, endereco, numero, complemento, bairro, cidade, estado, telefone)
        db.session.add(cliente)
        db.session.commit()
        db.session.flush()
        url = f"/inicial/cliente/{cliente.id}"
        return redirect(url, code=302)
    return render_template('show_cliente.html')

@app.route('/inicial/cliente/<int:nid>', methods=['GET'], endpoint='show_cliente')
@login_required
def show_cliente(nid):
    cliente = Clientes.query.filter_by(id=nid).all()
    db.session.commit()
    return render_template('show_cliente.html', cliente=cliente)

@app.route('/inicial/lista/cliente', methods=['GET'], endpoint='lista_cliente')
@login_required
def lista_cliente():
    data = Clientes.query.all()
    return render_template('lista_cliente.html', data=data)

@app.route('/inicial/cliente/<int:nid>/editar', methods=['POST'], endpoint='edita_cliente')
@login_required
def edita_cliente(nid):
    clinica = request.form.get('clinica', '')
    endereco = request.form.get('endereco', '')
    numero = request.form.get('numero', '')
    complemento = request.form.get('complemento', '')
    bairro = request.form.get('bairro', '')
    cidade = request.form.get('cidade', '')
    estado = request.form.get('estado', '')
    telefone = request.form.get('telefone', '')
    db.session.query(Clientes).filter_by(id=nid).update({
        'nome_clinica': clinica,
        'endereco': endereco,
        'numero': numero,
        'complemento': complemento,
        'bairro': bairro,
        'cidade': cidade,
        'estado': estado,
        'telefone': telefone
    })
    db.session.commit()
    return show_cliente(nid)

@app.route('/inicial/cliente/<int:nid>/deletar', methods=['POST'], endpoint='deleta_cliente')
@login_required
def deleta_cliente(nid):
    db.session.query(Clientes).filter_by(id=nid).delete()
    db.session.commit()
    return redirect('/inicial/cliente', code=302)

#servico
@app.route('/inicial/servico', methods=['GET'], endpoint='get_servico')
@login_required
def get_servico():
    return render_template('servico.html')

@app.route('/inicial/servico', methods=['POST'], endpoint='post_servico')
@login_required
def post_servico():
    servico = request.form.get('servico', '')
    valor = request.form.get('valor', '')
    if servico:
        servicos = Servicos(servico, valor)
        db.session.add(servicos)
        db.session.commit()
        db.session.flush()
        url = f"/inicial/servico/{servicos.id}"
        return redirect(url, code=302)
    return render_template('show_servico.html')

@app.route('/inicial/servico/<int:nid>', methods=['GET'], endpoint='show_servico')
@login_required
def show_servico(nid):
    servico = Servicos.query.filter_by(id=nid).all()
    db.session.commit()
    return render_template('show_servico.html', servico=servico)

@app.route('/inicial/lista/servico', methods=['GET'], endpoint='lista_servico')
@login_required
def lista_servico():
    data = Servicos.query.all()
    return render_template('lista_servico.html', data=data)

@app.route('/inicial/servico/<int:nid>/editar', methods=['POST'], endpoint='edita_servico')
@login_required
def edita_servico(nid):
    servico = request.form.get('servico', '')
    valor = request.form.get('valor', '')
    db.session.query(Servicos).filter_by(id=nid).update({
        'servico': servico,
        'valor': valor
    })
    db.session.commit()
    return show_servico(nid)

@app.route('/inicial/servico/<int:nid>/deletar', methods=['POST'], endpoint='deleta_servico')
@login_required
def deleta_servico(nid):
    db.session.query(Servicos).filter_by(id=nid).delete()
    db.session.commit()
    return redirect('/inicial/servico', code=302)

#fornecedor
@app.route('/inicial/fornecedor', methods=['GET'], endpoint='get_fornecedor')
@login_required
def get_fornecedor():
    return render_template('fornecedor.html')

@app.route('/inicial/fornecedor', methods=['POST'], endpoint='post_fornecedor')
@login_required
def post_fornecedor():
    fornecedor = request.form.get('fornecedor', '')
    endereco = request.form.get('endereco', '')
    numero = request.form.get('numero', '')
    complemento = request.form.get('complemento', '')
    bairro = request.form.get('bairro', '')
    cidade = request.form.get('cidade', '')
    estado = request.form.get('estado', '')
    telefone = request.form.get('telefone', '')
    if fornecedor:
        forne = Fornecedores(fornecedor, endereco, numero, complemento, bairro, cidade, estado, telefone)
        db.session.add(forne)
        db.session.commit()
        db.session.flush()
        url = f"/inicial/fornecedor/{forne.id}"
        return redirect(url, code=302)
    return render_template('show_fornecedor.html')

@app.route('/inicial/fornecedor/<int:nid>', methods=['GET'], endpoint='show_fornecedor')
@login_required
def show_fornecedor(nid):
    forne = Fornecedores.query.filter_by(id=nid).all()
    db.session.commit()
    return render_template('show_fornecedor.html', forne=forne)

@app.route('/inicial/lista/fornecedor', methods=['GET'], endpoint='lista_forne')
@login_required
def lista_forne():
    data = Fornecedores.query.all()
    return render_template('lista_fornecedor.html', data=data)

@app.route('/inicial/fornecedor/<int:nid>/editar', methods=['POST'], endpoint='edita_fornecedor')
@login_required
def edita_fornecedor(nid):
    fornecedor = request.form.get('fornecedor', '')
    endereco = request.form.get('endereco', '')
    numero = request.form.get('numero', '')
    complemento = request.form.get('complemento', '')
    bairro = request.form.get('bairro', '')
    cidade = request.form.get('cidade', '')
    estado = request.form.get('estado', '')
    telefone = request.form.get('telefone', '')
    db.session.query(Fornecedores).filter_by(id=nid).update({
        'nome_forne': fornecedor,
        'endereco': endereco,
        'numero': numero,
        'complemento': complemento,
        'bairro': bairro,
        'cidade': cidade,
        'estado': estado,
        'telefone': telefone
    })
    db.session.commit()
    return show_fornecedor(nid)

@app.route('/inicial/fornecedor/<int:nid>/deletar', methods=['POST'], endpoint='deleta_fornecedor')
@login_required
def deleta_fornecedor(nid):
    db.session.query(Fornecedores).filter_by(id=nid).delete()
    db.session.commit()
    return redirect('/inicial/fornecedor', code=302)

#lista de compras
@app.route('/inicial/compras', methods=['GET'], endpoint='get_compras')
@login_required
def get_compras():
    fornecedores = Fornecedores.query.all()
    return render_template('compras.html', fornecedores=fornecedores)

@app.route('/inicial/compras', methods=['POST'], endpoint='post_compras')
@login_required
def post_compras():
    fornecedor = request.form.get('fornecedor', '')
    descricao = request.form.get('valor', '')
    if descricao:
        compras = Compras(fornecedor, descricao)
        db.session.add(compras)
        db.session.commit()
        db.session.flush()
        url = f"/inicial/compras/{compras.id}"
        return redirect(url, code=302)
    return render_template('show_compras.html')

@app.route('/inicial/compras/<int:nid>', methods=['GET'], endpoint='show_compras')
@login_required
def show_compras(nid):
    compras = Compras.query.filter_by(id=nid).all()
    db.session.commit()
    return render_template('show_compras.html', compras=compras)

@app.route('/inicial/lista/compras', methods=['GET'], endpoint='lista_compras')
@login_required
def lista_compras():
    data = Compras.query.all()
    return render_template('lista_compras.html', data=data)

@app.route('/inicial/compras/<int:nid>/editar', methods=['POST'], endpoint='edita_compras')
@login_required
def edita_compras(nid):
    fornecedor = request.form.get('fornecedor', '')
    descricao = request.form.get('valor', '')
    db.session.query(Compras).filter_by(id=nid).update({
        'nome_forne': fornecedor,
        'descricao': descricao
    })
    db.session.commit()
    return show_compras(nid)

@app.route('/inicial/compras/<int:nid>/deletar', methods=['POST'], endpoint='deleta_compras')
@login_required
def deleta_compras(nid):
    db.session.query(Compras).filter_by(id=nid).delete()
    db.session.commit()
    return redirect('/inicial/compras', code=302)

#pagamento
@app.route('/inicial/pagamentos', methods=['GET'], endpoint='get_pagamento')
@login_required
def get_pagamento():
    clientes = Clientes.query.all()
    return render_template('pagamentos.html', clientes=clientes)

@app.route('/inicial/pagamentos', methods=['POST'], endpoint='post_pagamento')
@login_required
def post_pagamento():
    cliente = request.form.get('cliente', '')
    valor = request.form.get('valor', '')
    data_string = request.form.get('data', '')
    data_notok = datetime.datetime.strptime(data_string, "%Y-%m-%d").date()
    data = data_notok.strftime('%Y-%m-%d')
    if cliente:
        pagamentos = Pagamentos(cliente, valor, data)
        db.session.add(pagamentos)
        db.session.commit()
        db.session.flush()
        url = f"/inicial/pagamentos/{pagamentos.id}"
        return redirect(url, code=302)
    return render_template('show_pagamentos.html')

@app.route('/inicial/pagamentos/<int:nid>', methods=['GET'], endpoint='show_pagamentos')
@login_required
def show_pagamentos(nid):
    pagamentos = Pagamentos.query.filter_by(id=nid).all()
    db.session.commit()
    return render_template('show_pagamentos.html', pagamentos=pagamentos)

@app.route('/inicial/lista/pagamentos', methods=['GET'], endpoint='lista_pagamentos')
@login_required
def lista_pagamentos():
    data = Pagamentos.query.all()
    return render_template('lista_pagamentos.html', data=data)

#relatório
@app.route('/inicial/relatorios', methods=['GET'], endpoint='get_relatorios')
@login_required
def get_relatorios():
    clinica = Clientes.query.all()
    return render_template('relatorios_inicial.html', clinica=clinica)
    
@app.route('/inicial/relatorios', methods=['POST'], endpoint='post_relatorios')
@login_required
def post_relatorios():
    clinica = request.form.get('clinica', '')
    inicio = request.form.get('inicial', '')
    fim = request.form.get('final', '')
    data = db.session.query(Pedidos).filter(Pedidos.data_finalizacao)
    #sql = 'SELECT id, clinica, paciente, servico, valor FROM pedidos WHERE date_format(data_finalizacao, %s) between "%s" and "%s" AND clinica=%s;'
    
    html = render_template('relatorio_layout.html', data=data)
    pdf = pdfkit.from_string(html, False)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=fechamento.pdf"
    return response
    #return redirect(response, code=302)


if __name__ == "__main__":
    db.create_all()
    port = int(os.environ.get("PORT", 5002))
    app.run(host='0.0.0.0', port=port,debug=True)
#    app.run()
