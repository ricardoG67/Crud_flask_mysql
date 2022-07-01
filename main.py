from flask import Flask, redirect, render_template, request, url_for, flash
import mysql.connector

app = Flask(__name__)
cnx = mysql.connector.connect(host='localhost', user='root', password='', database='php_mysql_crud')

#SESION
app.secret_key='mysecretkey'

@app.route('/')
def index():
    cursor = cnx.cursor()
    cursor.execute('SELECT * FROM task')
    data = cursor.fetchall()

    return render_template('index.html', data = data)

@app.route('/add_task', methods=['POST'])
def add_contact():
    titulo = request.form['title']
    descripcion = request.form['description']
    #id = cursor.lastrowid //ESTO ES PARA COLUMNAS INCREMENTALES COMO EL ID
    cursor = cnx.cursor()
    agregar = ("INSERT INTO task (title, description) VALUES(%s, %s)")
    cursor.execute(agregar,(titulo, descripcion))
    cnx.commit()
    flash('TAREA AGREGADA')
    return redirect(url_for('index')) #NOMBRE DE LA FUNCION def index()


@app.route('/delete_task/<string:id>')#decimos que esta al lado de un string llamado id
def delete_contact(id):
    cursor = cnx.cursor()
    eliminar = 'DELETE FROM task WHERE id=%s'
    cursor.execute(eliminar, [id]) #(id,) tambien sirve, es un error que no recibe string solo list o tuplas
    cnx.commit()
    flash('TAREA ELIMINADA')
    return redirect(url_for('index'))

@app.route('/update_task/<string:id>')
def update_contact(id):
    cursor = cnx.cursor()
    cursor.execute('SELECT * FROM task WHERE id=%s', [id])
    data = cursor.fetchone()
    cnx.commit()
    return render_template('edit.html', data = data)

@app.route('/update/<string:id>', methods=['POST'])
def update(id):
    titulo = request.form['title']
    descripcion = request.form['description']

    cursor = cnx.cursor()
    update = ("UPDATE task SET title=%s, description=%s where id=%s")
    cursor.execute(update, (titulo,descripcion,id))
    cnx.commit()

    flash('TAREA EDITADA')
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(port=3000, debug=True)