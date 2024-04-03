import sqlite3
import csv

conn = sqlite3.connect('my_database.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS Customers (
    customer_id INTEGER PRIMARY KEY,
    age INTEGER,
    item TEXT,
    quantity INTEGER
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS Orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    item_id INTEGER,
    quantity INTEGER,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS Items (
    item_id INTEGER PRIMARY KEY,
    item_name TEXT
)
''')

sql = """
SELECT c.customer_id, c.age, i.item_name, SUM(COALESCE(o.quantity, 0)) AS quantity
FROM Customers AS c
INNER JOIN Orders AS o ON c.customer_id = o.customer_id
INNER JOIN Items AS i ON o.item_id = i.item_id
WHERE c.age BETWEEN 18 AND 35
GROUP BY c.customer_id, c.age, i.item_name
HAVING SUM(COALESCE(o.quantity, 0)) > 0
ORDER BY c.customer_id, c.age, i.item_name;
"""

c.execute(sql)
results = c.fetchall()

with open(r'C:\Users\yoges\OneDrive\Desktop\sales_analysis\output.csv', 'w', newline='') as csvfile:

    writer = csv.writer(csvfile, delimiter=';')
    writer.writerow(['Customer ID', 'Age', 'Item Name', 'Quantity'])  

    for row in results:
        writer.writerow(row) 

conn.close()

print("Successfully extracted data and stored in output.csv")

