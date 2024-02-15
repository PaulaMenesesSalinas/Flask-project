import sqlite3

db_locale = 'inventoryManagement.db'

connie = sqlite3.connect(db_locale)
c = connie.cursor()

c.execute("""
CREATE TABLE products 
(id INTEGER PRIMARY KEY,
name TEXT NOT NULL,
quantity INTEGER NOT NULL,
price REAL NOT NULL,
last_modified TEXT
)
""")

connie.commit()
connie.close()