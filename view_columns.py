import sqlite3

connection = sqlite3.connect("tailor_khay.db")
cursor = connection.cursor()

cursor.execute("PRAGMA table_info(measurements)")

for column in cursor.fetchall():
    print(column)

connection.close()