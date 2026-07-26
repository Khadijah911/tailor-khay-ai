import sqlite3

connection = sqlite3.connect("tailor_khay.db")
connection.row_factory = sqlite3.Row

cursor = connection.cursor()

cursor.execute("""
SELECT *
FROM measurements
WHERE customer_name = ?
""", ("Aisha",))

row = cursor.fetchone()

print(dict(row))

connection.close()