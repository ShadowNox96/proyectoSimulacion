from flask import Flask, redirect, render_template, url_for, request
from flaskext.mysql import MySQL
import functions as fn

app = Flask(__name__)
app.secret_key = 'Mysecret'

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Admin1234'
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

#Controladores para costos
@app.route('/costs')
def listCosts():
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM costo')
    data = cursor.fetchall()
    return render_template('costs.html', data = data)

@app.route('/addCost')
def nCost():
    return render_template('nCost.html')

@app.route('/nCost', methods =['POST'])
def addCost():
    x=0
    if request.method == 'POST':
        desCost = request.form['des']
        price = float(request.form['price'])
        
        tipo = str(request.form.get('tipo'))
        print(tipo)
        if tipo=='Fijo':
            x=1
        else:
            x=0
        
    
    cursor = mysql.get_db().cursor()
    cursor.execute('INSERT INTO costo (descripcion,precio,esfijo) VALUES(%s, %s,%s)', (desCost, price, x))
    cursor.connection.commit()
    return redirect(url_for('listCosts'))
@app.route('/simulate', methods = ['POST'])
def startSimulate():
    if request.method == 'POST':
        #promedio de llegadas
        PLl = int(request.form['PLl'])
        #promedio de servicio
        PS = int(request.form['PS'])
        #Numero de servidores
        NS = int(request.form['NS'])
        #Horas a simular
        HS = int(request.form['HS'])
        #Productos por personas
        PP = int(request.form['PP'])

        cursor = mysql.get_db().cursor()
        query = 'SELECT nomProducto FROM producto'
        cursor.execute(query)
        data = cursor.fetchall()
        result = fn.generateRandoms(PLl, PP, HS, data)
    print(result)
    return render_template('resultSimulate.html', data = result)


@app.route('/getCost/<id>')
def getCost(id):
    x=''
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM costo where idCosto = %s', [id])
    data = cursor.fetchall()
    print(data[0][3])
    if data[0][3]==1: 
        x='Fijo'
    else:
        x='Variable'
    return render_template('editCost.html', data= data[0],x=x)

@app.route('/editCost/<id>', methods=['POST'])
def editCost(id):
    x=0
    if request.method == 'POST':
        des = request.form['des']
        price = request.form['price']
        tipo= request.form['tipo']
    
        if tipo=='Fijo':
            x=1
        else:
            x=0

    cursor = mysql.get_db().cursor()
    cursor.execute('UPDATE costo SET descripcion = %s, precio=%s, esFijo=%s WHERE idCosto = %s',(des,price,x,id))
    cursor.connection.commit()
    return redirect(url_for('listCosts'))

@app.route('/deleteCost/<id>')
def deleteCost(id):
    cursor = mysql.get_db().cursor()
    cursor.execute('DELETE FROM costo WHERE idCosto= %s',(id))
    cursor.connection.commit()
    return redirect(url_for('listCosts'))















#Verifico si la que se ejecuta es la clase principal y la corro en modo debug
if __name__ == '__main__':
    app.run(debug=True)
