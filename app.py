from flask import Flask, redirect, render_template, url_for, request
from flaskext.mysql import MySQL
import functions as fn
import random
from math import factorial,e

app = Flask(__name__)
app.secret_key = 'Mysecret'

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Admin1234'
app.config['MYSQL_DATABASE_DB'] = 'mydb'

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

@app.route('/costs')
def listCosts():
    return render_template('costs.html')


@app.route('/simulate', methods = ['POST'])
def startSimulate():
    cursor = mysql.get_db().cursor()
    if request.method == 'POST':
        name = request.form['name']
        #promedio de llegadas
        PLl = int(request.form['PLl'])
        #promedio de servicio
        PS = float(request.form['PS'])
        #Numero de servidores
        NS = int(request.form['NS'])
        #Horas a simular
        HS = int(request.form['HS'])
        #Productos por personas
        PP = int(request.form['PP'])
        
        
        #Ingreso la nueva smulacion
        cursor.execute('INSERT into simulation(name) values(%s)', (name))
        cursor.connection.commit()
        
        #Extraigo el id de la simulacion que se acaba de ingresar 
        cursor.execute('SELECT idSimulation from simulation where name=%s', (name))
        idSimulation = cursor.fetchall()

        #extraigo todos los costos de la bd 
        cursor.execute('SELECT SUM(precio) from costo')
        totalCost = cursor.fetchall()
        totalCost = totalCost/30
        totalCost = totalCost/8
        #Extraigo todos los productos
        queryProducts = 'SELECT  precio,nomProducto FROM producto'
        cursor.execute(queryProducts)
        data = cursor.fetchall()

        #Empiezo a generar los escenarios
        rangeHours = range(HS)
        for i in rangeHours:
            #numero de personas en este escenario
            x = random.randint(1,PLl)
            #la media = PLLl
            probability = (PLl**x)/factorial(x) * (e**PLl)
            result, totalSale = fn.generateRandoms(x,PP, data)
            utility = totalSale - totalCost
            #Ingreso el stage
            cursor.execute('INSERT INTO stage(media,probability,persons,costHour,utility,idSimulation,totalHour) VALUES(%s,%s,%s,%s,%s,%s,%s)', x, probability,x,totalCost,utility,idSimulation,totalSale)
            cursor.connection.commit()
            #Extraigo el ultimo stage 
            cursor.execute('SELECT idStage from stage order by(idStage) desc limit 1;') 
            idStage = cursor.fetchall()
            idStage = idStage[0]
            for x in result:
                cursor.execute('INSERT INTO detail(hour,personNumber,cost, products,idStage) VALUES(%s,%s,%s,%s,%s)',i,result[x][0], result[x][2], result[x][1], idStage)
                cursor.connection.commit()
    return render_template('resultSimulate.html')

















#Verifico si la que se ejecuta es la clase principal y la corro en modo debug
if __name__ == '__main__':
    app.run(debug=True)
