import sqlite3

def get_connection():
    conn = sqlite3.connect("coffeestry.db")
    return conn

def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT CHECK(role IN ('owner', 'staff')) NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_default_users():
    conn = get_connection()
    cursor = conn.cursor()

    # Default users
    users = [
        ("owner", "admin123", "owner"),
        ("staff", "staff123", "staff")
    ]

    for username, password, role in users:
        try:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                           (username, password, role))
        except sqlite3.IntegrityError:
            pass  # Ignore duplicates if already added

    conn.commit()
    conn.close()

def create_products_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def get_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, category, price FROM products")
    products = cursor.fetchall()  # list of tuples (id, name, category, price)
    conn.close()
    return products

def add_product(name, category, price):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO products (name, category, price) VALUES (?, ?, ?)",
        (name, category, price)
    )
    conn.commit()
    conn.close()

def delete_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
    conn.commit()
    conn.close()


# Run setup on import
create_table()
add_default_users()
create_products_table()
