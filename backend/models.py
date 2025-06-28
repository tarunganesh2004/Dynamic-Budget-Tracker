import sqlite3


def init_db():
    conn = sqlite3.connect("budget.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount FLOAT,
            category TEXT,
            date TEXT
        )
    """)
    conn.commit()
    conn.close()
