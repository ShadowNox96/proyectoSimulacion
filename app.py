from flask import Flask, redirect, render_template, url_for, request, flash
from flaskext.mysql import MySQL
import functions as fn
import random
from math import factorial, e

app = Flask(__name__)
app.secret_key = 'Mysecret'

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'master'
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
    return render_template('productos.html', data=data)


@app.route('/addProduct')
def nProduct():
    return render_template('nProducto.html')


@app.route('/nProduct', methods=['POST'])
def addProduct():
    if request.method == 'POST':
        nameProduct = request.form['name']
        price = float(request.form['price'])

    cursor = mysql.get_db().cursor()
    cursor.execute(
        'INSERT INTO producto (nomProducto,precio) VALUES(%s, %s)', (nameProduct, price))
    cursor.connection.commit()
    return redirect(url_for('listProducts'))


@app.route('/editProduct/<id>')
def editProduct(id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM producto where idProducto = %s', [id])
    data = cursor.fetchall()
    print(data)
    return render_template('editProduct.html', data=data[0])


@app.route('/saveEditProduct/<id>', methods=['POST'])
def saveProduct(id):
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']

    cursor = mysql.get_db().cursor()
    cursor.execute(
        'UPDATE producto SET nomProducto = %s, precio=%s WHERE idProducto = %s', (name, price, id))
    cursor.connection.commit()
    return redirect(url_for('listProducts'))


@app.route('/deleteProduct/<id>')
def deleteProduct(id):
    cursor = mysql.get_db().cursor()
    cursor.execute('DELETE FROM producto WHERE idProducto= %s', (id))
    cursor.connection.commit()
    return redirect(url_for('listProducts'))


@app.route('/simulation')
def simulation():
    return render_template('simulacion.html')

# Controladores para costos
@app.route('/costs')
def listCosts():
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM costo')
    data = cursor.fetchall()
    return render_template('costs.html', data=data)


@app.route('/addCost')
def nCost():
    return render_template('nCost.html')


@app.route('/nCost', methods=['POST'])
def addCost():
    x = 0
    if request.method == 'POST':
        desCost = request.form['des']
        price = float(request.form['price'])

        tipo = str(request.form.get('tipo'))
        print(tipo)
        if tipo == 'Fijo':
            x = 1
        else:
            x = 0

    cursor = mysql.get_db().cursor()
    cursor.execute(
        'INSERT INTO costo (descripcion,precio,esfijo) VALUES(%s, %s,%s)', (desCost, price, x))
    cursor.connection.commit()
    return redirect(url_for('listCosts'))


@app.route('/simulate', methods=['POST'])
def startSimulate():
    cursor = mysql.get_db().cursor()
    if request.method == 'POST':
        name = request.form['name']
        # promedio de llegadas
        PLl = int(request.form['PLl'])
        # promedio de servicio
        PS = float(request.form['PS'])
        # Numero de servidores
        NS = int(request.form['NS'])
        # Horas a simular
        HS = int(request.form['HS'])
        # Productos por personas
        PP = int(request.form['PP'])
        if PS < PLl:
            flash('El ritmo de servicio es menor a la tasa de llegada, su sistema se esta convirtiendo en infinito, NO SE PUEDE SIMULAR!')
            return render_template('resultSimulate.html')
        else:
            # Ingreso la nueva smulacion
            cursor.execute('INSERT into simulation(name) values(%s)', (name))
            cursor.connection.commit()

            # Extraigo el id de la simulacion que se acaba de ingresar
            cursor.execute(
                'SELECT idSimulation from simulation where name=%s', (name))
            idSimulation = cursor.fetchall()

            # extraigo todos los costos de la bd
            cursor.execute('SELECT SUM(precio) from costo')
            totalCost = cursor.fetchall()

            totalCost = totalCost[0][0]/30
            totalCost = round((totalCost/8), 2)
            # Extraigo todos los productos
            queryProducts = 'SELECT  precio,nomProducto FROM producto'
            cursor.execute(queryProducts)
            data = cursor.fetchall()

            # Empiezo a generar los escenarios
            rangeHours = range(HS)
            for i in rangeHours:
                # numero de personas en este escenario
                x = random.randint(1, PLl-1)
                # la media = PLLl
                probability = round(((PLl**x)/(factorial(x) * (e**PLl))), 10)
                result, totalSale = fn.generateRandoms(x, PP, data)

                utility = totalSale - totalCost
                lq, wq, ls, ws, tllegada, tservicio = fn.colasdeEspera(x, PS)
                # Ingreso el stage
                cursor.execute('INSERT INTO stage(media,probability,persons,costHour,utilityHour,idSimulation,totalHour,ritmoServicio,tpServicio,tpLlegada,nClienteCola,tCola,nClienteSistema,tSistema) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                            (PLl, probability, x, totalCost, utility, idSimulation[0], totalSale, PS, tservicio, tllegada, lq, wq, ls, ws))
                cursor.connection.commit()
                # Extraigo el ultimo stage
                cursor.execute(
                    'SELECT idStage from stage order by(idStage) desc limit 1;')
                idStage = cursor.fetchall()
                idStage = idStage[0]

                # for para meter los resultados del detalle a la tabla
                for x in range(0, len(result), 1):
                    persons = int(result[x][0])
                    costs = float(result[x][2])
                    prods = str(result[x][1])
                    cursor.execute('INSERT INTO detail(hour,personNumber,cost, products,idStage) VALUES(%s,%s,%s,%s,%s)', (
                        i+1, persons, costs, prods, idStage))
                    cursor.connection.commit()
                # extraigo todos los stage para mostrarlos
                cursor.execute(
                    'SELECT * FROM stage where idSimulation =%s', (idSimulation))
                ndata = cursor.fetchall()
                # Variables para asignarle los datos de la grafica
                graphics = []
                count = 1
                # Recorro los datos y solo saco la hora, probabilidad y demas
                for x in ndata:
                    graphics.append([count,float(x[2]),float(x[5]),int(x[3])])
                    count +=1
            return render_template('resultSimulate.html', len=len(ndata), data=ndata, graphics= graphics)


@app.route('/getCost/<id>')
def getCost(id):
    x = ''
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM costo where idCosto = %s', [id])
    data = cursor.fetchall()
    print(data[0][3])
    if data[0][3] == 1:
        x = 'Fijo'
    else:
        x = 'Variable'
    return render_template('editCost.html', data=data[0], x=x)


@app.route('/editCost/<id>', methods=['POST'])
def editCost(id):
    x = 0
    if request.method == 'POST':
        des = request.form['des']
        price = request.form['price']
        tipo = request.form['tipo']

        if tipo == 'Fijo':
            x = 1
        else:
            x = 0

    cursor = mysql.get_db().cursor()
    cursor.execute(
        'UPDATE costo SET descripcion = %s, precio=%s, esFijo=%s WHERE idCosto = %s', (des, price, x, id))
    cursor.connection.commit()
    return redirect(url_for('listCosts'))


@app.route('/deleteCost/<id>')
def deleteCost(id):
    cursor = mysql.get_db().cursor()
    cursor.execute('DELETE FROM costo WHERE idCosto= %s', (id))
    cursor.connection.commit()
    return redirect(url_for('listCosts'))

# Administracion de las simulaciones
@app.route('/admSimulation')
def listSimulation():
    data = []
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM simulation order by idSimulation desc')
    data = cursor.fetchall()
    return render_template('admSimulation.html', data=data)


@app.route('/getSimulation/<id>')
def getViewSimulation(id):
    graphics = []
    count = 1
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM stage where idSimulation = %s', [id])
    data = cursor.fetchall()
    for x in data:
        graphics.append([count,float(x[2]),float(x[5]),int(x[3])])
        count +=1

    print(graphics)
    # return render_template('viewSimulation.html', data= data)
    return render_template('viewSimulation.html', len=len(data), data=data, graphics= graphics)


@app.route('/getSDetail/<id>')
def getViewDetail(id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM detail where idStage = %s', [id])
    data = cursor.fetchall()
    return render_template('viewDetail.html', data=data)


# Verifico si la que se ejecuta es la clase principal y la corro en modo debug
if __name__ == '__main__':
    app.run(debug=True)
