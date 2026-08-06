import sqlite3

conn = sqlite3.connect("tailor_khay.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS customer_memories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone TEXT NOT NULL,
    memory_type TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("Customer memory table created successfully.")