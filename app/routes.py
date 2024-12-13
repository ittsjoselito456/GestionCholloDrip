from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from .db import get_connection
from mysql.connector import Error

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/clientes', methods=['GET', 'POST'])
def add_cliente():
    if request.method == 'POST':
        data = request.form
        connection = get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = "INSERT INTO Clientes (nombre, telefono, direccion, ciudad, provincia, pais) VALUES (%s, %s, %s, %s, %s, %s)"
                values = (data['nombre'], data['telefono'], data['direccion'], data['ciudad'], data['provincia'], data['pais'])
                cursor.execute(query, values)
                connection.commit()
                flash('Cliente agregado exitosamente', 'success')
                return redirect(url_for('main.list_clientes'))
            except Error as e:
                flash(f'Error: {str(e)}', 'danger')
            finally:
                cursor.close()
                connection.close()
    return render_template('add_cliente.html')

@main.route('/productos', methods=['GET', 'POST'])
def add_producto():
    if request.method == 'POST':
        data = request.form
        connection = get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = "INSERT INTO Productos (nombre, precio_cliente, precio_tienda, telefono_proveedor) VALUES (%s, %s, %s, %s)"
                values = (data['nombre'], data['precio_cliente'], data['precio_tienda'], data['telefono_proveedor'])
                cursor.execute(query, values)
                connection.commit()
                flash('Producto agregado exitosamente', 'success')
                return redirect(url_for('main.list_productos'))
            except Error as e:
                flash(f'Error: {str(e)}', 'danger')
            finally:
                cursor.close()
                connection.close()
    return render_template('add_producto.html')


@main.route('/pedidos', methods=['GET', 'POST'])
def add_pedido():
    if request.method == 'POST':
        data = request.form
        connection = get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = "INSERT INTO Pedidos (id_cliente, id_producto, cantidad, entregado) VALUES (%s, %s, %s, %s)"
                values = (data['id_cliente'], data['id_producto'], data['cantidad'], 'entregado' in data)
                cursor.execute(query, values)
                connection.commit()
                flash('Pedido agregado exitosamente', 'success')
                return redirect(url_for('main.list_pedidos'))
            except Error as e:
                flash(f'Error: {str(e)}', 'danger')
            finally:
                cursor.close()
                connection.close()
    return render_template('add_pedido.html')



@main.route('/clientes/list', methods=['GET', 'POST'])
def list_clientes():
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM Clientes"
            if request.method == 'POST':
                filtro = request.form.get('filtro')
                if filtro:
                    query += f" WHERE nombre LIKE %s OR telefono LIKE %s OR direccion LIKE %s OR ciudad LIKE %s OR provincia LIKE %s OR pais LIKE %s"
                    values = (f'%{filtro}%', f'%{filtro}%', f'%{filtro}%', f'%{filtro}%', f'%{filtro}%', f'%{filtro}%')
                    cursor.execute(query, values)
                else:
                    cursor.execute(query)
            else:
                cursor.execute(query)
            clientes = cursor.fetchall()
            return render_template('list_clientes.html', clientes=clientes)
        except Error as e:
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            connection.close()
    return render_template('list_clientes.html', clientes=[])

@main.route('/productos/list', methods=['GET', 'POST'])
def list_productos():
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM Productos"
            if request.method == 'POST':
                filtro = request.form.get('filtro')
                if filtro:
                    query += f" WHERE nombre LIKE %s OR precio_cliente LIKE %s OR precio_tienda LIKE %s OR telefono_proveedor LIKE %s"
                    values = (f'%{filtro}%', f'%{filtro}%', f'%{filtro}%', f'%{filtro}%')
                    cursor.execute(query, values)
                else:
                    cursor.execute(query)
            else:
                cursor.execute(query)
            productos = cursor.fetchall()
            return render_template('list_productos.html', productos=productos)
        except Error as e:
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            connection.close()
    return render_template('list_productos.html', productos=[])


@main.route('/pedidos/update_entregado/<int:id>', methods=['POST'])
def update_entregado(id):
    data = request.get_json()
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "UPDATE Pedidos SET entregado = %s WHERE id_pedido = %s"
            values = (data['entregado'], id)
            cursor.execute(query, values)
            connection.commit()
            return jsonify({'success': True})
        except Error as e:
            return jsonify({'success': False, 'error': str(e)}), 500
        finally:
            cursor.close()
            connection.close()
    return jsonify({'success': False, 'error': 'No se pudo conectar a la base de datos'}), 500



