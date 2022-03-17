import os
from flask import Flask, render_template, request
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
def inicial():
    return render_template('login.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/contato', methods=['GET', 'POST'])
def contato():
    try:
        if request.method == 'POST':
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
    finally:
        return render_template('contato.html')

@app.route('/inicial', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def inicial2():
    return render_template('inicial.html')

@app.route('/pedido', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def pedido():
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute('SELECT servico, valor FROM servicos')
    servicos = cursor.fetchall()
    cursor.execute('SELECT nome_clinica FROM clientes')
    clientes = cursor.fetchall()

    if request.method == 'POST':
        cliente = request.form.get('cliente')
        paciente = request.form.get('paciente', '')
        servico = request.form.get('servico').split(';')[0]
        valor = request.form.get('servico').split(';')[1]

        if cliente:
            conn = mysql.connect()
            cursor = conn.cursor()
            sql = 'INSERT INTO pedidos (clinica, paciente, servico, valor) VALUES (%s, %s, %s, %s);'
            values = (cliente, paciente, servico, valor)
            cursor.execute(sql, values)
            conn.commit()

    return render_template('pedido.html', servicos=servicos, clientes=clientes)

@app.route('/cliente', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
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

@app.route('/servico', methods=['GET', 'POST', 'PUT', 'DELETE'])
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


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5002))
    app.run(host='0.0.0.0', port=port)