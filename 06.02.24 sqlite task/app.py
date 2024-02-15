from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Function to add a product to the inventory
def add_product(name, quantity, price):
    conn = sqlite3.connect('inventoryManagement.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)", (name, quantity, price))
    conn.commit()
    conn.close()

# Function to get all products from the inventory
def get_products():
    conn = sqlite3.connect('inventoryManagement.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    rows = cur.fetchall()
    conn.close()
    return rows

def update_product(conn, product_id, name, quantity, price):
    cur = conn.cursor()
    cur.execute('''
        UPDATE products SET name=?, quantity=?, price=? WHERE id=?
    ''', (name, quantity, price, product_id))
    conn.commit()

@app.route('/')
def index():
    products = get_products()
    return render_template('index.html', products=products)

@app.route('/add_product', methods=['POST'])
def add_product_route():
    name = request.form['name']
    quantity = request.form['quantity']
    price = request.form['price']
    add_product(name, quantity, price)
    return redirect(url_for('index'))

@app.route('/update_product/<int:product_id>', methods=['GET', 'POST'])
def update_product_route(product_id):
    conn = sqlite3.connect('inventoryManagement.db')
    if request.method == 'GET':
        # Aquí obtienes los detalles del producto para mostrar en el formulario
        cur = conn.cursor()
        cur.execute("SELECT name, quantity, price FROM products WHERE id=?", (product_id,))
        product_details = cur.fetchone()
        conn.close()
        if product_details:
            return render_template('update_product.html', product_id=product_id, product_details=product_details)
        else:
            return "Producto no encontrado"
    elif request.method == 'POST':
        # Aquí obtienes los datos actualizados del formulario y llamas a la función update_product
        name = request.form['name']
        quantity = request.form['quantity']
        price = request.form['price']
        update_product(conn, product_id, name, quantity, price)
        conn.close()
        return redirect(url_for('index'))

@app.route('/delete_product/<int:product_id>')
def delete_product_route(product_id):
    conn = sqlite3.connect('inventoryManagement.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE id=?", (product_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)

