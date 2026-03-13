import sys
from datetime import datetime

from database import (
    add_product,
    create_customer,
    get_connection,
    get_customers_for_business,
    get_orders_for_business,
    get_products,
    register_user,
    save_order,
)


def _get_user_id(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None


def _cleanup(usernames, product_ids, order_ids):
    conn = get_connection()
    cur = conn.cursor()

    if order_ids:
        placeholders = ",".join(["?"] * len(order_ids))
        cur.execute(f"DELETE FROM order_items WHERE order_id IN ({placeholders})", tuple(order_ids))
        cur.execute(f"DELETE FROM orders WHERE id IN ({placeholders})", tuple(order_ids))

    if product_ids:
        placeholders = ",".join(["?"] * len(product_ids))
        cur.execute(f"DELETE FROM products WHERE id IN ({placeholders})", tuple(product_ids))

    if usernames:
        placeholders = ",".join(["?"] * len(usernames))
        cur.execute(f"DELETE FROM users WHERE username IN ({placeholders})", tuple(usernames))

    conn.commit()
    conn.close()


def run_test():
    stamp = datetime.now().strftime("%Y%m%d%H%M%S%f")

    owner1 = f"it_owner_a_{stamp}"
    owner2 = f"it_owner_b_{stamp}"
    staff1 = f"it_staff_a_{stamp}"
    staff2 = f"it_staff_b_{stamp}"
    customer1 = f"it_customer_a_{stamp}"
    customer2 = f"it_customer_b_{stamp}"

    created_usernames = [owner1, owner2, staff1, staff2, customer1, customer2]
    created_product_ids = []
    created_order_ids = []

    try:
        ok, msg = register_user(owner1, "Pass1234", "owner")
        assert ok, f"Failed to create owner1: {msg}"

        ok, msg = register_user(owner2, "Pass1234", "owner")
        assert ok, f"Failed to create owner2: {msg}"

        owner1_id = _get_user_id(owner1)
        owner2_id = _get_user_id(owner2)
        assert owner1_id and owner2_id, "Owner IDs not found after creation"

        ok, msg = register_user(staff1, "Pass1234", "staff", owner1_id)
        assert ok, f"Failed to create staff1: {msg}"

        ok, msg = register_user(staff2, "Pass1234", "staff", owner2_id)
        assert ok, f"Failed to create staff2: {msg}"

        ok, msg = create_customer(customer1, "Pass1234", owner1_id)
        assert ok, f"Failed to create customer1: {msg}"

        ok, msg = create_customer(customer2, "Pass1234", owner2_id)
        assert ok, f"Failed to create customer2: {msg}"

        add_product("ISO_Product_A", "Coffee", 100.0, owner1_id)
        add_product("ISO_Product_B", "Coffee", 120.0, owner2_id)

        owner1_products = get_products(owner1_id)
        owner2_products = get_products(owner2_id)

        p1 = next((p for p in owner1_products if p[1] == "ISO_Product_A"), None)
        p2 = next((p for p in owner2_products if p[1] == "ISO_Product_B"), None)
        assert p1 is not None, "Owner1 product not found"
        assert p2 is not None, "Owner2 product not found"
        created_product_ids.extend([p1[0], p2[0]])

        assert all(p[1] != "ISO_Product_B" for p in owner1_products), "Owner1 can see Owner2 product"
        assert all(p[1] != "ISO_Product_A" for p in owner2_products), "Owner2 can see Owner1 product"

        customer1_id = _get_user_id(customer1)
        customer2_id = _get_user_id(customer2)
        assert customer1_id and customer2_id, "Customer IDs not found after creation"

        order1 = save_order(
            customer_name=customer1,
            order_type="Dine in",
            total=200.0,
            items=[{"name": "ISO_Product_A", "category": "Coffee", "price": 100.0, "quantity": 2}],
            customer_id=customer1_id,
            business_owner_id=owner1_id,
        )
        order2 = save_order(
            customer_name=customer2,
            order_type="Take out",
            total=120.0,
            items=[{"name": "ISO_Product_B", "category": "Coffee", "price": 120.0, "quantity": 1}],
            customer_id=customer2_id,
            business_owner_id=owner2_id,
        )
        created_order_ids.extend([order1, order2])

        owner1_orders = get_orders_for_business(owner1_id)
        owner2_orders = get_orders_for_business(owner2_id)
        owner1_order_ids = {o[0] for o in owner1_orders}
        owner2_order_ids = {o[0] for o in owner2_orders}

        assert order1 in owner1_order_ids, "Owner1 order not found in owner1 scope"
        assert order2 in owner2_order_ids, "Owner2 order not found in owner2 scope"
        assert order2 not in owner1_order_ids, "Owner1 can see Owner2 order"
        assert order1 not in owner2_order_ids, "Owner2 can see Owner1 order"

        owner1_customers = get_customers_for_business(owner1_id)
        owner2_customers = get_customers_for_business(owner2_id)
        owner1_customer_names = {c[1] for c in owner1_customers}
        owner2_customer_names = {c[1] for c in owner2_customers}

        assert customer1 in owner1_customer_names, "Owner1 customer not found in owner1 scope"
        assert customer2 in owner2_customer_names, "Owner2 customer not found in owner2 scope"
        assert customer2 not in owner1_customer_names, "Owner1 can see Owner2 customer"
        assert customer1 not in owner2_customer_names, "Owner2 can see Owner1 customer"

        print("PASS: Multi-user and multi-client isolation checks succeeded.")
        return 0

    except AssertionError as exc:
        print(f"FAIL: {exc}")
        return 1

    finally:
        _cleanup(created_usernames, created_product_ids, created_order_ids)


if __name__ == "__main__":
    sys.exit(run_test())
