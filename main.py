from flask import Flask, redirect, render_template, request, url_for, flash
import mysql.connector
from flask_bcrypt import Bcrypt
from sqlalchemy import false
from validate_email import validate_email

app = Flask(__name__)
cnx = mysql.connector.connect(
    host='localhost', user='root', password='', database='php_mysql_crud')
bcrypt = Bcrypt(app)

# SESION
app.secret_key = 'mysecretkey'


@app.route('/')
def index():
    cursor = cnx.cursor()
    cursor.execute('SELECT * FROM task')
    data = cursor.fetchall()

    return render_template('index.html', data=data)


@app.route('/add_task', methods=['POST'])
def add_contact():
    titulo = request.form['title']
    descripcion = request.form['description']
    # id = cursor.lastrowid //ESTO ES PARA COLUMNAS INCREMENTALES COMO EL ID
    cursor = cnx.cursor()
    agregar = ("INSERT INTO task (title, description) VALUES(%s, %s)")
    cursor.execute(agregar, (titulo, descripcion))
    cnx.commit()
    flash('TAREA AGREGADA')
    return redirect(url_for('index'))  # NOMBRE DE LA FUNCION def index()


# decimos que esta al lado de un string llamado id
@app.route('/delete_task/<string:id>')
def delete_contact(id):
    cursor = cnx.cursor()
    eliminar = 'DELETE FROM task WHERE id=%s'
    # (id,) tambien sirve, es un error que no recibe string solo list o tuplas
    cursor.execute(eliminar, [id])
    cnx.commit()
    flash('TAREA ELIMINADA')
    return redirect(url_for('index'))


@app.route('/update_task/<string:id>')
def update_contact(id):
    cursor = cnx.cursor()
    cursor.execute('SELECT * FROM task WHERE id=%s', [id])
    data = cursor.fetchone()
    cnx.commit()
    return render_template('edit.html', data=data)


@app.route('/update/<string:id>', methods=['POST'])
def update(id):
    titulo = request.form['title']
    descripcion = request.form['description']

    cursor = cnx.cursor()
    update = ("UPDATE task SET title=%s, description=%s where id=%s")
    cursor.execute(update, (titulo, descripcion, id))
    cnx.commit()

    flash('TAREA EDITADA')
    return redirect(url_for('index'))

# SIGNUP Y LOGIN


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login_comprobacion', methods=['POST'])
def login_comprobacion():
    email = request.form['email']
    pass1 = request.form['password']

    cursor = cnx.cursor()
    cursor.execute('SELECT * FROM users WHERE email=%s', [email])
    data = cursor.fetchone()        
    cnx.commit()

    if data!=None:
        if bcrypt.check_password_hash(data[2],pass1):
            return redirect(url_for('index'))
        else:
            flash('La contraseña es incorrecta')
    else:
        flash('La cuenta no existe')

    return redirect(url_for('login'))




@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/signup_comprobacion', methods=['POST'])
def signup_comprobacion():
    email = request.form['email']
    pass1 = request.form['password']
    pass2 = request.form['password2']

    errores = validar(email)

    if (pass1 == pass2) and (errores == False):
        cursor = cnx.cursor()
        passFinal = bcrypt.generate_password_hash(pass1)
        insert = "INSERT INTO `users`(email, password) VALUES(%s, %s)"
        cursor.execute(insert, (email, passFinal))
        cnx.commit()
        flash('USUARIO CREADO')
    
    elif (pass1!=pass2):
        flash('Las constraseñas son diferentes')

    return redirect(url_for('signup'))


def validar(e):
    errores = False

    if validate_email(e) == False:
        errores = True
        flash('Ingrese un correo valido')

    cursor = cnx.cursor()
    cursor.execute('SELECT * FROM users WHERE email=%s', [e])
    data = cursor.fetchone()
    cnx.commit()

    if data!=None:
        errores = True
        flash('La cuenta ya existe')

    return errores

if __name__ == '__main__':
    app.run(port=3000, debug=True)
