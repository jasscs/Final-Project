import flet as ft
from datetime import datetime
from config import *
from database_new import get_all_products, save_order

def create_orders_view(page, main_content):
    """Create the Making Orders view"""
    
    # Get products from database
    products = get_all_products()
    cart_items = []
    
    # Customer info fields
    customer_name_field = ft.TextField(
        hint_text="Enter customer name",
        bgcolor=BG_CARD,
        color=TEXT_DARK,
        border_color=ACCENT_WARM,
        focused_border_color=PRIMARY_MID,
        border_radius=8,
        width=200,
        prefix_icon=ft.Icons.PERSON,
    )
    
    order_date_field = ft.TextField(
        hint_text="Order Date",
        bgcolor=BG_CARD,
        color=TEXT_DARK,
        border_color=ACCENT_WARM,
        focused_border_color=PRIMARY_MID,
        border_radius=8,
        width=200,
        prefix_icon=ft.Icons.CALENDAR_TODAY,
        value=datetime.now().strftime("%Y-%m-%d"),
        read_only=True,
    )
    
    order_type_dropdown = ft.Dropdown(
        width=200,
        color=TEXT_DARK,
        value="Dine in",
        bgcolor=BG_CARD,
        border_color=ACCENT_WARM,
        focused_border_color=PRIMARY_MID,
        border_radius=8,
        options=[
            ft.dropdown.Option("Dine in"),
            ft.dropdown.Option("Take out"),
        ],
    )

    # Order summary elements
    order_summary_column = ft.Column([], spacing=5, scroll=ft.ScrollMode.AUTO)
    total_text = ft.Text("₱ 0.00", size=28, weight=ft.FontWeight.BOLD, color=PRIMARY_DARK)
    customer_display = ft.Text("Walk-in Customer", size=14, color=TEXT_DARK, weight=ft.FontWeight.W_500)
    
    # Cart Table
    cart_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Product", weight=ft.FontWeight.W_600, color=PRIMARY_DARK)),
            ft.DataColumn(ft.Text("Price", weight=ft.FontWeight.W_600, color=PRIMARY_DARK)),
            ft.DataColumn(ft.Text("Qty", weight=ft.FontWeight.W_600, color=PRIMARY_DARK)),
            ft.DataColumn(ft.Text("Total", weight=ft.FontWeight.W_600, color=PRIMARY_DARK)),
            ft.DataColumn(ft.Text("", color=PRIMARY_DARK)),
        ],
        rows=[],
        border=ft.border.all(1, ACCENT_WARM),
        border_radius=10,
        heading_row_color=ACCENT_CREAM,
    )

    def update_customer_display(e=None):
        name = customer_name_field.value.strip()
        customer_display.value = name if name else "Walk-in Customer"
        page.update()

    customer_name_field.on_change = update_customer_display

    def update_cart_table():
        total = 0
        rows = []
        summary_items = []
        
        for i, item in enumerate(cart_items):
            total_item = item["price"] * item["quantity"]
            total += total_item

            def make_remove_handler(idx):
                def remove_item(e):
                    cart_items.pop(idx)
                    update_cart_table()
                return remove_item

            rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(item["name"], color=TEXT_DARK)),
                    ft.DataCell(ft.Text(f"₱{item['price']:.2f}", color=TEXT_DARK)),
                    ft.DataCell(ft.Text(str(item["quantity"]), color=TEXT_DARK)),
                    ft.DataCell(ft.Text(f"₱{total_item:.2f}", weight=ft.FontWeight.W_600, color=PRIMARY_MID)),
                    ft.DataCell(ft.IconButton(
                        ft.Icons.DELETE_OUTLINE,
                        icon_color=ERROR,
                        icon_size=20,
                        on_click=make_remove_handler(i)
                    ))
                ])
            )
            
            summary_items.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(f"{item['name']} x{item['quantity']}", size=13, color=TEXT_DARK, expand=True),
                            ft.Text(f"₱{total_item:.2f}", size=13, weight=ft.FontWeight.W_500, color=PRIMARY_MID),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    padding=ft.padding.symmetric(vertical=4, horizontal=8),
                    bgcolor=ACCENT_CREAM,
                    border_radius=5,
                )
            )
        
        cart_table.rows = rows
        order_summary_column.controls = summary_items
        total_text.value = f"₱ {total:.2f}"
        page.update()

    def proceed_to_payment(e):
        if not cart_items:
            page.snack_bar = ft.SnackBar(
                ft.Text("Cart is empty! Please add items first.", color=ACCENT_CREAM),
                bgcolor=ERROR,
            )
            page.snack_bar.open = True
            page.update()
            return
        
        # Calculate total
        total = sum(item["price"] * item["quantity"] for item in cart_items)
        customer_name = customer_name_field.value.strip() or "Walk-in Customer"
        order_type = order_type_dropdown.value
        
        # Save order to database
        order_id = save_order(customer_name, order_type, total, cart_items)
        
        # Show success message
        page.snack_bar = ft.SnackBar(
            ft.Text(f"Order #{order_id} saved successfully! Total: ₱{total:.2f}", color=ACCENT_CREAM),
            bgcolor=SUCCESS,
        )
        page.snack_bar.open = True
        
        # Clear cart
        cart_items.clear()
        customer_name_field.value = ""
        customer_display.value = "Walk-in Customer"
        update_cart_table()

    # Create product rows with quantity controls
    product_rows = []
    for product in products:
        qty_ref = {"value": 1}  # Use dict to avoid closure issues
        qty_text = ft.Text(value="1", size=14, width=30, text_align=ft.TextAlign.CENTER, color=TEXT_DARK)

        def make_decrease_handler(qt, qr):
            def decrease(e):
                if qr["value"] > 1:
                    qr["value"] -= 1
                    qt.value = str(qr["value"])
                    page.update()
            return decrease

        def make_increase_handler(qt, qr):
            def increase(e):
                qr["value"] += 1
                qt.value = str(qr["value"])
                page.update()
            return increase

        def make_add_handler(prod, qr, qt):
            def add_to_cart(e):
                qty = qr["value"]
                # Check if product already in cart
                for item in cart_items:
                    if item["name"] == prod["name"]:
                        item["quantity"] += qty
                        update_cart_table()
                        # Reset quantity
                        qr["value"] = 1
                        qt.value = "1"
                        page.update()
                        return
                cart_items.append({
                    "name": prod["name"],
                    "category": prod["category"],
                    "price": prod["price"],
                    "quantity": qty
                })
                update_cart_table()
                # Reset quantity
                qr["value"] = 1
                qt.value = "1"
                page.update()
            return add_to_cart

        product_rows.append(
            ft.DataRow(cells=[
                ft.DataCell(ft.Text(product["name"], color=TEXT_DARK)),
                ft.DataCell(
                    ft.Container(
                        content=ft.Text(product["category"], size=11, color=ACCENT_CREAM),
                        bgcolor=PRIMARY_LIGHT if product["category"] == "Coffee" else ACCENT_GOLD,
                        padding=ft.padding.symmetric(horizontal=8, vertical=2),
                        border_radius=10,
                    )
                ),
                ft.DataCell(ft.Text(f"₱{product['price']:.2f}", color=TEXT_DARK, weight=ft.FontWeight.W_500)),
                ft.DataCell(
                    ft.Row([
                        ft.IconButton(ft.Icons.REMOVE_CIRCLE_OUTLINE, 
                                     on_click=make_decrease_handler(qty_text, qty_ref), 
                                     icon_color=PRIMARY_MID, icon_size=18),
                        qty_text,
                        ft.IconButton(ft.Icons.ADD_CIRCLE_OUTLINE, 
                                     on_click=make_increase_handler(qty_text, qty_ref), 
                                     icon_color=PRIMARY_MID, icon_size=18)
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=0)
                ),
                ft.DataCell(
                    ft.IconButton(
                        ft.Icons.ADD_SHOPPING_CART,
                        on_click=make_add_handler(product, qty_ref, qty_text),
                        icon_color=SUCCESS,
                        bgcolor=ft.Colors.with_opacity(0.1, SUCCESS),
                        icon_size=20,
                    )
                )
            ])
        )

    product_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Product", weight=ft.FontWeight.W_600, color=PRIMARY_DARK)),
            ft.DataColumn(ft.Text("Category", weight=ft.FontWeight.W_600, color=PRIMARY_DARK)),
            ft.DataColumn(ft.Text("Price", weight=ft.FontWeight.W_600, color=PRIMARY_DARK)),
            ft.DataColumn(ft.Text("Quantity", weight=ft.FontWeight.W_600, color=PRIMARY_DARK)),
            ft.DataColumn(ft.Text("Add", weight=ft.FontWeight.W_600, color=PRIMARY_DARK)),
        ],
        rows=product_rows,
        border=ft.border.all(1, ACCENT_WARM),
        border_radius=10,
        heading_row_color=ACCENT_CREAM,
    )

    # Main Making Orders Panel
    making_orders_panel = ft.Container(
        bgcolor=BG_CARD,
        padding=20,
        border_radius=15,
        shadow=ft.BoxShadow(
            color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
            blur_radius=15,
            offset=ft.Offset(0, 4)
        ),
        content=ft.Column(
            [
                # Header
                ft.Row(
                    [
                        ft.Icon(ft.Icons.SHOPPING_BAG, size=26, color=PRIMARY_MID),
                        ft.Text("Making Orders", size=20, weight=ft.FontWeight.BOLD, color=PRIMARY_DARK),
                    ],
                    spacing=10,
                ),
                ft.Divider(height=15, color=ACCENT_CREAM, thickness=2),
                
                # Customer Info Row
                ft.Row(
                    [
                        ft.Column([
                            ft.Text("Customer Name", size=12, color=TEXT_MID, weight=ft.FontWeight.W_500),
                            customer_name_field,
                        ], spacing=3),
                        ft.Column([
                            ft.Text("Order Date", size=12, color=TEXT_MID, weight=ft.FontWeight.W_500),
                            order_date_field,
                        ], spacing=3),
                        ft.Column([
                            ft.Text("Order Type", size=12, color=TEXT_MID, weight=ft.FontWeight.W_500),
                            order_type_dropdown,
                        ], spacing=3),
                    ],
                    spacing=20,
                    wrap=True,
                ),
                
                ft.Container(height=10),
                
                # Product List Section
                ft.Container(
                    content=ft.Column([
                        ft.Text("Product List", size=14, weight=ft.FontWeight.W_600, color=PRIMARY_DARK),
                        ft.Container(height=8),
                        product_table,
                    ]),
                    bgcolor=ft.Colors.with_opacity(0.3, ACCENT_CREAM),
                    padding=12,
                    border_radius=10,
                ),
                
                ft.Container(height=10),
                
                # Cart Section
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.SHOPPING_CART, size=18, color=PRIMARY_MID),
                            ft.Text("Cart", size=14, weight=ft.FontWeight.W_600, color=PRIMARY_DARK),
                        ], spacing=6),
                        ft.Container(height=8),
                        cart_table,
                    ]),
                    bgcolor=ft.Colors.with_opacity(0.3, ACCENT_CREAM),
                    padding=12,
                    border_radius=10,
                ),
            ],
            spacing=8,
            scroll=ft.ScrollMode.AUTO,
        ),
        expand=True,
    )

    # Order Details Panel (Right Side)
    order_details_panel = ft.Container(
        bgcolor=BG_CARD,
        padding=20,
        border_radius=15,
        width=280,
        shadow=ft.BoxShadow(
            color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
            blur_radius=15,
            offset=ft.Offset(0, 4)
        ),
        content=ft.Column(
            [
                # Header
                ft.Row(
                    [
                        ft.Icon(ft.Icons.RECEIPT_LONG, size=22, color=PRIMARY_MID),
                        ft.Text("Order Details", size=16, weight=ft.FontWeight.BOLD, color=PRIMARY_DARK),
                    ],
                    spacing=8,
                ),
                ft.Divider(height=12, color=ACCENT_CREAM, thickness=2),
                
                # Customer Info Display
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.PERSON_OUTLINE, size=14, color=TEXT_MID),
                            ft.Text("Customer:", size=11, color=TEXT_MID),
                        ], spacing=4),
                        customer_display,
                    ], spacing=2),
                    bgcolor=ACCENT_CREAM,
                    padding=10,
                    border_radius=8,
                ),
                
                ft.Container(height=10),
                
                # Items Summary
                ft.Text("Items Summary", size=13, weight=ft.FontWeight.W_600, color=TEXT_MID),
                ft.Container(
                    content=order_summary_column,
                    bgcolor=ft.Colors.with_opacity(0.5, ACCENT_CREAM),
                    padding=8,
                    border_radius=8,
                    height=180,
                ),
                
                ft.Container(expand=True),
                
                # Total Section
                ft.Divider(height=15, color=ACCENT_WARM, thickness=1),
                ft.Row(
                    [
                        ft.Text("Total:", size=16, weight=ft.FontWeight.W_600, color=TEXT_MID),
                        total_text,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                
                ft.Container(height=12),
                
                # Proceed to Payment Button
                ft.ElevatedButton(
                    "Proceed to Payment",
                    icon=ft.Icons.PAYMENT,
                    bgcolor=PRIMARY_MID,
                    color=ACCENT_CREAM,
                    width=240,
                    height=45,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=12),
                        elevation=3,
                    ),
                    on_click=proceed_to_payment,
                ),
            ],
            spacing=6,
        ),
    )

    # Main Layout
    dashboard_view = ft.Row(
        [
            making_orders_panel,
            order_details_panel,
        ],
        spacing=15,
        expand=True,
    )

    main_content.content = ft.Container(
        padding=15,
        bgcolor=BG_LIGHT,
        content=dashboard_view,
        expand=True,
    )
    page.update()
