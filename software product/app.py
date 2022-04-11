import os
import pdfkit
from flask import Flask, render_template, request, redirect, make_response
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

# configuracoes MySQL
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '475869'
app.config['MYSQL_DATABASE_DB'] = 'testes'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/')
def inicio():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/contato', methods=['GET', 'POST'])
def contato():
        if request.method == 'POST':
            try:
                _name = request.form['user_name']
                _email = request.form['user_email']
                _phone = request.form['user_phone']
                if _name and _email and _phone:
                    conn = mysql.connect()
                    cursor = conn.cursor()
                    sql = 'INSERT INTO contatos (name, email, phone) VALUES (%s, %s, %s);'
                    values = (_name, _email, _phone)
                    cursor.execute(sql, values)
                    conn.commit()
            except Exception as error:
                print('Problema de inserção no banco de dados: '+ str(error))
        return render_template('contato.html')

@app.route('/inicial', methods=['GET'])
def inicial():
    return render_template('inicial.html')

#pedido
@app.route('/inicial/pedido', methods=['GET'])
def get_pedido():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT servico, valor FROM servicos')
    servicos = cursor.fetchall()
    cursor.execute('SELECT nome_clinica FROM clientes')
    clientes = cursor.fetchall()
    return render_template('pedido.html', servicos=servicos, clientes=clientes)

@app.route('/inicial/pedido', methods=['POST'])
def post_pedido():
    cliente = request.form.get('cliente')
    paciente = request.form.get('paciente', '')
    servico_valor = request.form.get('servico')
    servico = ''
    valor = '0.0'
    if servico_valor != 'Selecione':
        servico = servico_valor.split(';')[0]
        valor = servico_valor.split(';')[1]
    if cliente:
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = 'INSERT INTO pedidos (clinica, paciente, servico, valor, status) VALUES (%s, %s, %s, %s, 0);'
        values = (cliente, paciente, servico, valor)
        cursor.execute(sql, values)
        conn.commit()
        cursor.execute('SELECT LAST_INSERT_ID();')
        pedido = cursor.fetchone()
        for nid in pedido:
            url = f"/inicial/pedido/{nid}"
            return redirect(url, code=302)
    return render_template('show_pedido.html')

@app.route('/inicial/pedido/<int:nid>', methods=['GET'])
def show_pedido(nid):
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = 'SELECT id, clinica, paciente, servico, valor FROM pedidos WHERE id = %s'
    value = (nid)
    cursor.execute(sql, value)
    pedido = cursor.fetchall()
    return render_template('show_pedido.html', pedido=pedido)

@app.route('/inicial/pedido/<int:nid>', methods=['POST'])
def finaliza_pedido(nid):
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = 'UPDATE pedidos SET status = 1 WHERE id = %s'
    value = (nid)
    cursor.execute(sql, value)
    sql = 'UPDATE pedidos SET data_finalizacao = CURDATE() WHERE id = %s'
    cursor.execute(sql, value)
    conn.commit()
    return show_pedido(nid)

@app.route('/inicial/lista/pedidos', methods=['GET'])
def lista_pedido():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT id, clinica, data_criacao, valor FROM pedidos')
    data = cursor.fetchall()
    return render_template('lista_pedidos.html', data=data)

#cliente
@app.route('/inicial/cliente', methods=['GET'])
def get_cliente():
    return render_template('cliente.html')

@app.route('/inicial/cliente', methods=['POST'])
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
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = 'INSERT INTO clientes (nome_clinica, endereco, numero, complemento, bairro, cidade, estado, telefone) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);'
        values = (clinica, endereco, numero, complemento, bairro, cidade, estado, telefone)
        cursor.execute(sql, values)
        conn.commit()
        cursor.execute('SELECT LAST_INSERT_ID();')
        cliente = cursor.fetchone()
        for nid in cliente:
            url = f"/inicial/cliente/{nid}"
            return redirect(url, code=302)
    return render_template('show_cliente.html')

@app.route('/inicial/cliente/<int:nid>', methods=['GET'])
def show_cliente(nid):
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = 'SELECT id, nome_clinica, endereco, numero, complemento, bairro, cidade, estado, telefone FROM clientes WHERE id = %s'
    value = (nid)
    cursor.execute(sql, value)
    cliente = cursor.fetchall()
    return render_template('show_cliente.html', cliente=cliente)

@app.route('/inicial/lista/cliente', methods=['GET'])
def lista_cliente():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome_clinica, endereco, telefone FROM clientes')
    data = cursor.fetchall()
    return render_template('lista_cliente.html', data=data)

#servico
@app.route('/inicial/servico', methods=['GET'])
def get_servico():
    return render_template('servico.html')

