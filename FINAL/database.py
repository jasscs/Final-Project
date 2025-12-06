import sqlite3
import os
from datetime import datetime, timedelta
print("Database path:", os.path.abspath("coffeestry.db"))

def get_connection():
    conn = sqlite3.connect("coffeestry.db")
    return conn

def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    # Check if users table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    table_exists = cursor.fetchone()
    
    if table_exists:
        # Check if the table has old constraint by trying to insert a customer role
        try:
            cursor.execute("INSERT INTO users (username, password, role) VALUES ('__test_constraint__', 'test', 'customer')")
            # If successful, delete the test row and continue
            cursor.execute("DELETE FROM users WHERE username = '__test_constraint__'")
            conn.commit()
        except sqlite3.IntegrityError:
            # Old constraint exists - need to recreate table
            print("Migrating users table to support new roles...")
            
            # Backup existing data
            cursor.execute("SELECT id, username, password, role FROM users")
            existing_users = cursor.fetchall()
            
            # Drop old table
            cursor.execute("DROP TABLE users")
            
            # Create new table with updated constraint
            cursor.execute("""
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT CHECK(role IN ('superadmin', 'owner', 'staff', 'customer')) NOT NULL,
                    business_owner_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (business_owner_id) REFERENCES users(id)
                )
            """)
            
            # Restore existing users
            for user in existing_users:
                try:
                    cursor.execute("INSERT INTO users (id, username, password, role) VALUES (?, ?, ?, ?)", user)
                except:
                    pass
            conn.commit()
            print("Migration completed!")
        
        # Check if business_owner_id column exists
        cursor.execute("PRAGMA table_info(users)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'business_owner_id' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN business_owner_id INTEGER")
        if 'created_at' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN created_at TIMESTAMP")
    else:
        # Create new users table with all columns
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT CHECK(role IN ('superadmin', 'owner', 'staff', 'customer')) NOT NULL,
                business_owner_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (business_owner_id) REFERENCES users(id)
            )
        """)
    conn.commit()
    conn.close()

def add_default_users():
    conn = get_connection()
    cursor = conn.cursor()

    # Default users including superadmin
    users = [
        ("superadmin", "superadmin123", "superadmin", None),
        ("owner", "admin123", "owner", None),
        ("staff", "staff123", "staff", None)
    ]

    for username, password, role, business_owner_id in users:
        try:
            cursor.execute("INSERT INTO users (username, password, role, business_owner_id) VALUES (?, ?, ?, ?)",
                           (username, password, role, business_owner_id))
        except sqlite3.IntegrityError:
            pass  # Ignore duplicates if already added

    conn.commit()
    conn.close()

def create_products_table():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if products table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='products'")
    table_exists = cursor.fetchone()
    
    if table_exists:
        # Check and add business_owner_id column if missing
        cursor.execute("PRAGMA table_info(products)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'business_owner_id' not in columns:
            cursor.execute("ALTER TABLE products ADD COLUMN business_owner_id INTEGER")
            print("Added business_owner_id column to products table!")
    else:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price REAL NOT NULL,
                business_owner_id INTEGER,
                FOREIGN KEY (business_owner_id) REFERENCES users(id)
            )
        """)
    
    conn.commit()
    conn.close()

def add_default_products():
    """Default products are no longer added - each business owner has their own products"""
    pass  # Each business owner manages their own products

