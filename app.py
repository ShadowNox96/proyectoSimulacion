from flask import Flask, redirect, render_template, url_for, request
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
    cursor.execute('SELECT * FROM producto')
    data = cursor.fetchall()
    return render_template('productos.html', data = data)



@app.route('/addProduct')
def nProduct():
    return render_template('nProducto.html')

@app.route('/nProduct', methods =['POST'])
def addProduct():
    if request.method == 'POST':
        nameProduct = request.form['name']
        price = float(request.form['price']) 
    
    cursor = mysql.get_db().cursor()
    cursor.execute('INSERT INTO producto (nomProducto,precio) VALUES(%s, %s)', (nameProduct, price))
    cursor.connection.commit()
    return redirect(url_for('listProducts'))


@app.route('/editProduct/<id>')
def editProduct(id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM producto where idProducto = %s', [id])
    data = cursor.fetchall()
    print(data)
    return render_template('editProduct.html', data= data[0])

@app.route('/saveEditProduct/<id>', methods=['POST'])
def saveProduct(id):
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
    
    cursor = mysql.get_db().cursor()
    cursor.execute('UPDATE producto SET nomProducto = %s, precio=%s WHERE idProducto = %s',(name,price,id))
    cursor.connection.commit()
    return redirect(url_for('listProducts'))

@app.route('/deleteProduct/<id>')
def deleteProduct(id):
    cursor = mysql.get_db().cursor()
    cursor.execute('DELETE FROM producto WHERE idProducto= %s',(id))
    cursor.connection.commit()
    return redirect(url_for('listProducts'))

@app.route('/simulation')
def simulation():
    return render_template('simulacion.html')

@app.route('/cost')
def listCosts():
    return render_template('costs.html')


















#Verifico si la que se ejecuta es la clase principal y la corro en modo debug
if __name__ == '__main__':
    app.run(debug=True)