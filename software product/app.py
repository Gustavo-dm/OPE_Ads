import os
import json
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

@app.route('/pedido', methods=['POST'])
def pedido2():
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
            url = f"/pedido/{nid}"
            return redirect(url, code=302)
    return render_template('show_pedido.html')

@app.route('/pedido', methods=['GET'])
def pedido():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT servico, valor FROM servicos')
    servicos = cursor.fetchall()
    cursor.execute('SELECT nome_clinica FROM clientes')
    clientes = cursor.fetchall()
    return render_template('pedido.html', servicos=servicos, clientes=clientes)

@app.route('/pedido/<int:nid>', methods=['GET'])
def show_pedido(nid):
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = 'SELECT id, clinica, paciente, servico, valor FROM pedidos WHERE id = %s'
    value = (nid)
    cursor.execute(sql, value)
    pedido = cursor.fetchall()
    return render_template('show_pedido.html', pedido=pedido)

@app.route('/pedido/<int:nid>', methods=['POST'])
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

@app.route('/lista/pedidos', methods=['GET'])
def listagem():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT id, clinica, data_criacao, valor FROM pedidos')
    data = cursor.fetchall()
    return render_template('lista.html', data=data)

@app.route('/cliente', methods=['GET', 'POST'])
def cliente():
    if request.method == 'POST':
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
    return render_template('cliente.html')

@app.route('/servico', methods=['GET', 'POST'])
def servico():
    if request.method == 'POST':
        servico = request.form.get('servico', '')
        valor = request.form.get('valor', '')

        if servico:
            conn = mysql.connect()
            cursor = conn.cursor()
            sql = 'INSERT INTO servicos (servico, valor) VALUES (%s, %s);'
            values = (servico, valor)
            cursor.execute(sql, values)
            conn.commit()
    return render_template('servico.html')

@app.route('/relatorios', methods=['GET'])
def relatorios():
    name = 'Fechamento'
    html = render_template('relatorios.html', name=name)
    pdf = pdfkit.from_string(html, False)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=fechamento.pdf"
    return response

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5002))
    app.run(host='0.0.0.0', port=port)
