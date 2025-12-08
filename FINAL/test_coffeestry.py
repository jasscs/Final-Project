"""
Unit Tests for Coffeestry POS System
=====================================
This module contains unit tests for the database operations and core functionality.

Run tests with: python -m pytest test_coffeestry.py -v
Or: python test_coffeestry.py
"""

import unittest
import sqlite3
import os
import sys
import tempfile
import shutil

# Import the database module
from database import (
    hash_password, verify_password, get_connection,
    register_user, login_user, check_username_exists,
    add_product, get_products, update_product, delete_product,
    create_customer, get_customers_for_business, delete_customer,
    save_order, get_all_orders, get_order_items,
    confirm_order, complete_order, cancel_order, mark_order_paid,
    get_total_business_owners, get_total_customers, get_total_sales, get_total_orders,
    get_user_by_id, update_user, delete_user
)


class TestPasswordHashing(unittest.TestCase):
    """Test cases for password hashing functionality"""
    
    def test_hash_password_returns_string(self):
        """Test that hash_password returns a string"""
        result = hash_password("testpassword")
        self.assertIsInstance(result, str)
    
    def test_hash_password_returns_64_chars(self):
        """Test that SHA-256 hash is 64 characters (hex)"""
        result = hash_password("testpassword")
        self.assertEqual(len(result), 64)
    
    def test_hash_password_consistent(self):
        """Test that same password produces same hash"""
        hash1 = hash_password("mypassword123")
        hash2 = hash_password("mypassword123")
        self.assertEqual(hash1, hash2)
    
    def test_hash_password_different_inputs(self):
        """Test that different passwords produce different hashes"""
        hash1 = hash_password("password1")
        hash2 = hash_password("password2")
        self.assertNotEqual(hash1, hash2)
    
    def test_verify_password_correct(self):
        """Test password verification with correct password"""
        password = "securepassword"
        hashed = hash_password(password)
        self.assertTrue(verify_password(password, hashed))
    
    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password"""
        hashed = hash_password("correctpassword")
        self.assertFalse(verify_password("wrongpassword", hashed))
    
    def test_hash_empty_password(self):
        """Test hashing an empty password"""
        result = hash_password("")
        self.assertEqual(len(result), 64)
    
    def test_hash_special_characters(self):
        """Test hashing password with special characters"""
        result = hash_password("p@$$w0rd!#$%^&*()")
        self.assertEqual(len(result), 64)
    
    def test_hash_unicode_password(self):
        """Test hashing password with unicode characters"""
        result = hash_password("密码测试123")
        self.assertEqual(len(result), 64)


class TestDatabaseConnection(unittest.TestCase):
    """Test cases for database connection"""
    
    def test_get_connection_returns_connection(self):
        """Test that get_connection returns a valid connection"""
        conn = get_connection()
        self.assertIsInstance(conn, sqlite3.Connection)
        conn.close()
    
    def test_connection_is_functional(self):
        """Test that connection can execute queries"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        self.assertEqual(result[0], 1)
        conn.close()


class TestUserRegistration(unittest.TestCase):
    """Test cases for user registration"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_username = f"testuser_{os.getpid()}"
        self.test_password = "testpass123"
    
    def tearDown(self):
        """Clean up test data"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE username LIKE 'testuser_%'")
        conn.commit()
        conn.close()
    
    def test_register_user_success(self):
        """Test successful user registration"""
        success, message = register_user(self.test_username, self.test_password, "staff")
        self.assertTrue(success)
        self.assertEqual(message, "Registration successful!")
    
    def test_register_duplicate_username(self):
        """Test registration with duplicate username fails"""
        register_user(self.test_username, self.test_password, "staff")
        success, message = register_user(self.test_username, "different_pass", "staff")
        self.assertFalse(success)
        self.assertEqual(message, "Username already exists!")
    
    def test_register_user_password_is_hashed(self):
        """Test that registered password is hashed in database"""
        register_user(self.test_username, self.test_password, "staff")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username=?", (self.test_username,))
        stored_password = cursor.fetchone()[0]
        conn.close()
        
        # Password should be hashed (64 chars) not plain text
        self.assertEqual(len(stored_password), 64)
        self.assertNotEqual(stored_password, self.test_password)
    
    def test_register_user_with_different_roles(self):
        """Test registration with different roles"""
        roles = ["owner", "staff", "customer"]
        for i, role in enumerate(roles):
            username = f"{self.test_username}_{i}"
            success, _ = register_user(username, self.test_password, role)
            self.assertTrue(success, f"Failed to register user with role: {role}")