def create_orders_table():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if orders table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='orders'")
    table_exists = cursor.fetchone()
    
    if table_exists:
        # Check and add missing columns
        cursor.execute("PRAGMA table_info(orders)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'customer_id' not in columns:
            cursor.execute("ALTER TABLE orders ADD COLUMN customer_id INTEGER")
        if 'business_owner_id' not in columns:
            cursor.execute("ALTER TABLE orders ADD COLUMN business_owner_id INTEGER")
        if 'status' not in columns:
            cursor.execute("ALTER TABLE orders ADD COLUMN status TEXT DEFAULT 'pending'")
        if 'payment_status' not in columns:
            cursor.execute("ALTER TABLE orders ADD COLUMN payment_status TEXT DEFAULT 'unpaid'")
    else:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT,
                customer_id INTEGER,
                business_owner_id INTEGER,
                order_type TEXT,
                total REAL NOT NULL,
                status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'confirmed', 'completed', 'cancelled')),
                payment_status TEXT DEFAULT 'unpaid' CHECK(payment_status IN ('unpaid', 'paid')),
                order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES users(id),
                FOREIGN KEY (business_owner_id) REFERENCES users(id)
            )
        """)
    
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

def get_products(business_owner_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    if business_owner_id:
        cursor.execute("SELECT id, name, category, price FROM products WHERE business_owner_id = ?", (business_owner_id,))
    else:
        cursor.execute("SELECT id, name, category, price FROM products")
    products = cursor.fetchall()  # list of tuples (id, name, category, price)
    conn.close()
    return products

def add_product(name, category, price, business_owner_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO products (name, category, price, business_owner_id) VALUES (?, ?, ?, ?)",
        (name, category, price, business_owner_id)
    )
    conn.commit()
    conn.close()

def delete_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
    conn.commit()
    conn.close()

def register_user(username, password, role="staff"):
    """Register a new user in the database"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                       (username, password, role))
        conn.commit()
        conn.close()
        return True, "Registration successful!"
    except sqlite3.IntegrityError:
        conn.close()
        return False, "Username already exists!"
    except Exception as e:
        conn.close()
        return False, f"Error: {str(e)}"

def check_username_exists(username):
    """Check if username already exists"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username=?", (username,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def update_product(product_id, name, category, price):
    """Update an existing product"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET name=?, category=?, price=? WHERE id=?",
                   (name, category, price, product_id))
    conn.commit()
    conn.close()

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
    return order_id

def get_all_orders():
    """Get all orders with their items"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, customer_name, order_type, total, order_date, status, payment_status FROM orders ORDER BY order_date DESC")
    orders = cursor.fetchall()
    conn.close()
    return orders

def get_order_items(order_id):
    """Get items for a specific order"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT product_name, category, price, quantity FROM order_items WHERE order_id=?", (order_id,))
    items = cursor.fetchall()
    conn.close()
    return items

# ============ SUPERADMIN FUNCTIONS ============

def get_all_business_owners():
    """Get all business owners (owner and staff roles)"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password, role, created_at FROM users WHERE role IN ('owner', 'staff') ORDER BY created_at DESC")
    users = cursor.fetchall()
    conn.close()
    return users

def get_total_business_owners():
    """Get count of business owners"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users WHERE role IN ('owner', 'staff')")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_total_customers():
    """Get count of all customers"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'customer'")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_total_sales():
    """Get total sales amount"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COALESCE(SUM(total), 0) FROM orders WHERE payment_status = 'paid'")
    total = cursor.fetchone()[0]
    conn.close()
    return total

def get_sales_by_date(days=7):
    """Get sales data for the last N days"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DATE(order_date) as date, SUM(total) as total_sales
        FROM orders 
        WHERE payment_status = 'paid' AND order_date >= date('now', ?)
        GROUP BY DATE(order_date)
        ORDER BY date ASC
    """, (f'-{days} days',))
    sales = cursor.fetchall()
    conn.close()
    return sales

def get_customers_by_date(days=7):
    """Get new customers count for the last N days"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DATE(created_at) as date, COUNT(*) as count
        FROM users 
        WHERE role = 'customer' AND created_at >= date('now', ?)
        GROUP BY DATE(created_at)
        ORDER BY date ASC
    """, (f'-{days} days',))
    customers = cursor.fetchall()
    conn.close()
    return customers

def delete_user(user_id):
    """Delete a user"""
    conn = get_connection()
    cursor = conn.cursor()
    # First delete their customers
    cursor.execute("DELETE FROM users WHERE business_owner_id = ?", (user_id,))
    # Then delete the user
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

