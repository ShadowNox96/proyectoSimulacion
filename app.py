from flask import Flask, redirect, render_template, url_for
from flaskext.mysql import MySQL

app = Flask(__name__)
app.secret_key = 'Mysecret'

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'bdcafeteria'

mysql = MySQL()
mysql.init_app(app)

@app.route('/')
def indexPage():
    return render_template('index.html')

@app.route('/products')
def listProducts():
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM costo')
    data = cursor.fetchall()
    return render_template('productos.html', data = data)

























#Verifico si la que se ejecuta es la clase principal y la corro en modo debug
if __name__ == '__main__':
    app.run(debug=True)
