import sqlite3

db_locale = 'inventoryManagement.db'

connie = sqlite3.connect(db_locale)
c = connie.cursor()

c.execute("""
INSERT INTO products (id, name, quantity, price, last_modified) VALUES 
(1, 'Babolat Racquet', 10, 150.00, 'user1'),
(2, 'Wilson Balls', 50, 2.50, 'user2'),
(3, 'Adidas Shoes', 20, 120.00, 'user3'),
(4, 'Wilson Overgrips', 100, 1.00, 'user4'),
(5, 'Babolat Backpack', 15, 70.00, 'user5')
""")

connie.commit()
connie.close()