class TestUserLogin(unittest.TestCase):
    """Test cases for user login"""
    
    def setUp(self):
        """Set up test user"""
        self.test_username = f"logintest_{os.getpid()}"
        self.test_password = "loginpass123"
        register_user(self.test_username, self.test_password, "staff")
    
    def tearDown(self):
        """Clean up test data"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE username LIKE 'logintest_%'")
        conn.commit()
        conn.close()
    
    def test_login_success(self):
        """Test successful login"""
        user = login_user(self.test_username, self.test_password)
        self.assertIsNotNone(user)
        self.assertEqual(user[1], self.test_username)  # username
        self.assertEqual(user[2], "staff")  # role
    
    def test_login_wrong_password(self):
        """Test login with wrong password"""
        user = login_user(self.test_username, "wrongpassword")
        self.assertIsNone(user)
    
    def test_login_nonexistent_user(self):
        """Test login with non-existent username"""
        user = login_user("nonexistent_user_xyz", "anypassword")
        self.assertIsNone(user)
    
    def test_login_empty_credentials(self):
        """Test login with empty credentials"""
        user = login_user("", "")
        self.assertIsNone(user)


class TestCheckUsernameExists(unittest.TestCase):
    """Test cases for username existence check"""
    
    def setUp(self):
        """Set up test user"""
        self.test_username = f"existstest_{os.getpid()}"
        register_user(self.test_username, "password123", "staff")
    
    def tearDown(self):
        """Clean up test data"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE username LIKE 'existstest_%'")
        conn.commit()
        conn.close()
    
    def test_username_exists(self):
        """Test that existing username returns True"""
        result = check_username_exists(self.test_username)
        self.assertTrue(result)
    
    def test_username_not_exists(self):
        """Test that non-existing username returns False"""
        result = check_username_exists("nonexistent_user_abc123")
        self.assertFalse(result)


