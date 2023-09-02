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
app.config['MYSQL_DB']='bdturismo'
mysql=MySQL(app)

app.secret_key='mysecretkey'


#Zona de routing
@app.route('/')
def inde():
    cursor=mysql.connection.cursor()
    cursor.execute('select * from tbpueblosmagicos')
    consulta=cursor.fetchall()
    
    return render_template('IndexPue.html', PueblosMagicos=consulta)

@app.route('/insertar', methods=['POST'])
def insert():

        vid=request.form['txtid']
        vestado = request.form['txtestado']
        vpueblo = request.form['txtpueblo']
       
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO tbpueblosmagicos(idPueblo,Estado,Pueblo) VALUES(%s,%s,%s)",(vid,vestado,vpueblo))
        mysql.connection.commit()
        
        flash('Pueblo agregado en la base de datos')
       
        return redirect(url_for('inde'))

#arrancar el servidor
if __name__=='__main__':
    app.run(port=3000,debug=True)