def update_user(user_id, username, password, role):
    """Update user credentials"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE users SET username=?, password=?, role=? WHERE id=?",
                       (username, password, role, user_id))
        conn.commit()
        conn.close()
        return True, "User updated successfully!"
    except sqlite3.IntegrityError:
        conn.close()
        return False, "Username already exists!"
    except Exception as e:
        conn.close()
        return False, f"Error: {str(e)}"

def get_user_by_id(user_id):
    """Get user by ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password, role, business_owner_id, created_at FROM users WHERE id=?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

# ============ BUSINESS OWNER FUNCTIONS ============

def create_customer(username, password, business_owner_id):
    """Create a customer account linked to a business owner"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, role, business_owner_id) VALUES (?, ?, 'customer', ?)",
                       (username, password, business_owner_id))
        conn.commit()
        conn.close()
        return True, "Customer created successfully!"
    except sqlite3.IntegrityError:
        conn.close()
        return False, "Username already exists!"
    except Exception as e:
        conn.close()
        return False, f"Error: {str(e)}"

def get_customers_for_business(business_owner_id):
    """Get all customers for a specific business owner"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password, created_at FROM users WHERE role='customer' AND business_owner_id=? ORDER BY created_at DESC", (business_owner_id,))
    customers = cursor.fetchall()
    conn.close()
    return customers

def get_orders_for_business(business_owner_id):
    """Get all orders for a business owner"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT o.id, o.customer_name, o.order_type, o.total, o.status, o.payment_status, o.order_date, u.username
        FROM orders o
        LEFT JOIN users u ON o.customer_id = u.id
        WHERE o.business_owner_id = ?
        ORDER BY o.order_date DESC
    """, (business_owner_id,))
    orders = cursor.fetchall()
    conn.close()
    return orders

def get_pending_orders_for_business(business_owner_id):
    """Get pending orders for a business owner"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT o.id, o.customer_name, o.order_type, o.total, o.status, o.payment_status, o.order_date, u.username
        FROM orders o
        LEFT JOIN users u ON o.customer_id = u.id
        WHERE o.business_owner_id = ? AND o.status = 'pending'
        ORDER BY o.order_date DESC
    """, (business_owner_id,))
    orders = cursor.fetchall()
    conn.close()
    return orders

def confirm_order(order_id):
    """Confirm an order"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET status = 'confirmed' WHERE id = ?", (order_id,))
    conn.commit()
    conn.close()

def complete_order(order_id):
    """Complete an order"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET status = 'completed' WHERE id = ?", (order_id,))
    conn.commit()
    conn.close()

def cancel_order(order_id):
    """Cancel an order"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET status = 'cancelled' WHERE id = ?", (order_id,))
    conn.commit()
    conn.close()

def mark_order_paid(order_id):
    """Mark order as paid"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET payment_status = 'paid' WHERE id = ?", (order_id,))
    conn.commit()
    conn.close()

def get_business_sales(business_owner_id):
    """Get total sales for a business owner"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COALESCE(SUM(total), 0) FROM orders WHERE business_owner_id = ? AND payment_status = 'paid'", (business_owner_id,))
    total = cursor.fetchone()[0]
    conn.close()
    return total

def delete_customer(customer_id):
    """Delete a customer"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ? AND role = 'customer'", (customer_id,))
    conn.commit()
    conn.close()

# ============ CUSTOMER FUNCTIONS ============

