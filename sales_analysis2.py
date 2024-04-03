import sqlite3
import pandas as pd

conn = sqlite3.connect('my_database.db')

sql = """
SELECT c.customer_id, c.age, i.item_name, o.quantity
FROM Customers AS c
INNER JOIN Orders AS o ON c.customer_id = o.customer_id
INNER JOIN Items AS i ON o.item_id = i.item_id;
"""

data = pd.read_sql_query(sql, conn)


data_filtered = data[(data['age'] >= 18) & (data['age'] <= 35)]


data_grouped = data_filtered.groupby(['customer_id', 'age', 'item_name'])['quantity'].sum().reset_index()
data_grouped = data_grouped[data_grouped['quantity'] > 0]  


data_grouped.to_csv('output.csv', index=False, header=True, delimiter=';')

conn.close()

print("Successfully extracted data and stored in output.csv")
