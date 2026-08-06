import sqlite3

DB_NAME = "tailor_khay.db"


def save_memory(phone: str, content: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Check whether this exact memory already exists
    cursor.execute(
        """
        SELECT id
        FROM customer_memories
        WHERE phone = ?

        AND content = ?
        """,
        (phone, content),
    )

    existing = cursor.fetchone()

    if existing:
        conn.close()
        return False

    cursor.execute(
        """
        INSERT INTO customer_memories (phone, content)
        VALUES (?, ?)
        """,
        (phone, content),
    )

    conn.commit()
    conn.close()

    return True


def load_memories(phone: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT  content
        FROM customer_memories
        WHERE phone = ?
        ORDER BY created_at
        """,
        (phone,),
    )

    memories = cursor.fetchall()

    conn.close()

    return memories