import sqlite3
import os

# Database path - use a new database file
DB_FILE = "coffeestry_pos.db"
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), DB_FILE)

def get_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    return conn

def init_database():
    """Initialize all database tables"""
    conn = get_connection()
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT CHECK(role IN ('owner', 'staff')) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create products table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create orders table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            order_type TEXT CHECK(order_type IN ('Dine in', 'Take out')) NOT NULL,
            total REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create order_items table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id)
        )
    """)

    conn.commit()
    conn.close()
    print(f"[DB] Database initialized: {DB_PATH}")

def add_default_data():
    """Add default users and products if they don't exist"""
    conn = get_connection()
    cursor = conn.cursor()

    # Check if default owner exists
    cursor.execute("SELECT id FROM users WHERE username='owner'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                       ("owner", "admin123", "owner"))
        print("[DB] Default owner account created")

    # Check if default staff exists
    cursor.execute("SELECT id FROM users WHERE username='staff'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                       ("staff", "staff123", "staff"))
        print("[DB] Default staff account created")

    # Default products
    default_products = [
        ("Espresso", "Coffee", 120.00),
        ("Cappuccino", "Coffee", 150.00),
        ("Latte", "Coffee", 160.00),
        ("Americano", "Coffee", 130.00),
        ("Mocha", "Coffee", 170.00),
        ("Blueberry Muffin", "Pastry", 80.00),
        ("Chocolate Croissant", "Pastry", 90.00),
        ("Cinnamon Roll", "Pastry", 85.00),
        ("Cheesecake", "Pastry", 120.00),
    ]

    for name, category, price in default_products:
        cursor.execute("SELECT id FROM products WHERE name=?", (name,))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO products (name, category, price) VALUES (?, ?, ?)",
                           (name, category, price))

    conn.commit()
    conn.close()
    print("[DB] Default data loaded")

# ==================== USER OPERATIONS ====================

def authenticate_user(username, password):
    """Authenticate user and return role if valid"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()
    conn.close()
    if result:
        print(f"[DB] User '{username}' authenticated successfully")
        return result[0]
    else:
        print(f"[DB] Authentication failed for '{username}'")
        return None

def register_user(username, password, role="staff"):
    """Register a new user"""
    print(f"[DB] Attempting to register user: {username}")
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                       (username, password, role))
        conn.commit()
        print(f"[DB] User '{username}' registered successfully!")
        conn.close()
        return True, "Registration successful!"
    except sqlite3.IntegrityError as e:
        print(f"[DB] Registration failed: {e}")
        conn.close()
        return False, "Username already exists!"
    except Exception as e:
        print(f"[DB] Registration error: {e}")
        conn.close()
        return False, f"Error: {str(e)}"

def check_username_exists(username):
    """Check if username already exists"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username=?", (username,))
    result = cursor.fetchone()
    conn.close()
    exists = result is not None
    print(f"[DB] Username '{username}' exists: {exists}")
    return exists

def get_all_users():
    """Get all users"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role, created_at FROM users ORDER BY id")
    rows = cursor.fetchall()
    conn.close()
    return rows

# ==================== PRODUCT OPERATIONS ====================

def get_all_products():
    """Get all products as list of dictionaries"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, category, price FROM products ORDER BY category, name")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "category": r[2], "price": r[3]} for r in rows]

def add_product(name, category, price):
    """Add a new product"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name, category, price) VALUES (?, ?, ?)",
                   (name, category, price))
    conn.commit()
    conn.close()
    print(f"[DB] Product '{name}' added")

def update_product(product_id, name, category, price):
    """Update an existing product"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET name=?, category=?, price=? WHERE id=?",
                   (name, category, price, product_id))
    conn.commit()
    conn.close()
    print(f"[DB] Product ID {product_id} updated")

def delete_product(product_id):
    """Delete a product"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
    conn.commit()
    conn.close()
    print(f"[DB] Product ID {product_id} deleted")

# ==================== ORDER OPERATIONS ====================

def save_order(customer_name, order_type, total, items):
    """Save an order with its items"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO orders (customer_name, order_type, total) VALUES (?, ?, ?)",
                   (customer_name, order_type, total))
    order_id = cursor.lastrowid
    
    for item in items:
        cursor.execute("""
            INSERT INTO order_items (order_id, product_name, category, price, quantity)
            VALUES (?, ?, ?, ?, ?)
        """, (order_id, item["name"], item["category"], item["price"], item["quantity"]))
    
    conn.commit()
    conn.close()
    print(f"[DB] Order #{order_id} saved (Total: {total})")
    return order_id

def get_all_orders():
    """Get all orders"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, customer_name, order_type, total, created_at FROM orders ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

# ==================== INITIALIZE ====================
# Initialize database when module is imported
init_database()
add_default_data()