@app.route('/inicial/servico', methods=['POST'])
def post_servico():
    servico = request.form.get('servico', '')
    valor = request.form.get('valor', '')
    if servico:
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = 'INSERT INTO servicos (servico, valor) VALUES (%s, %s);'
        values = (servico, valor)
        cursor.execute(sql, values)
        conn.commit()
        cursor.execute('SELECT LAST_INSERT_ID();')
        servico = cursor.fetchone()
        for nid in servico:
            url = f"/inicial/servico/{nid}"
            return redirect(url, code=302)
    return render_template('show_servico.html')

@app.route('/inicial/servico/<int:nid>', methods=['GET'])
def show_servico(nid):
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = 'SELECT id, servico, valor FROM servicos WHERE id = %s'
    value = (nid)
    cursor.execute(sql, value)
    servico = cursor.fetchall()
    return render_template('show_servico.html', servico=servico)

@app.route('/inicial/lista/servico', methods=['GET'])
def lista_servico():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT id, servico, valor FROM servicos')
    data = cursor.fetchall()
    return render_template('lista_servico.html', data=data)

#fornecedor
@app.route('/inicial/fornecedor', methods=['GET'])
def get_fornecedor():
    return render_template('fornecedor.html')

@app.route('/inicial/fornecedor', methods=['POST'])
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
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = 'INSERT INTO fornecedores (nome_forne, endereco, numero, complemento, bairro, cidade, estado, telefone) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);'
        values = (fornecedor, endereco, numero, complemento, bairro, cidade, estado, telefone)
        cursor.execute(sql, values)
        conn.commit()
        cursor.execute('SELECT LAST_INSERT_ID();')
        forne = cursor.fetchone()
        for nid in forne:
            url = f"/inicial/fornecedor/{nid}"
            return redirect(url, code=302)
    return render_template('show_fornecedor.html')

@app.route('/inicial/fornecedor/<int:nid>', methods=['GET'])
def show_fornecedor(nid):
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = 'SELECT id, nome_forne, endereco, numero, complemento, bairro, cidade, estado, telefone FROM fornecedores WHERE id = %s'
    value = (nid)
    cursor.execute(sql, value)
    forne = cursor.fetchall()
    return render_template('show_fornecedor.html', forne=forne)

@app.route('/inicial/lista/fornecedor', methods=['GET'])
def lista_forne():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome_forne, endereco, telefone FROM fornecedores')
    data = cursor.fetchall()
    return render_template('lista_fornecedor.html', data=data)

#lista de compras
@app.route('/inicial/compras', methods=['GET'])
def get_compras():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT nome_forne FROM fornecedores')
    fornecedores = cursor.fetchall()
    return render_template('compras.html', fornecedores=fornecedores)

@app.route('/inicial/compras', methods=['POST'])
def post_compras():
    fornecedor = request.form.get('fornecedor', '')
    descricao = request.form.get('valor', '')
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = 'INSERT INTO compras (nome_forne, descricao) VALUES (%s, %s);'
    values = (fornecedor, descricao)
    cursor.execute(sql, values)
    conn.commit()
    cursor.execute('SELECT LAST_INSERT_ID();')
    compras = cursor.fetchone()
    for nid in compras:
        url = f"/inicial/compras/{nid}"
        return redirect(url, code=302)
    return render_template('show_compras.html')

@app.route('/inicial/compras/<int:nid>', methods=['GET'])
def show_compras(nid):
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = 'SELECT id, nome_forne, descricao FROM compras WHERE id = %s'
    value = (nid)
    cursor.execute(sql, value)
    compras = cursor.fetchall()
    return render_template('show_compras.html', compras=compras)

@app.route('/inicial/lista/compras', methods=['GET'])
def lista_compras():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT id, data_criacao, nome_forne FROM compras')
    data = cursor.fetchall()
    return render_template('lista_compras.html', data=data)

#relatório
@app.route('/inicial/relatorios', methods=['GET'])
def get_relatorios():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT nome_clinica FROM clientes')
    clinica = cursor.fetchall()
    return render_template('relatorios_inicial.html', clinica=clinica)
    
@app.route('/inicial/relatorios', methods=['POST'])
def post_relatorios():
    clinica = request.form.get('clinica', '')
    inicio = request.form.get('inicial', '')
    fim = request.form.get('final', '')
    conn = mysql.connect()
    cursor = conn.cursor()
    formato = "'%m/%d/%Y'"
    sql = 'SELECT id, clinica, paciente, servico, valor FROM pedidos WHERE date_format(data_finalizacao, %s) between "%s" and "%s" AND clinica=%s;'
    values = (formato, inicio, fim, clinica)
    cursor.execute(sql, values)
    data = cursor.fetchall()
    html = render_template('relatorio_layout.html', data=data)
    pdf = pdfkit.from_string(html, False)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=fechamento.pdf"
    return response


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5002))
    app.run(host='0.0.0.0', port=port)