@main.route('/pedidos/list', methods=['GET', 'POST'])
def list_pedidos():
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM Pedidos"
            if request.method == 'POST':
                filtro_cliente = request.form.get('filtro_cliente')
                filtro_entregado = request.form.get('filtro_entregado')
                if filtro_cliente:
                    query += f" WHERE id_cliente LIKE %s"
                    values = (f'%{filtro_cliente}%',)
                    if filtro_entregado:
                        query += f" AND entregado = %s"
                        values += (filtro_entregado.lower() == 'true',)
                elif filtro_entregado:
                    query += f" WHERE entregado = %s"
                    values = (filtro_entregado.lower() == 'true',)
                else:
                    values = ()
                cursor.execute(query, values)
            else:
                cursor.execute(query)
            pedidos = cursor.fetchall()
            return render_template('list_pedidos.html', pedidos=pedidos)
        except Error as e:
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            connection.close()
    return render_template('list_pedidos.html', pedidos=[])


@main.route('/clientes/delete/<int:id>', methods=['POST'])
def delete_cliente(id):
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "DELETE FROM Clientes WHERE id_cliente=%s"
            values = (id,)
            cursor.execute(query, values)
            connection.commit()
            flash('Cliente eliminado exitosamente', 'success')
        except Error as e:
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            connection.close()
    return redirect(url_for('main.list_clientes'))



@main.route('/clientes/search', methods=['GET'])
def search_clientes():
    query = request.args.get('query', '')
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            if query:
                query_sql = "SELECT id_cliente, nombre FROM Clientes WHERE nombre LIKE %s"
                values = (f'%{query}%',)
            else:
                query_sql = "SELECT id_cliente, nombre FROM Clientes"
                values = ()
            cursor.execute(query_sql, values)
            clientes = cursor.fetchall()
            return jsonify(clientes)
        except Error as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            connection.close()
    return jsonify([])

@main.route('/productos/search', methods=['GET'])
def search_productos():
    query = request.args.get('query', '')
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            if query:
                query_sql = "SELECT id_producto, nombre FROM Productos WHERE nombre LIKE %s"
                values = (f'%{query}%',)
            else:
                query_sql = "SELECT id_producto, nombre FROM Productos"
                values = ()
            cursor.execute(query_sql, values)
            productos = cursor.fetchall()
            return jsonify(productos)
        except Error as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            connection.close()
    return jsonify([])




@main.route('/productos/delete/<int:id>', methods=['POST'])
def delete_producto(id):
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "DELETE FROM Productos WHERE id_producto=%s"
            values = (id,)
            cursor.execute(query, values)
            connection.commit()
            flash('Producto eliminado exitosamente', 'success')
        except Error as e:
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            connection.close()
    return redirect(url_for('main.list_productos'))

@main.route('/pedidos/delete/<int:id>', methods=['POST'])
def delete_pedido(id):
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "DELETE FROM Pedidos WHERE id_pedido=%s"
            values = (id,)
            cursor.execute(query, values)
            connection.commit()
            flash('Pedido eliminado exitosamente', 'success')
        except Error as e:
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            connection.close()
    return redirect(url_for('main.list_pedidos'))

@main.route('/clientes/edit/<int:id>', methods=['GET', 'POST'])
def edit_cliente(id):
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            if request.method == 'POST':
                data = request.form
                query = "UPDATE Clientes SET nombre=%s, telefono=%s, direccion=%s, ciudad=%s, provincia=%s, pais=%s WHERE id_cliente=%s"
                values = (data['nombre'], data['telefono'], data['direccion'], data['ciudad'], data['provincia'], data['pais'], id)
                cursor.execute(query, values)
                connection.commit()
                flash('Cliente modificado exitosamente', 'success')
                return redirect(url_for('main.list_clientes'))
            else:
                query = "SELECT * FROM Clientes WHERE id_cliente=%s"
                values = (id,)
                cursor.execute(query, values)
                cliente = cursor.fetchone()
                return render_template('edit_cliente.html', cliente=cliente)
        except Error as e:
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            connection.close()
    return render_template('edit_cliente.html', cliente=None)

@main.route('/productos/edit/<int:id>', methods=['GET', 'POST'])
def edit_producto(id):
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            if request.method == 'POST':
                data = request.form
                query = "UPDATE Productos SET nombre=%s, precio_cliente=%s, precio_tienda=%s, telefono_proveedor=%s WHERE id_producto=%s"
                values = (data['nombre'], data['precio_cliente'], data['precio_tienda'], data['telefono_proveedor'], id)
                cursor.execute(query, values)
                connection.commit()
                flash('Producto modificado exitosamente', 'success')
                return redirect(url_for('main.list_productos'))
            else:
                query = "SELECT * FROM Productos WHERE id_producto=%s"
                values = (id,)
                cursor.execute(query, values)
                producto = cursor.fetchone()
                return render_template('edit_producto.html', producto=producto)
        except Error as e:
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            connection.close()
    return render_template('edit_producto.html', producto=None)
