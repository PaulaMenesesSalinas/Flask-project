import sqlite3

db_locale = 'inventoryManagement.db'

connie = sqlite3.connect(db_locale)
c = connie.cursor()

c.execute("""
SELECT * FROM products
""")
inventory_info = c.fetchall()

for product in inventory_info:
    print(product)
    
connie.commit()
connie.close()