def get_products_for_customer(business_owner_id):
    """Get products for a specific business owner"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, category, price FROM products WHERE business_owner_id = ?", (business_owner_id,))
    products = cursor.fetchall()
    conn.close()
    return products

def get_best_sellers(business_owner_id=None, limit=3):
    """Get top selling products"""
    conn = get_connection()
    cursor = conn.cursor()
    if business_owner_id:
        cursor.execute("""
            SELECT oi.product_name, oi.category, oi.price, SUM(oi.quantity) as total_sold
            FROM order_items oi
            JOIN orders o ON oi.order_id = o.id
            WHERE o.business_owner_id = ? AND oi.category = 'Coffee'
            GROUP BY oi.product_name
            ORDER BY total_sold DESC
            LIMIT ?
        """, (business_owner_id, limit))
    else:
        cursor.execute("""
            SELECT oi.product_name, oi.category, oi.price, SUM(oi.quantity) as total_sold
            FROM order_items oi
            WHERE oi.category = 'Coffee'
            GROUP BY oi.product_name
            ORDER BY total_sold DESC
            LIMIT ?
        """, (limit,))
    products = cursor.fetchall()
    conn.close()
    return products

def place_customer_order(customer_id, customer_name, business_owner_id, order_type, total, items):
    """Place an order as a customer"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO orders (customer_name, customer_id, business_owner_id, order_type, total, status, payment_status)
        VALUES (?, ?, ?, ?, ?, 'pending', 'unpaid')
    """, (customer_name, customer_id, business_owner_id, order_type, total))
    order_id = cursor.lastrowid
    
    for item in items:
        cursor.execute("""
            INSERT INTO order_items (order_id, product_name, category, price, quantity)
            VALUES (?, ?, ?, ?, ?)
        """, (order_id, item["name"], item["category"], item["price"], item["quantity"]))
    
    conn.commit()
    conn.close()
    return order_id

def get_customer_orders(customer_id):
    """Get order history for a customer"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, customer_name, order_type, total, status, payment_status, order_date
        FROM orders
        WHERE customer_id = ?
        ORDER BY order_date DESC
    """, (customer_id,))
    orders = cursor.fetchall()
    conn.close()
    return orders

def get_customer_business_owner(customer_id):
    """Get the business owner for a customer"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT business_owner_id FROM users WHERE id = ?", (customer_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def login_user(username, password):
    """Login a user and return their details"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role, business_owner_id FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

# ============ SUPERADMIN ANALYTICS FUNCTIONS ============

def get_orders_by_date(days=30):
    """Get orders count for the last N days"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DATE(order_date) as date, COUNT(*) as count
        FROM orders 
        WHERE order_date >= date('now', ?)
        GROUP BY DATE(order_date)
        ORDER BY date ASC
    """, (f'-{days} days',))
    orders = cursor.fetchall()
    conn.close()
    return orders

def get_top_business_owners(limit=5):
    """Get top performing business owners by sales"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.username, COALESCE(SUM(o.total), 0) as total_sales, COUNT(o.id) as order_count
        FROM users u
        LEFT JOIN orders o ON u.id = o.business_owner_id AND o.payment_status = 'paid'
        WHERE u.role IN ('owner', 'staff')
        GROUP BY u.id
        ORDER BY total_sales DESC
        LIMIT ?
    """, (limit,))
    owners = cursor.fetchall()
    conn.close()
    return owners

def get_order_status_distribution():
    """Get distribution of order statuses"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT status, COUNT(*) as count
        FROM orders
        GROUP BY status
    """)
    distribution = cursor.fetchall()
    conn.close()
    return distribution

def get_monthly_revenue(months=6):
    """Get monthly revenue for the last N months"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT strftime('%Y-%m', order_date) as month, SUM(total) as revenue
        FROM orders 
        WHERE payment_status = 'paid' AND order_date >= date('now', ?)
        GROUP BY strftime('%Y-%m', order_date)
        ORDER BY month ASC
    """, (f'-{months} months',))
    revenue = cursor.fetchall()
    conn.close()
    return revenue

def get_total_orders():
    """Get total number of orders"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM orders")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_total_products():
    """Get total number of products"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM products")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_top_selling_products(limit=5):
    """Get top selling products across all business owners"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT oi.product_name, SUM(oi.quantity) as total_sold, SUM(oi.price * oi.quantity) as total_revenue
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.id
        WHERE o.payment_status = 'paid'
        GROUP BY oi.product_name
        ORDER BY total_sold DESC
        LIMIT ?
    """, (limit,))
    products = cursor.fetchall()
    conn.close()
    return products


# Run setup on import
create_table()
add_default_users()
create_products_table()
add_default_products()
create_orders_table()
