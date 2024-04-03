import sqlite3
import pandas as pd


conn = sqlite3.connect('my_database.db')


conn.execute('''
CREATE TABLE IF NOT EXISTS Customers (
    customer_id INTEGER PRIMARY KEY,
    age INTEGER,
    item TEXT,
    quantity INTEGER
)
''')

conn.execute('''
CREATE TABLE IF NOT EXISTS Orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    item_id INTEGER,
    quantity INTEGER,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
)
''')

conn.execute('''
CREATE TABLE IF NOT EXISTS Items (
    item_id INTEGER PRIMARY KEY,
    item_name TEXT
)
''')


conn.commit()


sql = """
SELECT c.customer_id, c.age, i.item_name, o.quantity
FROM Customers AS c
INNER JOIN Orders AS o ON c.customer_id = o.customer_id
INNER JOIN Items AS i ON o.item_id = i.item_id;
"""


try:
    data = pd.read_sql_query(sql, conn)

    
    data_filtered = data[(data['age'] >= 18) & (data['age'] <= 35)]
    data_grouped = data_filtered.groupby(['customer_id', 'age', 'item_name'])['quantity'].sum().reset_index()
    data_grouped = data_grouped[data_grouped['quantity'] > 0]  

    
    data_grouped.to_csv('output.csv', index=False, header=True, sep=';') 

    print("Successfully extracted data and stored in output.csv")
except pd.io.sql.DatabaseError as e:
    print("DatabaseError:", e)


conn.close()

