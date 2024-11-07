import sqlite3

DATABASE_NAME = 'payfast_tip_app.db'

def initialize_database():
    # Connect to the database
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            email TEXT NOT NULL,
            name_first TEXT NOT NULL,
            is_admin INTEGER NOT NULL DEFAULT 0
        )
    ''')
    # Create payments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            amount REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Commit changes to the database
    conn.commit()
    # Check if admin user exists, if not, create it
    cursor.execute('SELECT * FROM users WHERE username = ?', ('admin',))
    if not cursor.fetchone():
        cursor.execute('INSERT INTO users (username, password, email, name_first, is_admin) VALUES (?, ?, ?, ?, ?)', 
                       ('admin', 'admin123', 'admin@example.com', 'Admin', 1))
        conn.commit()
    # Close the database connection
    conn.close()

def add_user(username, password, email, name_first):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, password, email, name_first, is_admin) VALUES (?, ?, ?, ?, ?)', 
                   (username, password, email, name_first, 0))
    conn.commit()
    conn.close()

def delete_user(username):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE username = ?', (username,))
    conn.commit()
    conn.close()

def get_user(username, password):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

def save_payment(username, amount):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO payments (username, amount) VALUES (?, ?)', (username, amount))
    conn.commit()
    conn.close()

def get_payments(username=None):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    if username:
        cursor.execute('SELECT amount, timestamp FROM payments WHERE username = ?', (username,))
    else:
        cursor.execute('SELECT username, amount, timestamp FROM payments')
    payments = cursor.fetchall()
    conn.close()
    return payments

def get_all_users():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT username, email, name_first, is_admin FROM users')
    users = cursor.fetchall()
    conn.close()
    return users

def get_total_amount(username):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT SUM(amount) FROM payments WHERE username = ?', (username,))
    total = cursor.fetchone()[0]
    conn.close()
    return total if total else 0