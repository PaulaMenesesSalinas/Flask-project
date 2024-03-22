from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Function to add a product to the inventory
def add_product(name, quantity, price):
    conn = sqlite3.connect('inventoryManagement.db')
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)", (name, quantity, price))
        conn.commit()
    except sqlite3.Error as e:
        print("Error adding product:", e)
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# Function to get all products from the inventory
def get_products():
    conn = sqlite3.connect('inventoryManagement.db')
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM products")
        rows = cur.fetchall()
        return rows
    except sqlite3.Error as e:
        print("Error fetching products:", e)
        return []
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def update_product(product_id, name, quantity, price):
    conn = sqlite3.connect('inventoryManagement.db')
    try:
        cur = conn.cursor()
        cur.execute('''
            UPDATE products SET name=?, quantity=?, price=? WHERE id=?
        ''', (name, quantity, price, product_id))
        conn.commit()
    except sqlite3.Error as e:
        print("Error updating product:", e)
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

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
    if request.method == 'GET':
        conn = sqlite3.connect('inventoryManagement.db')
        try:
            cur = conn.cursor()
            cur.execute("SELECT name, quantity, price FROM products WHERE id=?", (product_id,))
            product_details = cur.fetchone()
            if product_details:
                return render_template('update_product.html', product_id=product_id, product_details=product_details)
            else:
                return "Product not found"
        except sqlite3.Error as e:
            print("Error fetching product details:", e)
            return "Error getting product details"
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
    elif request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        price = request.form['price']
        update_product(product_id, name, quantity, price)
        return redirect(url_for('index'))

@app.route('/delete_product/<int:product_id>')
def delete_product_route(product_id):
    conn = sqlite3.connect('inventoryManagement.db')
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM products WHERE id=?", (product_id,))
        conn.commit()
        return redirect(url_for('index'))
    except sqlite3.Error as e:
        print("Error deleting product:", e)
        return "Error deleting product"
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)


