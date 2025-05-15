import sqlite3

def get_connection():
    return sqlite3.connect("healthcare.db", check_same_thread=False)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        gender TEXT,
        diagnosis TEXT
    )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        date TEXT,
        doctor TEXT
    )""")
    cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES ('admin', 'admin', 'admin')")
    cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES ('user', 'user', 'user')")
    conn.commit()
    conn.close()
