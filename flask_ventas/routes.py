from flask import render_template, request, redirect, url_for
from flask_ventas import app, mysql

@app.route('/')
def index():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM productos')
    productos = cursor.fetchall()
    cursor.close()
    return render_template('index.html', productos=productos)

@app.route('/agregar_producto', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        stock = request.form['stock']

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s)', (nombre, precio, stock))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('index'))
    
    return render_template('agregar_producto.html')

@app.route('/vender_producto', methods=['GET', 'POST'])
def vender_producto():
    if request.method == 'POST':
        producto_id = request.form['producto_id']
        cantidad = request.form['cantidad']

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT precio, stock FROM productos WHERE id = %s', (producto_id,))
        producto = cursor.fetchone()

        if not producto:
            return "Producto no encontrado", 404

        precio, stock = producto['precio'], producto['stock']
        if stock < int(cantidad):
            return "Stock insuficiente", 400

        total = precio * int(cantidad)
        cursor.execute('INSERT INTO ventas (producto_id, cantidad, total) VALUES (%s, %s, %s)', (producto_id, cantidad, total))
        cursor.execute('UPDATE productos SET stock = stock - %s WHERE id = %s', (cantidad, producto_id))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('index'))

    return render_template('vender_producto.html')
