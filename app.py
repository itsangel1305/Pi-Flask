from flask import Flask, render_template, request, session, redirect, Response
from flask_mysqldb import MySQL, MySQLdb

app = Flask(__name__, template_folder='templates')


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'login'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.post('/perfil')
def perfil():
    return render_template('PerfilUsu.html')

@app.route('/user')
def admin():
    return render_template('InicioUsuario.html')


@app.route('/acceso-login', methods=["GET", "POST"])
def login():
    if request.method == 'POST' and 'txtCorreo' in request.form and 'txtPassword' in request.form:
        _correo = request.form['txtCorreo']
        _password = request.form['txtPassword']

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE correo = %s AND password = %s', (_correo, _password))
        account = cur.fetchone()
        cur.close()

        if account:
            session['logueado'] = True
            session['Id'] = account['Id']
            session['id_rol'] = account['id_rol']
            
            if session['id_rol'] == 1:
                return render_template("admin2.html")
            elif session['id_rol'] == 2:
                return render_template("InicioUsuario.html")
        else:
            return render_template('index.html', mensaje="Correo o Contaseña incorrecta")
        
@app.route('/registro')
def registro():
    return render_template('registro.html')

#--------------Registros------------------
@app.route('/crear-registro', methods=["GET", "POST"])
def crear_registro():
    
    correo=request.form['txtCorreo']
    password=request.form['txtPassword']
    
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO usuarios (correo, password, id_rol) VALUES (%s, %s, '2')", (correo, password))
    mysql.connection.commit()
    
    return render_template('index.html', mensaje2="Registro exitoso")
#-----------------------------------------

#-------------lista de usuarios------------------

@app.route('/listar', methods=["GET", "POST"])
def listar():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios")
    usuarios = cur.fetchall()
    cur.close()
    return render_template('listar_usuarios.html', usuarios=usuarios)

#-------------------------------


if __name__ == '__main__':
    app.secret_key = "llovascript"
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
    
    

    

