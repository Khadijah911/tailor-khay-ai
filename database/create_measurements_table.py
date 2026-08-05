import sqlite3

connection = sqlite3.connect("tailor_khay.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS measurements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT,
    phone_number TEXT UNIQUE,
    bust REAL,
    waist REAL,
    hip REAL,
    full_length REAL,
    half_length REAL,
    blouse_length REAL,
    shoulder REAL,
    sleeve_length REAL,
    round_sleeve REAL,
    nipple_to_nipple REAL,
    shoulder_to_nipple REAL,
    shoulder_to_underbust REAL,
    waist_to_hip REAL,
    lap REAL,
    trouser_length REAL,
    upper_cleavage REAL,
    lower_cleavage REAL
)
""")

connection.commit()
connection.close()

print("Measurements table created successfully!")