class TestProductManagement(unittest.TestCase):
    """Test cases for product management"""
    
    def setUp(self):
        """Set up test owner"""
        self.test_owner = f"productowner_{os.getpid()}"
        register_user(self.test_owner, "password123", "owner")
        
        # Get owner ID
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username=?", (self.test_owner,))
        self.owner_id = cursor.fetchone()[0]
        conn.close()
    
    def tearDown(self):
        """Clean up test data"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE business_owner_id=?", (self.owner_id,))
        cursor.execute("DELETE FROM users WHERE username LIKE 'productowner_%'")
        conn.commit()
        conn.close()
    
    def test_add_product(self):
        """Test adding a product"""
        add_product("Test Coffee", "Coffee", 150.00, self.owner_id)
        products = get_products(self.owner_id)
        
        product_names = [p[1] for p in products]
        self.assertIn("Test Coffee", product_names)
    
    def test_add_product_with_category(self):
        """Test adding products with different categories"""
        add_product("Espresso Test", "Coffee", 120.00, self.owner_id)
        add_product("Muffin Test", "Pastry", 80.00, self.owner_id)
        
        products = get_products(self.owner_id)
        categories = [p[2] for p in products]
        
        self.assertIn("Coffee", categories)
        self.assertIn("Pastry", categories)
    
    def test_get_products_by_owner(self):
        """Test that products are filtered by owner"""
        add_product("Owner Product", "Coffee", 100.00, self.owner_id)
        
        # Products for this owner should include the added product
        products = get_products(self.owner_id)
        self.assertTrue(len(products) >= 1)
        
        # Products for non-existent owner should be empty
        products_other = get_products(99999)
        self.assertEqual(len(products_other), 0)
    
    def test_update_product(self):
        """Test updating a product"""
        add_product("Original Name", "Coffee", 100.00, self.owner_id)
        
        # Get the product ID
        products = get_products(self.owner_id)
        product_id = None
        for p in products:
            if p[1] == "Original Name":
                product_id = p[0]
                break
        
        self.assertIsNotNone(product_id)
        
        # Update the product
        update_product(product_id, "Updated Name", "Pastry", 150.00)
        
        # Verify update
        products = get_products(self.owner_id)
        updated_product = None
        for p in products:
            if p[0] == product_id:
                updated_product = p
                break
        
        self.assertEqual(updated_product[1], "Updated Name")
        self.assertEqual(updated_product[2], "Pastry")
        self.assertEqual(updated_product[3], 150.00)
    
    def test_delete_product(self):
        """Test deleting a product"""
        add_product("To Delete", "Coffee", 100.00, self.owner_id)
        
        # Get the product ID
        products = get_products(self.owner_id)
        product_id = None
        for p in products:
            if p[1] == "To Delete":
                product_id = p[0]
                break
        
        # Delete the product
        delete_product(product_id)
        
        # Verify deletion
        products = get_products(self.owner_id)
        product_names = [p[1] for p in products]
        self.assertNotIn("To Delete", product_names)


class TestCustomerManagement(unittest.TestCase):
    """Test cases for customer management"""
    
    def setUp(self):
        """Set up test owner"""
        self.test_owner = f"custowner_{os.getpid()}"
        register_user(self.test_owner, "password123", "owner")
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username=?", (self.test_owner,))
        self.owner_id = cursor.fetchone()[0]
        conn.close()
    
    def tearDown(self):
        """Clean up test data"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE business_owner_id=?", (self.owner_id,))
        cursor.execute("DELETE FROM users WHERE username LIKE 'custowner_%'")
        cursor.execute("DELETE FROM users WHERE username LIKE 'testcust_%'")
        conn.commit()
        conn.close()
    
    def test_create_customer(self):
        """Test creating a customer"""
        customer_name = f"testcust_{os.getpid()}"
        success, message = create_customer(customer_name, "custpass123", self.owner_id)
        
        self.assertTrue(success)
        self.assertEqual(message, "Customer created successfully!")
    
    def test_create_customer_password_hashed(self):
        """Test that customer password is hashed"""
        customer_name = f"testcust_hash_{os.getpid()}"
        create_customer(customer_name, "plainpassword", self.owner_id)
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username=?", (customer_name,))
        stored_password = cursor.fetchone()[0]
        conn.close()
        
        self.assertEqual(len(stored_password), 64)  # SHA-256 hex length
    
    def test_get_customers_for_business(self):
        """Test getting customers for a business owner"""
        customer_name = f"testcust_list_{os.getpid()}"
        create_customer(customer_name, "password123", self.owner_id)
        
        customers = get_customers_for_business(self.owner_id)
        customer_names = [c[1] for c in customers]
        
        self.assertIn(customer_name, customer_names)
    
    def test_customers_isolated_by_owner(self):
        """Test that customers are isolated by business owner"""
        customer_name = f"testcust_iso_{os.getpid()}"
        create_customer(customer_name, "password123", self.owner_id)
        
        # Customers for different owner should not include this customer
        customers = get_customers_for_business(99999)
        customer_names = [c[1] for c in customers]
        
        self.assertNotIn(customer_name, customer_names)


