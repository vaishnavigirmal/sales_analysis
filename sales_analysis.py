import sqlite3
import csv

conn = sqlite3.connect('your_database.db')
c = conn.cursor()

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

with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    writer.writerow(['Customer', 'Age', 'Item', 'Quantity'])

    for row in results:
        writer.writerow(row)

conn.close()

print("Successfully extracted data and stored in output.csv")
