import sqlite3
connection=sqlite3.connect('tailor_khay.db')
cursor=connection.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS measurements (
    customer_name TEXT,
    phone_number TEXT PRIMARY KEY,

    bust REAL,
    waist REAL,
    hip REAL,

    full_length REAL,
    half_length REAL,

    sleeve_length REAL,
    shoulder REAL,

    shoulder_to_nipple REAL,
    shoulder_to_underbust REAL,

    blouse_length REAL,
    waist_to_hip REAL,

    lap REAL,
    trouser_length REAL,

    round_sleeve REAL,

    nipple_to_nipple REAL,
    upper_cleavage REAL,
    lower_cleavage REAL,

    created_at TEXT,
    updated_at TEXT
)
""")

connection.commit()
connection.close()