class TestOrderManagement(unittest.TestCase):
    """Test cases for order management"""
    
    def setUp(self):
        """Set up test data"""
        self.test_items = [
            {"name": "Test Coffee", "category": "Coffee", "price": 150.00, "quantity": 2},
            {"name": "Test Pastry", "category": "Pastry", "price": 80.00, "quantity": 1}
        ]
        self.total = (150.00 * 2) + (80.00 * 1)  # 380.00
    
    def tearDown(self):
        """Clean up test orders"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM order_items WHERE order_id IN (SELECT id FROM orders WHERE customer_name LIKE 'Test Customer%')")
        cursor.execute("DELETE FROM orders WHERE customer_name LIKE 'Test Customer%'")
        conn.commit()
        conn.close()
    
    def test_save_order(self):
        """Test saving an order"""
        order_id = save_order("Test Customer", "Dine in", self.total, self.test_items)
        
        self.assertIsNotNone(order_id)
        self.assertIsInstance(order_id, int)
        self.assertGreater(order_id, 0)
    
    def test_save_order_items(self):
        """Test that order items are saved correctly"""
        order_id = save_order("Test Customer Items", "Take out", self.total, self.test_items)
        
        items = get_order_items(order_id)
        
        self.assertEqual(len(items), 2)
        item_names = [item[0] for item in items]
        self.assertIn("Test Coffee", item_names)
        self.assertIn("Test Pastry", item_names)
    
    def test_get_all_orders(self):
        """Test getting all orders"""
        save_order("Test Customer Orders", "Dine in", self.total, self.test_items)
        
        orders = get_all_orders()
        
        self.assertIsInstance(orders, list)
        self.assertGreater(len(orders), 0)


class TestOrderStatusManagement(unittest.TestCase):
    """Test cases for order status management"""
    
    def setUp(self):
        """Set up test order"""
        self.test_items = [{"name": "Status Test", "category": "Coffee", "price": 100.00, "quantity": 1}]
        self.order_id = save_order("Test Customer Status", "Dine in", 100.00, self.test_items)
    
    def tearDown(self):
        """Clean up test data"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM order_items WHERE order_id=?", (self.order_id,))
        cursor.execute("DELETE FROM orders WHERE id=?", (self.order_id,))
        conn.commit()
        conn.close()
    
    def test_confirm_order(self):
        """Test confirming an order"""
        confirm_order(self.order_id)
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM orders WHERE id=?", (self.order_id,))
        status = cursor.fetchone()[0]
        conn.close()
        
        self.assertEqual(status, "confirmed")
    
    def test_complete_order(self):
        """Test completing an order"""
        complete_order(self.order_id)
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM orders WHERE id=?", (self.order_id,))
        status = cursor.fetchone()[0]
        conn.close()
        
        self.assertEqual(status, "completed")
    
    def test_cancel_order(self):
        """Test cancelling an order"""
        cancel_order(self.order_id)
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM orders WHERE id=?", (self.order_id,))
        status = cursor.fetchone()[0]
        conn.close()
        
        self.assertEqual(status, "cancelled")
    
    def test_mark_order_paid(self):
        """Test marking order as paid"""
        mark_order_paid(self.order_id)
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT payment_status FROM orders WHERE id=?", (self.order_id,))
        payment_status = cursor.fetchone()[0]
        conn.close()
        
        self.assertEqual(payment_status, "paid")


class TestAnalyticsFunctions(unittest.TestCase):
    """Test cases for analytics/statistics functions"""
    
    def test_get_total_business_owners(self):
        """Test getting total business owners count"""
        count = get_total_business_owners()
        self.assertIsInstance(count, int)
        self.assertGreaterEqual(count, 0)
    
    def test_get_total_customers(self):
        """Test getting total customers count"""
        count = get_total_customers()
        self.assertIsInstance(count, int)
        self.assertGreaterEqual(count, 0)
    
    def test_get_total_sales(self):
        """Test getting total sales"""
        total = get_total_sales()
        self.assertIsInstance(total, (int, float))
        self.assertGreaterEqual(total, 0)
    
    def test_get_total_orders(self):
        """Test getting total orders count"""
        count = get_total_orders()
        self.assertIsInstance(count, int)
        self.assertGreaterEqual(count, 0)


class TestUserManagement(unittest.TestCase):
    """Test cases for user management (admin functions)"""
    
    def setUp(self):
        """Set up test user"""
        self.test_username = f"mgmttest_{os.getpid()}"
        register_user(self.test_username, "password123", "staff")
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username=?", (self.test_username,))
        self.user_id = cursor.fetchone()[0]
        conn.close()
    
    def tearDown(self):
        """Clean up test data"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE username LIKE 'mgmttest_%'")
        conn.commit()
        conn.close()
    
    def test_get_user_by_id(self):
        """Test getting user by ID"""
        user = get_user_by_id(self.user_id)
        
        self.assertIsNotNone(user)
        self.assertEqual(user[1], self.test_username)
    
    def test_get_user_by_invalid_id(self):
        """Test getting user by invalid ID"""
        user = get_user_by_id(99999999)
        self.assertIsNone(user)
    
    def test_update_user(self):
        """Test updating user"""
        new_username = f"mgmttest_updated_{os.getpid()}"
        success, message = update_user(self.user_id, new_username, "newpassword", "owner")
        
        self.assertTrue(success)
        
        # Verify update
        user = get_user_by_id(self.user_id)
        self.assertEqual(user[1], new_username)
        self.assertEqual(user[3], "owner")


# Test runner
if __name__ == "__main__":
    # Run with verbosity
    unittest.main(verbosity=2)
