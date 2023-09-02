#importar el framework
from colorama import Cursor
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from email.policy import default
from flask_mysqldb import MySQL



#inicializar variable para usar flask
app= Flask(__name__)

#configuracion de coneccion
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='bdflask'
mysql=MySQL(app)

app.secret_key='mysecretkey'


#Zona de routing
@app.route('/')
def index():
    cursor=mysql.connection.cursor()
    cursor.execute('select * from tb_albums')
    consulta=cursor.fetchall()
    
    return render_template('index.html', Albums=consulta)

@app.route('/agregar', methods=['POST'])
def agregar():

        valbum = request.form['txtalbum']
        vartista = request.form['txtartista']
        vanio = request.form['txtanio']
       
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO tb_albums(Nombre,Artista,Anio) VALUES(%s,%s,%s)",(valbum,vartista,vanio))
        mysql.connection.commit()
        
        flash('Album agregado en la base de datos')
       
        return redirect(url_for('index'))

@app.route('/editar/<string:id>', methods=['POST','GET'])
def get_album(id):
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM tb_albums WHERE id = {0}'.format(id))
    data=cur.fetchall()
    return render_template('Actualizar.html', album = data[0])
    

@app.route('/update/<string:id>', methods=['POST'])
def update_album(id):
    if request.method == 'POST':
        valbum = request.form['txtalbum']
        vartista = request.form['txtartista']
        vanio = request.form['txtanio']
       
        cur=mysql.connection.cursor()
        cur.execute("UPDATE tb_albums SET Nombre=%s, Artista=%s, Anio=%s WHERE id=%s",(valbum,vartista,vanio,id))
        mysql.connection.commit()
        
        flash('Album actualizado')
        
    return redirect(url_for('index'))
    

@app.route('/eliminar/<string:id>')
def eliminar(id):
    
    cur=mysql.connection.cursor()
    cur.execute("DELETE FROM tb_albums WHERE id={0}".format(id))
    mysql.connection.commit()
    
    flash('Album eliminado de la base de datos')
    return redirect(url_for('index'))



#arrancamos servidor
if __name__=='__main__':
    app.run(port=3000,debug=True)
