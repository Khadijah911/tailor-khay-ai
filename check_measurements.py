import sqlite3

connection = sqlite3.connect("tailor_khay.db")
cursor = connection.cursor()

cursor.execute("""
SELECT customer_name, phone_number
FROM measurements
""")

rows = cursor.fetchall()

for row in rows:
    print(row)

connection.close()