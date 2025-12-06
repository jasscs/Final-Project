import flet as ft 
from database import (get_connection, add_product, get_products, delete_product, register_user, 
                      check_username_exists, update_product, save_order, get_all_orders, get_order_items,
                      get_all_business_owners, get_total_business_owners, get_total_customers, get_total_sales,
                      get_sales_by_date, get_customers_by_date, delete_user, update_user, get_user_by_id,
                      create_customer, get_customers_for_business, get_orders_for_business, get_pending_orders_for_business,
                      confirm_order, complete_order, cancel_order, mark_order_paid, get_business_sales, delete_customer,
                      get_products_for_customer, get_best_sellers, place_customer_order, get_customer_orders,
                      get_customer_business_owner, login_user, get_orders_by_date, get_top_business_owners,
                      get_order_status_distribution, get_monthly_revenue, get_total_orders, get_total_products,
                      get_top_selling_products)
from prod import products
from flet import TextField, ElevatedButton, Text, Row, Column 
from datetime import datetime
import random
import string
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

# Color Palette - Modern Coffee Shop Theme
PRIMARY_DARK = "#2C1810"      # Dark espresso brown
PRIMARY_MID = "#5D4037"       # Medium coffee brown
PRIMARY_LIGHT = "#8D6E63"     # Light mocha
ACCENT_WARM = "#D4A574"       # Warm caramel/latte
ACCENT_CREAM = "#F5E6D3"      # Cream/milk
ACCENT_GOLD = "#C9A86C"       # Golden highlight
BG_LIGHT = "#FFF8F0"          # Warm white background
BG_CARD = "#FFFFFF"           # Card background
TEXT_DARK = "#1A1110"         # Almost black text
TEXT_MID = "#4A3728"          # Medium brown text
TEXT_LIGHT = "#8B7355"        # Light brown text
SUCCESS = "#4CAF50"           # Green for success
ERROR = "#E57373"             # Soft red for errors

def main(page: ft.Page):
    page.title = "Coffeestry System"
    page.bgcolor = BG_LIGHT
    page.window_maximized = True
    page.window_resizable = True
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.fonts = {"Poppins": "https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap"}

    # Store the last save path for receipts (default to receipts folder)
    default_receipts_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "receipts")
    if not os.path.exists(default_receipts_folder):
        os.makedirs(default_receipts_folder)
    last_save_path = {"path": default_receipts_folder}  # Using dict to allow modification in nested functions

    page.appbar = ft.AppBar(
        title=ft.Text("☕ Coffeestry System", size=18, color=ACCENT_CREAM, weight=ft.FontWeight.W_600),
        center_title=True,
        bgcolor=PRIMARY_DARK,
        elevation=4,
    )
    
    # HOME PAGE
    def layout1():
        page.clean()

        main_container = ft.Container(expand=True, bgcolor=BG_LIGHT)

        page.add(main_container)    

        home_content = ft.Column(
            [
                ft.Container(
                    content=ft.Image(src="logo.png", width=400, height=300, fit=ft.ImageFit.CONTAIN),
                    alignment=ft.alignment.top_center,
                    margin=ft.margin.only(top=5, bottom=5),
                ),
                ft.Text("Welcome to Coffeestry", size=36, weight=ft.FontWeight.BOLD, color=PRIMARY_DARK),
                ft.Text("Your cozy coffee shop system", size=18, color=TEXT_MID, italic=True),
                ft.Container(height=20),
                ft.Container(
                    content=ft.ElevatedButton(
                        "Login", on_click=lambda e: layout3(),
                        bgcolor=PRIMARY_MID, color=ACCENT_CREAM, width=280,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=25),
                            elevation=3,
                        )
                    ),
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    content=ft.ElevatedButton(
                        "Sign Up", on_click=lambda e: signup_page(),
                        bgcolor=ACCENT_GOLD, color=PRIMARY_DARK, width=280,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=25),
                            elevation=3,
                        )
                    ),
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    content=ft.ElevatedButton(
                        "About", on_click=lambda e: layout2(),
                        bgcolor=ACCENT_WARM, color=PRIMARY_DARK, width=280,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=25),
                            elevation=3,
                        )
                    ),
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    content=ft.ElevatedButton(
                        "Exit", on_click=lambda e: page.window_close(),
                        bgcolor=PRIMARY_LIGHT, color=ACCENT_CREAM, width=280,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=25),
                            elevation=3,
                        )
                    ),
                    alignment=ft.alignment.center,
                ),
                ft.Container(height=30),
                ft.Text("© 2025 Coffeestry", size=12, color=TEXT_LIGHT,
                        italic=True, text_align=ft.TextAlign.CENTER),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=12,
        )
        main_container.content = home_content
        page.update()


    # ABOUT COFFEESTRY PAGE
    def layout2():
        page.clean()
        page.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Container(
                            content=ft.Icon(ft.Icons.LOCAL_CAFE, size=80, color=ACCENT_WARM),
                            bgcolor=PRIMARY_DARK,
                            border_radius=50,
                            padding=20,
                        ),
                        ft.Text(
                            "About Coffeestry",
                            size=32,
                            weight=ft.FontWeight.BOLD,
                            color=PRIMARY_DARK
                        ),
                        ft.Container(
                            content=ft.Text(
                                "Coffeestry is a coffee shop that serves freshly brewed coffee and freshly baked pastries.\n"
                                "We aim to provide a cozy and inviting atmosphere for coffee and pastry lovers.",
                                size=16,
                                color=TEXT_MID,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            width=500,
                        ),
                        ft.Container(height=20),
                        ft.ElevatedButton(
                            "Back",
                            on_click=lambda e: layout1(),
                            width=200,
                            bgcolor=PRIMARY_MID,
                            color=ACCENT_CREAM,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=25),
                                elevation=3,
                            )
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                ),
                padding=40,
                margin=30,
                border_radius=20,
                bgcolor=BG_CARD,
                alignment=ft.alignment.center,
                expand=True,
                shadow=ft.BoxShadow(
                    color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
                    blur_radius=20,
                    offset=ft.Offset(0, 8)
                ),
            )
        )
   
    # LOGIN PAGE (need to create user roles in the database)
    def layout3():
        page.clean()

        def login_clicked(e):
            username = username_field.value
            password = password_field.value

            user = login_user(username, password)

            if user:
                user_id, username, role, business_owner_id = user
                role = role.lower()
                message.value = f"Welcome, {role.capitalize()}!"
                message.color = SUCCESS
                page.update()

                if role == "superadmin":
                    superadmin_dashboard()
                elif role == "owner":
                    layout4(user_id)
                elif role == "staff":
                    # Show welcome page for staff
                    welcome_page(username, role, user_id)
                elif role == "customer":
                    customer_portal(user_id, username, business_owner_id)
            else:
                message.value = "Invalid username or password!"
                message.color = ERROR
                page.update()

        username_field = ft.TextField(
            label="Username", width=320, color=TEXT_DARK,
            border_color=PRIMARY_LIGHT, focused_border_color=PRIMARY_MID,
            label_style=ft.TextStyle(color=TEXT_MID),
            border_radius=12,
            on_submit=lambda e: page.focus(password_field)
        )
        password_field = ft.TextField(
            label="Password", password=True, can_reveal_password=True,
            width=320, color=TEXT_DARK,
            border_color=PRIMARY_LIGHT, focused_border_color=PRIMARY_MID,
            label_style=ft.TextStyle(color=TEXT_MID),
            border_radius=12,
            on_submit=login_clicked
        )
        message = ft.Text(value="", color=ERROR)

        login_button = ft.ElevatedButton(
            "Login", on_click=login_clicked, width=320,
            bgcolor=PRIMARY_MID, color=ACCENT_CREAM,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=25),
                elevation=3,
            )
        )
        back_button = ft.OutlinedButton(
            "Back", on_click=lambda e: layout1(), width=320,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=25),
                side=ft.BorderSide(2, PRIMARY_MID),
            )
        )

        page.add(
            ft.Container(
                content=ft.Row(
                    [
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Icon(ft.Icons.COFFEE, size=50, color=PRIMARY_MID),
                                    ft.Text("Login to Coffeestry", size=24, weight=ft.FontWeight.BOLD, color=PRIMARY_DARK),
                                    ft.Container(height=10),
                                    username_field,
                                    password_field,
                                    ft.Container(height=10),
                                    login_button,
                                    ft.Row(
                                        [
                                            ft.Text("Don't have an account?", size=13, color=TEXT_MID),
                                            ft.TextButton(
                                                "Sign Up",
                                                on_click=lambda e: signup_page(),
                                                style=ft.ButtonStyle(color=PRIMARY_MID),
                                            ),
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                    ),
                                    back_button,
                                    message,
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=12,
                            ),
                            padding=40,
                            width=400,
                            bgcolor=BG_CARD,
                            border_radius=20,
                            shadow=ft.BoxShadow(
                                color=ft.Colors.with_opacity(0.12, ft.Colors.BLACK),
                                blur_radius=25,
                                offset=ft.Offset(0, 10)
                            ),
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True,
                ),
                expand=True,
                bgcolor=BG_LIGHT,
            )
        )

    # SIGNUP PAGE
    def signup_page():
        page.clean()

        def signup_clicked(e):
            username = (username_field.value or "").strip()
            password = password_field.value or ""
            confirm_password = confirm_password_field.value or ""

            # Validation
            if not username or not password or not confirm_password:
                message.value = "Please fill in all fields!"
                message.color = ERROR
                page.update()
                return

            if len(username) < 3:
                message.value = "Username must be at least 3 characters!"
                message.color = ERROR
                page.update()
                return

            if len(password) < 6:
                message.value = "Password must be at least 6 characters!"
                message.color = ERROR
                page.update()
                return

            if password != confirm_password:
                message.value = "Passwords do not match!"
                message.color = ERROR
                page.update()
                return

            if check_username_exists(username):
                message.value = "Username already exists!"
                message.color = ERROR
                page.update()
                return

            # Register user
            success, msg = register_user(username, password, "staff")
            
            if success:
                page.snack_bar = ft.SnackBar(
                    ft.Text(f"Account '{username}' created successfully!", color=ACCENT_CREAM),
                    bgcolor=SUCCESS,
                )
                page.snack_bar.open = True
                page.update()
                layout3()  # Go to login page
            else:
                message.value = msg
                message.color = ERROR
                page.update()

        username_field = ft.TextField(
            label="Username", 
            width=320, 
            color=TEXT_DARK,
            border_color=PRIMARY_LIGHT, 
            focused_border_color=PRIMARY_MID,
            label_style=ft.TextStyle(color=TEXT_MID),
            border_radius=12,
            prefix_icon=ft.Icons.PERSON,
            hint_text="At least 3 characters",
        )
        
        password_field = ft.TextField(
            label="Password", 
            password=True, 
            can_reveal_password=True,
            width=320, 
            color=TEXT_DARK,
            border_color=PRIMARY_LIGHT, 
            focused_border_color=PRIMARY_MID,
            label_style=ft.TextStyle(color=TEXT_MID),
            border_radius=12,
            prefix_icon=ft.Icons.LOCK,
            hint_text="At least 6 characters"
        )

        confirm_password_field = ft.TextField(
            label="Confirm Password", 
            password=True, 
            can_reveal_password=True,
            width=320, 
            color=TEXT_DARK,
            border_color=PRIMARY_LIGHT, 
            focused_border_color=PRIMARY_MID,
            label_style=ft.TextStyle(color=TEXT_MID),
            border_radius=12,
            prefix_icon=ft.Icons.LOCK_OUTLINE,
            on_submit=signup_clicked
        )
        
        message = ft.Text(value="", color=ERROR, size=14)

        page.add(
            ft.Container(
                content=ft.Row(
                    [
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Icon(ft.Icons.PERSON_ADD, size=50, color=PRIMARY_MID),
                                    ft.Text("Create Account", size=24, weight=ft.FontWeight.BOLD, color=PRIMARY_DARK),
                                    ft.Text("Join Coffeestry today", size=14, color=TEXT_MID),
                                    ft.Container(height=15),
                                    username_field,
                                    password_field,
                                    confirm_password_field,
                                    ft.Container(height=10),
                                    ft.ElevatedButton(
                                        "Sign Up", 
                                        on_click=signup_clicked, 
                                        width=320,
                                        bgcolor=PRIMARY_MID, 
                                        color=ACCENT_CREAM,
                                        style=ft.ButtonStyle(
                                            shape=ft.RoundedRectangleBorder(radius=25),
                                            elevation=3,
                                        )
                                    ),
                                    ft.Row(
                                        [
                                            ft.Text("Already have an account?", size=13, color=TEXT_MID),
                                            ft.TextButton(
                                                "Login",
                                                on_click=lambda e: layout3(),
                                                style=ft.ButtonStyle(color=PRIMARY_MID),
                                            ),
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                    ),
                                    ft.OutlinedButton(
                                        "Back to Home", 
                                        on_click=lambda e: layout1(), 
                                        width=320,
                                        style=ft.ButtonStyle(
                                            shape=ft.RoundedRectangleBorder(radius=25),
                                            side=ft.BorderSide(2, PRIMARY_MID),
                                        )
                                    ),
                                    message,
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=10,
                            ),
                            padding=40,
                            width=420,
                            bgcolor=BG_CARD,
                            border_radius=20,
                            shadow=ft.BoxShadow(
                                color=ft.Colors.with_opacity(0.12, ft.Colors.BLACK),
                                blur_radius=25,
                                offset=ft.Offset(0, 10)
                            ),
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True,
                ),
                expand=True,
                bgcolor=BG_LIGHT,
            )
        )

    # WELCOME PAGE FOR STAFF
    def welcome_page(username, role, user_id):
        page.clean()
        
        def continue_to_dashboard(e):
            layout4(user_id)  # Go to the main dashboard
        
        page.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Container(
                            content=ft.Icon(ft.Icons.WAVING_HAND, size=80, color=ACCENT_WARM),
                            bgcolor=PRIMARY_DARK,
                            border_radius=50,
                            padding=25,
                        ),
                        ft.Container(height=20),
                        ft.Text(
                            f"Welcome, {username.capitalize()}!",
                            size=36,
                            weight=ft.FontWeight.BOLD,
                            color=PRIMARY_DARK
                        ),
                        ft.Text(
                            f"Role: {role.capitalize()}",
                            size=18,
                            color=TEXT_MID,
                            italic=True
                        ),
                        ft.Container(height=10),
                        ft.Container(
                            content=ft.Text(
                                "You have successfully logged into Coffeestry POS System.\n"
                                "Click the button below to continue to the dashboard.",
                                size=16,
                                color=TEXT_MID,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            width=450,
                        ),
                        ft.Container(height=30),
                        ft.ElevatedButton(
                            "Continue to Dashboard",
                            on_click=continue_to_dashboard,
                            width=280,
                            height=50,
                            bgcolor=PRIMARY_MID,
                            color=ACCENT_CREAM,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=25),
                                elevation=3,
                            ),
                            icon=ft.Icons.ARROW_FORWARD,
                        ),
                        ft.Container(height=20),
                        ft.Text(
                            "☕ Ready to serve great coffee!",
                            size=14,
                            color=TEXT_LIGHT,
                            italic=True
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=8,
                ),
                padding=50,
                margin=30,
                border_radius=25,
                bgcolor=BG_CARD,
                alignment=ft.alignment.center,
                expand=True,
                shadow=ft.BoxShadow(
                    color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
                    blur_radius=25,
                    offset=ft.Offset(0, 10)
                ),
            )
        )

# OWNER DASHBOARD
    def layout4(current_user_id=None):
        page.clean()
        main_content = ft.Container(expand=True, bgcolor=BG_LIGHT)

# DASHBOARD PAGE (Making Orders - with Order Details panel)
        def layout5():
            # Load products from database
            def load_dashboard_products():
                db_products = get_products(current_user_id)  # Returns list of tuples (id, name, category, price)
                return [{"id": p[0], "name": p[1], "category": p[2], "price": p[3]} for p in db_products]
            
            dashboard_products = load_dashboard_products()
            
            def order_type_changed(e):
                if e.control:
                    print("Selected Order Type:", e.control.value)

            cart_items = []
            customer_name_field = ft.TextField(
                hint_text="Enter customer name",
                bgcolor=BG_CARD,
                color=TEXT_DARK,
                border_color=ACCENT_WARM,
                focused_border_color=PRIMARY_MID,
                border_radius=8,
                width=220,
                prefix_icon=ft.Icons.PERSON,
            )
            
            order_date_field = ft.TextField(
                hint_text="Enter Order Date",
                bgcolor=BG_CARD,
                color=TEXT_DARK,
                border_color=ACCENT_WARM,
                focused_border_color=PRIMARY_MID,
                border_radius=8,
                width=220,
                prefix_icon=ft.Icons.CALENDAR_TODAY,
                value=datetime.now().strftime("%Y-%m-%d"),
            )
            
            order_type_dropdown = ft.Dropdown(
                width=220,
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
                on_change=order_type_changed
            )

            # Order Details Panel elements
            order_summary_column = ft.Column([], spacing=5, scroll=ft.ScrollMode.AUTO)
            total_text = ft.Text("₱ 0.00", size=28, weight=ft.FontWeight.BOLD, color=PRIMARY_DARK)
            cart_total = [0]  # Use list to make it mutable in nested functions
            
            # Customer name display in order details
            customer_display = ft.Text("Walk-in Customer", size=14, color=TEXT_DARK, weight=ft.FontWeight.W_500)
            order_type_display = ft.Text("Dine in", size=14, color=TEXT_DARK, weight=ft.FontWeight.W_500)
            
            # Order confirmed status
            order_confirmed = [False]
            confirmed_order_items = []
            
            # Cart Table
            cart_table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Product", weight=ft.FontWeight.W_600, color=PRIMARY_DARK)),
                    ft.DataColumn(ft.Text("Category", weight=ft.FontWeight.W_600, color=PRIMARY_DARK)),
                    ft.DataColumn(ft.Text("Price", weight=ft.FontWeight.W_600, color=PRIMARY_DARK)),
                    ft.DataColumn(ft.Text("Qty", weight=ft.FontWeight.W_600, color=PRIMARY_DARK)),
                    ft.DataColumn(ft.Text("Total", weight=ft.FontWeight.W_600, color=PRIMARY_DARK)),
                    ft.DataColumn(ft.Text("", color=PRIMARY_DARK)),
                ],
                rows=[],
                border=ft.border.all(1, ACCENT_WARM),
                border_radius=10,
                heading_row_color=ACCENT_CREAM,
                data_row_color={ft.ControlState.HOVERED: ft.Colors.with_opacity(0.1, ACCENT_WARM)},
            )

            def update_cart_table():
                total = 0
                rows = []
                
                for i, item in enumerate(cart_items):
                    total_item = item["price"] * item["quantity"]
                    total += total_item

                    def remove_item(e, idx=i):
                        cart_items.pop(idx)
                        update_cart_table()

                    rows.append(
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text(item["name"], color=TEXT_DARK)),
                            ft.DataCell(ft.Text(item["category"], color=TEXT_MID)),
                            ft.DataCell(ft.Text(f"₱{item['price']:.2f}", color=TEXT_DARK)),
                            ft.DataCell(ft.Text(str(item["quantity"]), color=TEXT_DARK)),
                            ft.DataCell(ft.Text(f"₱{total_item:.2f}", weight=ft.FontWeight.W_600, color=PRIMARY_MID)),
                            ft.DataCell(ft.IconButton(
                                ft.Icons.DELETE_OUTLINE,
                                icon_color=ERROR,
                                icon_size=20,
                                on_click=remove_item
                            ))
                        ])
                    )
                
                cart_table.rows = rows
                cart_total[0] = total
                page.update()
            
            def confirm_order(e):
                if not cart_items:
                    page.snack_bar = ft.SnackBar(
                        ft.Text("Cart is empty! Add items first.", color=ACCENT_CREAM),
                        bgcolor=ERROR,
                    )
                    page.snack_bar.open = True
                    page.update()
                    return
                
                # Update customer info display
                customer_name = customer_name_field.value if customer_name_field.value else "Walk-in Customer"
                customer_display.value = customer_name
                order_type_display.value = order_type_dropdown.value
                
                # Copy cart items to confirmed order
                confirmed_order_items.clear()
                confirmed_order_items.extend(cart_items.copy())
                
                # Build order summary
                summary_items = []
                total = 0
                for item in confirmed_order_items:
                    total_item = item["price"] * item["quantity"]
                    total += total_item
                    summary_items.append(
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.Text(f"{item['name']} x{item['quantity']}", size=14, color=TEXT_DARK, expand=True),
                                    ft.Text(f"₱{total_item:.2f}", size=14, weight=ft.FontWeight.W_500, color=PRIMARY_MID),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            padding=ft.padding.symmetric(vertical=5, horizontal=10),
                            bgcolor=ACCENT_CREAM,
                            border_radius=5,
                        )
                    )
                
                order_summary_column.controls = summary_items
                total_text.value = f"₱ {total:.2f}"
                order_confirmed[0] = True
                
                # Show success message
                page.snack_bar = ft.SnackBar(
                    ft.Text(f"Order confirmed! Total: ₱{total:.2f}", color=ACCENT_CREAM),
                    bgcolor=SUCCESS,
                )
                page.snack_bar.open = True
                page.update()
            
            def clear_cart(e):
                cart_items.clear()
                update_cart_table()
                page.snack_bar = ft.SnackBar(
                    ft.Text("Cart cleared!", color=ACCENT_CREAM),
                    bgcolor=PRIMARY_MID,
                )
                page.snack_bar.open = True
                page.update()
            
            def proceed_to_payment(e):
                if not order_summary_column.controls:
                    page.snack_bar = ft.SnackBar(
                        ft.Text("Please confirm your order first!", color=ACCENT_CREAM),
                        bgcolor=ERROR,
                    )
                    page.snack_bar.open = True
                    page.update()
                    return
                
                if not confirmed_order_items:
                    page.snack_bar = ft.SnackBar(
                        ft.Text("No items to process!", color=ACCENT_CREAM),
                        bgcolor=ERROR,
                    )
                    page.snack_bar.open = True
                    page.update()
                    return
                
                # Get order details
                customer_name = customer_display.value if customer_display.value else "Walk-in Customer"
                order_type = order_type_display.value if order_type_display.value else "Dine in"
                total = cart_total[0]
                
                # Payment mode selection
                selected_payment = [None]
                
                # Generate random QR code data
                def generate_qr_code():
                    qr_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
                    return f"COFFEESTRY-PAY-{qr_id}"
                
                qr_code_data = [generate_qr_code()]
                
                # QR Code display container (initially hidden)
                qr_display = ft.Container(
                    content=ft.Column([
                        ft.Text("Scan QR Code to Pay", size=14, weight=ft.FontWeight.W_600, color=PRIMARY_DARK),
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(ft.Icons.QR_CODE_2, size=120, color=PRIMARY_DARK),
                                ft.Text(qr_code_data[0], size=10, color=TEXT_MID, selectable=True),
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                            bgcolor=BG_CARD,
                            padding=15,
                            border_radius=10,
                            border=ft.border.all(2, PRIMARY_MID),
                        ),
                        ft.Text(f"Amount: ₱{total:.2f}", size=16, weight=ft.FontWeight.BOLD, color=SUCCESS),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                    padding=15,
                    bgcolor=ACCENT_CREAM,
                    border_radius=10,
                    visible=False,
                )
                
                def select_payment(mode):
                    selected_payment[0] = mode
                    # Update button styles
                    cash_btn.bgcolor = SUCCESS if mode == "Cash" else BG_CARD
                    cash_btn.content.controls[0].color = ACCENT_CREAM if mode == "Cash" else PRIMARY_MID
                    cash_btn.content.controls[1].color = ACCENT_CREAM if mode == "Cash" else TEXT_DARK
                    
                    qr_btn.bgcolor = SUCCESS if mode == "Online QR" else BG_CARD
                    qr_btn.content.controls[0].color = ACCENT_CREAM if mode == "Online QR" else PRIMARY_MID
                    qr_btn.content.controls[1].color = ACCENT_CREAM if mode == "Online QR" else TEXT_DARK
                    
                    # Show/hide QR code and regenerate
                    if mode == "Online QR":
                        qr_code_data[0] = generate_qr_code()
                        qr_display.content.controls[1].content.controls[1].value = qr_code_data[0]
                        qr_display.visible = True
                    else:
                        qr_display.visible = False
                    
                    page.update()
                
                cash_btn = ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.MONEY, size=32, color=PRIMARY_MID),
                        ft.Text("Cash", size=14, weight=ft.FontWeight.W_600, color=TEXT_DARK),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                    width=120,
                    height=80,
                    bgcolor=BG_CARD,
                    border_radius=12,
                    border=ft.border.all(2, ACCENT_WARM),
                    alignment=ft.alignment.center,
                    on_click=lambda e: select_payment("Cash"),
                    ink=True,
                )
                
                qr_btn = ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.QR_CODE, size=32, color=PRIMARY_MID),
                        ft.Text("Online QR", size=14, weight=ft.FontWeight.W_600, color=TEXT_DARK),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                    width=120,
                    height=80,
                    bgcolor=BG_CARD,
                    border_radius=12,
                    border=ft.border.all(2, ACCENT_WARM),
                    alignment=ft.alignment.center,
                    on_click=lambda e: select_payment("Online QR"),
                    ink=True,
                )
                
                def close_payment_dialog(e):
                    page.close(payment_dialog)
                
                def confirm_payment(e):
                    if not selected_payment[0]:
                        page.snack_bar = ft.SnackBar(
                            ft.Text("Please select a payment method!", color=ACCENT_CREAM),
                            bgcolor=ERROR,
                        )
                        page.snack_bar.open = True
                        page.update()
                        return
                    
                    # Save order to database
                    order_id = save_order(customer_name, order_type, total, confirmed_order_items)
                    
                    # Close payment dialog
                    page.close(payment_dialog)
                    
                    # Show detailed receipt
                    show_receipt(order_id, customer_name, order_type, selected_payment[0], total, confirmed_order_items.copy())
                    
                    # Clear everything
                    cart_items.clear()
                    confirmed_order_items.clear()
                    update_cart_table()
                    order_summary_column.controls = []
                    total_text.value = "₱ 0.00"
                    customer_name_field.value = ""
                    customer_display.value = "Walk-in Customer"
                    order_type_display.value = "Dine in"
                    order_type_dropdown.value = "Dine in"
                    cart_total[0] = 0
                    page.update()
                
                # Build items preview for payment dialog
                items_preview = []
                for item in confirmed_order_items:
                    items_preview.append(
                        ft.Row([
                            ft.Text(f"{item['name']} x{item['quantity']}", size=13, color=TEXT_DARK, expand=True),
                            ft.Text(f"₱{item['price'] * item['quantity']:.2f}", size=13, color=PRIMARY_MID, weight=ft.FontWeight.W_500),
                        ])
                    )
                
                payment_dialog = ft.AlertDialog(
                    modal=True,
                    title=ft.Row([
                        ft.Icon(ft.Icons.PAYMENT, color=PRIMARY_MID, size=28),
                        ft.Text("Select Payment Method", size=20, weight=ft.FontWeight.BOLD, color=PRIMARY_DARK),
                    ], spacing=10),
                    content=ft.Container(
                        content=ft.Column([
                            # QR Code Display (at top, initially hidden)
                            qr_display,
                            
                            # Order Summary
                            ft.Container(
                                content=ft.Column([
                                    ft.Row([
                                        ft.Text("Customer:", size=12, color=TEXT_LIGHT),
                                        ft.Text(customer_name, size=12, color=TEXT_DARK, weight=ft.FontWeight.W_500),
                                    ], spacing=10),
                                    ft.Row([
                                        ft.Text("Order Type:", size=12, color=TEXT_LIGHT),
                                        ft.Container(
                                            content=ft.Text(order_type, size=11, color=ACCENT_CREAM),
                                            bgcolor=PRIMARY_LIGHT,
                                            padding=ft.padding.symmetric(horizontal=8, vertical=2),
                                            border_radius=8,
                                        ),
                                    ], spacing=10),
                                ], spacing=5),
                                padding=12,
                                bgcolor=ACCENT_CREAM,
                                border_radius=8,
                            ),
                            ft.Container(height=10),
                            
                            # Items
                            ft.Text("Items:", size=13, weight=ft.FontWeight.W_600, color=TEXT_MID),
                            ft.Container(
                                content=ft.Column(items_preview, spacing=5, scroll=ft.ScrollMode.AUTO),
                                height=100 if len(items_preview) > 3 else None,
                                padding=10,
                                bgcolor=ft.Colors.with_opacity(0.3, ACCENT_CREAM),
                                border_radius=8,
                            ),
                            ft.Divider(height=15, color=ACCENT_WARM),
                            
                            # Total
                            ft.Row([
                                ft.Text("Total Amount:", size=16, weight=ft.FontWeight.BOLD, color=PRIMARY_DARK),
                                ft.Container(expand=True),
                                ft.Text(f"₱{total:.2f}", size=20, weight=ft.FontWeight.BOLD, color=SUCCESS),
                            ]),
                            ft.Container(height=15),
                            
                            # Payment Methods (only Cash and QR)
                            ft.Text("Payment Method:", size=14, weight=ft.FontWeight.W_600, color=TEXT_MID),
                            ft.Container(height=5),
                            ft.Row([cash_btn, qr_btn], spacing=20, alignment=ft.MainAxisAlignment.CENTER),
                        ], spacing=8, scroll=ft.ScrollMode.AUTO),
                        width=380,
                        padding=10,
                    ),
                    actions=[
                        ft.OutlinedButton(
                            "Cancel",
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=8),
                                side=ft.BorderSide(2, PRIMARY_MID),
                            ),
                            on_click=close_payment_dialog,
                        ),
                        ft.ElevatedButton(
                            "Confirm Payment",
                            icon=ft.Icons.CHECK_CIRCLE,
                            bgcolor=SUCCESS,
                            color=ACCENT_CREAM,
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                            on_click=confirm_payment,
                        ),
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                )
                
                page.open(payment_dialog)
            
            def generate_pdf_receipt(order_id, customer_name, order_type, payment_method, total, items, order_date, save_folder=None):
                """Generate a PDF receipt file"""
                # Use provided folder or default to last saved path
                if save_folder is None:
                    save_folder = last_save_path["path"]
                
                # Create folder if it doesn't exist
                if not os.path.exists(save_folder):
                    os.makedirs(save_folder)
                
                # Generate filename with .pdf extension
                filename = f"receipt_order_{order_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                filepath = os.path.join(save_folder, filename)
                
                # Create PDF document
                doc = SimpleDocTemplate(filepath, pagesize=letter, 
                                       rightMargin=50, leftMargin=50, 
                                       topMargin=50, bottomMargin=50)
                
                # Create styles
                styles = getSampleStyleSheet()
                title_style = ParagraphStyle(
                    'CustomTitle',
                    parent=styles['Heading1'],
                    fontSize=24,
                    alignment=1,  # Center
                    spaceAfter=6,
                    textColor=colors.HexColor('#5D4037')
                )
                subtitle_style = ParagraphStyle(
                    'CustomSubtitle',
                    parent=styles['Normal'],
                    fontSize=12,
                    alignment=1,  # Center
                    spaceAfter=20,
                    textColor=colors.HexColor('#6D4C41')
                )
                normal_style = ParagraphStyle(
                    'CustomNormal',
                    parent=styles['Normal'],
                    fontSize=11,
                    spaceAfter=3,
                    textColor=colors.HexColor('#3E2723')
                )
                footer_style = ParagraphStyle(
                    'CustomFooter',
                    parent=styles['Normal'],
                    fontSize=12,
                    alignment=1,  # Center
                    spaceBefore=20,
                    textColor=colors.HexColor('#5D4037')
                )
                
                # Build PDF elements
                elements = []
                
                # Header
                elements.append(Paragraph("☕ COFFEESTRY", title_style))
                elements.append(Paragraph("Your Cozy Coffee Shop", subtitle_style))
                
                # Order details
                elements.append(Paragraph(f"<b>Order #:</b> {order_id}", normal_style))
                elements.append(Paragraph(f"<b>Date:</b> {order_date}", normal_style))
                elements.append(Paragraph(f"<b>Customer:</b> {customer_name}", normal_style))
                elements.append(Paragraph(f"<b>Order Type:</b> {order_type}", normal_style))
                elements.append(Paragraph(f"<b>Payment:</b> {payment_method}", normal_style))
                elements.append(Spacer(1, 20))
                
                # Items table
                table_data = [['Item', 'Qty', 'Price', 'Total']]
                subtotal = 0
                for item in items:
                    item_total = item['price'] * item['quantity']
                    subtotal += item_total
                    table_data.append([
                        item['name'],
                        str(item['quantity']),
                        f"₱{item['price']:.2f}",
                        f"₱{item_total:.2f}"
                    ])
                
                # Create table with styling
                table = Table(table_data, colWidths=[2.5*inch, 0.75*inch, 1*inch, 1*inch])
                table.setStyle(TableStyle([
                    # Header row
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#5D4037')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 11),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                    ('TOPPADDING', (0, 0), (-1, 0), 10),
                    # Data rows
                    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#FFF8E1')),
                    ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#3E2723')),
                    ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
                    ('ALIGN', (0, 1), (0, -1), 'LEFT'),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
                    ('TOPPADDING', (0, 1), (-1, -1), 8),
                    # Grid
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#D4A574')),
                    # Alternating row colors
                    *[('BACKGROUND', (0, i), (-1, i), colors.HexColor('#FFECB3') if i % 2 == 0 else colors.HexColor('#FFF8E1')) 
                      for i in range(1, len(table_data))],
                ]))
                elements.append(table)
                elements.append(Spacer(1, 15))
                
                # Totals table
                totals_data = [
                    ['Subtotal:', f'₱{subtotal:.2f}'],
                    ['Tax (0%):', '₱0.00'],
                    ['TOTAL:', f'₱{total:.2f}'],
                ]
                totals_table = Table(totals_data, colWidths=[4*inch, 1.25*inch])
                totals_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                    ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                    ('FONTNAME', (0, 0), (-1, 1), 'Helvetica'),
                    ('FONTNAME', (0, 2), (-1, 2), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 11),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#3E2723')),
                    ('FONTSIZE', (0, 2), (-1, 2), 14),
                    ('TEXTCOLOR', (0, 2), (-1, 2), colors.HexColor('#5D4037')),
                    ('TOPPADDING', (0, 2), (-1, 2), 10),
                    ('LINEABOVE', (0, 2), (-1, 2), 2, colors.HexColor('#5D4037')),
                ]))
                elements.append(totals_table)
                
                # Footer
                elements.append(Spacer(1, 30))
                elements.append(Paragraph("Thank you for your purchase!", footer_style))
                elements.append(Paragraph("Visit us again soon! ☕", footer_style))
                
                # Build PDF
                doc.build(elements)
                
                return filepath
            
            def show_receipt(order_id, customer_name, order_type, payment_method, total, items):
                order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Build receipt items
                receipt_items = []
                subtotal = 0
                for item in items:
                    item_total = item['price'] * item['quantity']
                    subtotal += item_total
                    receipt_items.append(
                        ft.Container(
                            content=ft.Row([
                                ft.Container(
                                    content=ft.Text(item['category'][0], size=11, color=ACCENT_CREAM, weight=ft.FontWeight.BOLD),
                                    bgcolor=PRIMARY_LIGHT if item['category'] == "Coffee" else ACCENT_GOLD,
                                    width=26,
                                    height=26,
                                    border_radius=13,
                                    alignment=ft.alignment.center,
                                ),
                                ft.Column([
                                    ft.Text(item['name'], size=14, color=TEXT_DARK, weight=ft.FontWeight.W_500),
                                    ft.Text(f"₱{item['price']:.2f} x {item['quantity']}", size=12, color=TEXT_MID),
                                ], spacing=0, expand=True),
                                ft.Text(f"₱{item_total:.2f}", size=14, color=PRIMARY_MID, weight=ft.FontWeight.W_600),
                            ], spacing=12),
                            padding=ft.padding.symmetric(vertical=10),
                            border=ft.border.only(bottom=ft.BorderSide(1, ACCENT_CREAM)),
                        )
                    )
                
                def close_receipt(e):
                    page.close(receipt_dialog)
                
                # File picker for choosing save location
                def on_folder_selected(e: ft.FilePickerResultEvent):
                    if e.path:
                        # Update the last save path
                        last_save_path["path"] = e.path
                        try:
                            filepath = generate_pdf_receipt(order_id, customer_name, order_type, payment_method, total, items, order_date, e.path)
                            page.snack_bar = ft.SnackBar(
                                content=ft.Row([
                                    ft.Icon(ft.Icons.CHECK_CIRCLE, color=ACCENT_CREAM, size=20),
                                    ft.Text(f"Receipt saved successfully!", color=ACCENT_CREAM, weight=ft.FontWeight.W_500),
                                ], spacing=10),
                                bgcolor=SUCCESS,
                                duration=3000,
                            )
                            page.snack_bar.open = True
                            page.update()
                            
                            # Show a second notification with the file path
                            page.snack_bar = ft.SnackBar(
                                content=ft.Row([
                                    ft.Icon(ft.Icons.FOLDER_OPEN, color=ACCENT_CREAM, size=20),
                                    ft.Column([
                                        ft.Text("Saved to:", color=ACCENT_CREAM, size=11),
                                        ft.Text(filepath, color=ACCENT_CREAM, size=12, weight=ft.FontWeight.W_500),
                                    ], spacing=0, expand=True),
                                ], spacing=10),
                                bgcolor=PRIMARY_MID,
                                duration=5000,
                            )
                            page.snack_bar.open = True
                            page.update()
                        except Exception as ex:
                            page.snack_bar = ft.SnackBar(
                                content=ft.Row([
                                    ft.Icon(ft.Icons.ERROR, color=ACCENT_CREAM, size=20),
                                    ft.Text(f"Error saving receipt: {str(ex)}", color=ACCENT_CREAM),
                                ], spacing=10),
                                bgcolor=ERROR,
                                duration=4000,
                            )
                            page.snack_bar.open = True
                            page.update()
                
                folder_picker = ft.FilePicker(on_result=on_folder_selected)
                page.overlay.append(folder_picker)
                page.update()
                
                def save_receipt_pdf(e):
                    # Open folder picker dialog with last save path as initial directory
                    folder_picker.get_directory_path(
                        dialog_title="Choose where to save the receipt",
                        initial_directory=last_save_path["path"]
                    )
                
                # Get payment icon
                payment_icon = ft.Icons.MONEY if payment_method == "Cash" else ft.Icons.QR_CODE
                
                receipt_dialog = ft.AlertDialog(
                    modal=True,
                    title=ft.Row([
                        ft.Icon(ft.Icons.RECEIPT_LONG, color=PRIMARY_MID, size=28),
                        ft.Column([
                            ft.Text(f"Order #{order_id}", size=20, weight=ft.FontWeight.BOLD, color=PRIMARY_DARK),
                            ft.Text("Payment Successful!", size=12, color=SUCCESS, weight=ft.FontWeight.W_500),
                        ], spacing=0, expand=True),
                        ft.Icon(ft.Icons.CHECK_CIRCLE, color=SUCCESS, size=32),
                    ], spacing=10),
                    content=ft.Container(
                        content=ft.Column([
                            # Store Header
                            ft.Container(
                                content=ft.Column([
                                    ft.Row([
                                        ft.Icon(ft.Icons.LOCAL_CAFE, color=ACCENT_WARM, size=24),
                                        ft.Text("COFFEESTRY", size=18, weight=ft.FontWeight.BOLD, color=PRIMARY_DARK),
                                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                                    ft.Text("Your Cozy Coffee Shop", size=11, color=TEXT_MID, italic=True),
                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                                padding=12,
                                bgcolor=ACCENT_CREAM,
                                border_radius=10,
                            ),
                            ft.Container(height=10),
                            
                            # Customer & Order Info
                            ft.Container(
                                content=ft.Column([
                                    ft.Row([
                                        ft.Icon(ft.Icons.PERSON_OUTLINE, size=16, color=TEXT_MID),
                                        ft.Text("Customer:", size=12, color=TEXT_LIGHT),
                                        ft.Text(customer_name, size=12, color=TEXT_DARK, weight=ft.FontWeight.W_500),
                                    ], spacing=8),
                                    ft.Row([
                                        ft.Icon(ft.Icons.RESTAURANT, size=16, color=TEXT_MID),
                                        ft.Text("Type:", size=12, color=TEXT_LIGHT),
                                        ft.Container(
                                            content=ft.Text(order_type, size=11, color=ACCENT_CREAM),
                                            bgcolor=PRIMARY_LIGHT if order_type == "Dine in" else ACCENT_GOLD,
                                            padding=ft.padding.symmetric(horizontal=10, vertical=3),
                                            border_radius=10,
                                        ),
                                    ], spacing=8),
                                    ft.Row([
                                        ft.Icon(ft.Icons.CALENDAR_TODAY, size=16, color=TEXT_MID),
                                        ft.Text("Date:", size=12, color=TEXT_LIGHT),
                                        ft.Text(order_date, size=12, color=TEXT_DARK),
                                    ], spacing=8),
                                    ft.Row([
                                        ft.Icon(payment_icon, size=16, color=TEXT_MID),
                                        ft.Text("Payment:", size=12, color=TEXT_LIGHT),
                                        ft.Container(
                                            content=ft.Text(payment_method, size=11, color=ACCENT_CREAM),
                                            bgcolor=SUCCESS,
                                            padding=ft.padding.symmetric(horizontal=10, vertical=3),
                                            border_radius=10,
                                        ),
                                    ], spacing=8),
                                ], spacing=8),
                                padding=15,
                                bgcolor=BG_LIGHT,
                                border_radius=10,
                                border=ft.border.all(1, ACCENT_CREAM),
                            ),
                            ft.Container(height=10),
                            
                            # Order Items Header
                            ft.Text("Order Items:", size=14, weight=ft.FontWeight.W_600, color=TEXT_MID),
                            
                            # Items List
                            ft.Container(
                                content=ft.Column(receipt_items, spacing=0, scroll=ft.ScrollMode.AUTO),
                                height=180 if len(receipt_items) > 4 else None,
                                padding=10,
                                bgcolor=BG_CARD,
                                border_radius=10,
                                border=ft.border.all(1, ACCENT_CREAM),
                            ),
                            
                            # Totals Section
                            ft.Container(
                                content=ft.Column([
                                    ft.Row([
                                        ft.Text("Subtotal:", size=13, color=TEXT_MID),
                                        ft.Container(expand=True),
                                        ft.Text(f"₱{subtotal:.2f}", size=13, color=TEXT_DARK),
                                    ]),
                                    ft.Row([
                                        ft.Text("Tax (0%):", size=13, color=TEXT_MID),
                                        ft.Container(expand=True),
                                        ft.Text("₱0.00", size=13, color=TEXT_DARK),
                                    ]),
                                    ft.Divider(height=10, color=ACCENT_WARM),
                                    ft.Row([
                                        ft.Text("Total:", size=18, weight=ft.FontWeight.BOLD, color=PRIMARY_DARK),
                                        ft.Container(expand=True),
                                        ft.Text(f"₱{total:.2f}", size=22, weight=ft.FontWeight.BOLD, color=SUCCESS),
                                    ]),
                                ], spacing=5),
                                padding=15,
                                bgcolor=ft.Colors.with_opacity(0.5, ACCENT_CREAM),
                                border_radius=10,
                            ),
                            
                            # Thank You Message
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Thank you for your purchase!", size=14, weight=ft.FontWeight.W_600, color=PRIMARY_DARK),
                                    ft.Text("Visit us again soon! ☕", size=12, color=TEXT_MID),
                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=3),
                                padding=10,
                                alignment=ft.alignment.center,
                            ),
                        ], spacing=8, scroll=ft.ScrollMode.AUTO),
                        width=420,
                        height=520,
                        padding=10,
                    ),
                    actions=[
                        ft.ElevatedButton(
                            "Save Receipt",
                            icon=ft.Icons.SAVE_ALT,
                            bgcolor=PRIMARY_MID,
                            color=ACCENT_CREAM,
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                            on_click=save_receipt_pdf,
                        ),
                        ft.ElevatedButton(
                            "Done",
                            icon=ft.Icons.CHECK,
                            bgcolor=SUCCESS,
                            color=ACCENT_CREAM,
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                            on_click=close_receipt,
                        ),
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                )
                
                page.open(receipt_dialog)

            # Product Table Container (will be updated by search/filter)
            product_table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Product", weight=ft.FontWeight.W_600, color=PRIMARY_DARK)),
                    ft.DataColumn(ft.Text("Category", weight=ft.FontWeight.W_600, color=PRIMARY_DARK)),
                    ft.DataColumn(ft.Text("Price", weight=ft.FontWeight.W_600, color=PRIMARY_DARK)),
                    ft.DataColumn(ft.Text("Qty", weight=ft.FontWeight.W_600, color=PRIMARY_DARK)),
                ],
                rows=[],
                border=ft.border.all(1, ACCENT_WARM),
                border_radius=10,
                heading_row_color=ACCENT_CREAM,
                data_row_color={ft.ControlState.HOVERED: ft.Colors.with_opacity(0.1, ACCENT_WARM)},
            )

            # Function to build product rows with working buttons
            def build_product_rows(filtered_products):
                rows = []
                for product in filtered_products:
                    qty_text = ft.Text(value="1", size=14, width=35, text_align=ft.TextAlign.CENTER, color=TEXT_DARK)

                    def make_decrease_qty(qt):
                        def decrease_qty(e):
                            qty = int(qt.value)
                            if qty > 1:
                                qt.value = str(qty - 1)
                                page.update()
                        return decrease_qty

                    def make_increase_qty(qt):
                        def increase_qty(e):
                            qt.value = str(int(qt.value) + 1)
                            page.update()
                        return increase_qty

                    def make_add_to_cart(prod, qt):
                        def add_to_cart(e):
                            qty = int(qt.value)
                            # Check if product already in cart
                            for item in cart_items:
                                if item["name"] == prod["name"]:
                                    item["quantity"] += qty
                                    update_cart_table()
                                    qt.value = "1"
                                    page.snack_bar = ft.SnackBar(
                                        ft.Text(f"Added {qty}x {prod['name']} to cart!", color=ACCENT_CREAM),
                                        bgcolor=SUCCESS,
                                        duration=1500,
                                    )
                                    page.snack_bar.open = True
                                    page.update()
                                    return
                            cart_items.append({
                                "name": prod["name"],
                                "category": prod["category"],
                                "price": prod["price"],
                                "quantity": qty
                            })
                            update_cart_table()
                            qt.value = "1"
                            page.snack_bar = ft.SnackBar(
                                ft.Text(f"Added {qty}x {prod['name']} to cart!", color=ACCENT_CREAM),
                                bgcolor=SUCCESS,
                                duration=1500,
                            )
                            page.snack_bar.open = True
                            page.update()
                        return add_to_cart

                    def make_quick_order(prod, qt):
                        def quick_order(e):
                            qty = int(qt.value)
                            # Clear cart and add only this product
                            cart_items.clear()
                            cart_items.append({
                                "name": prod["name"],
                                "category": prod["category"],
                                "price": prod["price"],
                                "quantity": qty
                            })
                            update_cart_table()
                            # Auto confirm the order
                            customer_name = customer_name_field.value if customer_name_field.value else "Walk-in Customer"
                            customer_display.value = customer_name
                            order_type_display.value = order_type_dropdown.value
                            
                            # Build order summary
                            total = prod["price"] * qty
                            order_summary_column.controls = [
                                ft.Container(
                                    content=ft.Row(
                                        [
                                            ft.Text(f"{prod['name']} x{qty}", size=14, color=TEXT_DARK, expand=True),
                                            ft.Text(f"₱{total:.2f}", size=14, weight=ft.FontWeight.W_500, color=PRIMARY_MID),
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    ),
                                    padding=ft.padding.symmetric(vertical=5, horizontal=10),
                                    bgcolor=ACCENT_CREAM,
                                    border_radius=5,
                                )
                            ]
                            total_text.value = f"₱ {total:.2f}"
                            qt.value = "1"
                            
                            page.snack_bar = ft.SnackBar(
                                ft.Text(f"Order confirmed! {qty}x {prod['name']} - ₱{total:.2f}", color=ACCENT_CREAM),
                                bgcolor=PRIMARY_MID,
                                duration=2000,
                            )
                            page.snack_bar.open = True
                            page.update()
                        return quick_order

                    rows.append(
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text(product["name"], color=TEXT_DARK, weight=ft.FontWeight.W_500)),
                            ft.DataCell(
                                ft.Container(
                                    content=ft.Text(product["category"], size=12, color=ACCENT_CREAM),
                                    bgcolor=PRIMARY_LIGHT if product["category"] == "Coffee" else ACCENT_GOLD,
                                    padding=ft.padding.symmetric(horizontal=10, vertical=3),
                                    border_radius=12,
                                )
                            ),
                            ft.DataCell(ft.Text(f"₱{product['price']:.2f}", color=TEXT_DARK, weight=ft.FontWeight.W_500)),
                            ft.DataCell(
                                ft.Row([
                                    ft.IconButton(ft.Icons.REMOVE_CIRCLE_OUTLINE, on_click=make_decrease_qty(qty_text), icon_color=PRIMARY_MID, icon_size=20),
                                    qty_text,
                                    ft.IconButton(ft.Icons.ADD_CIRCLE_OUTLINE, on_click=make_increase_qty(qty_text), icon_color=PRIMARY_MID, icon_size=20),
                                    ft.Container(width=10),
                                    ft.Container(
                                        content=ft.IconButton(
                                            ft.Icons.ADD_SHOPPING_CART_ROUNDED,
                                            icon_color=ACCENT_CREAM,
                                            icon_size=22,
                                            on_click=make_add_to_cart(product, qty_text),
                                            tooltip="Add to Cart",
                                        ),
                                        bgcolor=SUCCESS,
                                        border_radius=8,
                                        padding=2,
                                    ),
                                ], alignment=ft.MainAxisAlignment.CENTER, spacing=0)
                            ),
                        ])
                    )
                return rows

            # Search and filter function
            def filter_products(e=None):
                # Reload products from database to get latest
                nonlocal dashboard_products
                dashboard_products = load_dashboard_products()
                
                search_text = search_field.value.lower() if search_field.value else ""
                selected_category = category_dropdown.value if category_dropdown.value and category_dropdown.value != "All" else None
                
                filtered = []
                for product in dashboard_products:
                    # Check search text
                    if search_text and search_text not in product["name"].lower():
                        continue
                    # Check category
                    if selected_category and product["category"] != selected_category:
                        continue
                    filtered.append(product)
                
                product_table.rows = build_product_rows(filtered)
                page.update()

            # Search and Category Filter
            search_field = ft.TextField(
                hint_text="Search Product...",
                color=TEXT_DARK,
                bgcolor=BG_CARD,
                border_color=ACCENT_WARM,
                focused_border_color=PRIMARY_MID,
                border_radius=8,
                width=200,
                prefix_icon=ft.Icons.SEARCH,
                on_change=filter_products,
            )
            
            category_dropdown = ft.Dropdown(
                width=180,
                border_color=ACCENT_WARM,
                focused_border_color=PRIMARY_MID,
                border_radius=8,
                hint_text="All Categories",
                bgcolor=BG_CARD,
                color=TEXT_DARK,
                value="All",
                options=[
                    ft.dropdown.Option("All"),
                    ft.dropdown.Option("Coffee"),
                    ft.dropdown.Option("Pastry"),
                ],
                on_change=filter_products,
            )

            # Initialize product table with all products from database
            product_table.rows = build_product_rows(dashboard_products)

            # Main Making Orders Panel
            making_orders_panel = ft.Container(
                bgcolor=BG_CARD,
                padding=25,
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
                                ft.Icon(ft.Icons.SHOPPING_BAG, size=28, color=PRIMARY_MID),
                                ft.Text("Making Orders", size=22, weight=ft.FontWeight.BOLD, color=PRIMARY_DARK),
                            ],
                            spacing=10,
                        ),
                        ft.Divider(height=20, color=ACCENT_CREAM, thickness=2),
                        
                        # Customer Info Row
                        ft.Row(
                            [
                                ft.Column([
                                    ft.Text("Customer Name", size=13, color=TEXT_MID, weight=ft.FontWeight.W_500),
                                    customer_name_field,
                                ], spacing=5),
                                ft.Column([
                                    ft.Text("Order Date", size=13, color=TEXT_MID, weight=ft.FontWeight.W_500),
                                    order_date_field,
                                ], spacing=5),
                                ft.Column([
                                    ft.Text("Order Type", size=13, color=TEXT_MID, weight=ft.FontWeight.W_500),
                                    order_type_dropdown,
                                ], spacing=5),
                            ],
                            spacing=30,
                            wrap=True,
                        ),
                        
                        ft.Container(height=15),
                        
                        # Product List Section
                        ft.Container(
                            content=ft.Column([
                                ft.Row(
                                    [
                                        ft.Text("Product List", size=16, weight=ft.FontWeight.W_600, color=PRIMARY_DARK),
                                        ft.Container(expand=True),
                                        search_field,
                                        category_dropdown,
                                    ],
                                    alignment=ft.MainAxisAlignment.START,
                                    spacing=15,
                                ),
                                ft.Container(height=10),
                                ft.Container(
                                    content=product_table,
                                    border_radius=10,
                                ),
                            ]),
                            bgcolor=ft.Colors.with_opacity(0.3, ACCENT_CREAM),
                            padding=15,
                            border_radius=10,
                        ),
                        
                        ft.Container(height=15),
                        
                        # Cart Section
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Icon(ft.Icons.SHOPPING_CART, size=20, color=PRIMARY_MID),
                                    ft.Text("Cart", size=16, weight=ft.FontWeight.W_600, color=PRIMARY_DARK),
                                    ft.Container(expand=True),
                                    ft.OutlinedButton(
                                        "Clear Cart",
                                        icon=ft.Icons.DELETE_SWEEP,
                                        on_click=clear_cart,
                                        style=ft.ButtonStyle(
                                            color=ERROR,
                                            side=ft.BorderSide(1, ERROR),
                                            shape=ft.RoundedRectangleBorder(radius=8),
                                        ),
                                    ),
                                    ft.ElevatedButton(
                                        "Confirm Order",
                                        icon=ft.Icons.CHECK_CIRCLE,
                                        on_click=confirm_order,
                                        bgcolor=SUCCESS,
                                        color=ACCENT_CREAM,
                                        style=ft.ButtonStyle(
                                            shape=ft.RoundedRectangleBorder(radius=8),
                                            elevation=2,
                                        ),
                                    ),
                                ], spacing=10),
                                ft.Container(height=10),
                                cart_table,
                            ]),
                            bgcolor=ft.Colors.with_opacity(0.3, ACCENT_CREAM),
                            padding=15,
                            border_radius=10,
                        ),
                    ],
                    spacing=10,
                    scroll=ft.ScrollMode.AUTO,
                ),
                expand=True,
            )

            # Order Details Panel (Right Side)
            order_details_panel = ft.Container(
                bgcolor=BG_CARD,
                padding=25,
                border_radius=15,
                width=320,
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
                                ft.Icon(ft.Icons.RECEIPT_LONG, size=24, color=PRIMARY_MID),
                                ft.Text("Order Details", size=18, weight=ft.FontWeight.BOLD, color=PRIMARY_DARK),
                            ],
                            spacing=10,
                        ),
                        ft.Divider(height=15, color=ACCENT_CREAM, thickness=2),
                        
                        # Customer Info Display
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Icon(ft.Icons.PERSON_OUTLINE, size=16, color=TEXT_MID),
                                    ft.Text("Customer:", size=12, color=TEXT_MID),
                                ], spacing=5),
                                customer_display,
                            ], spacing=2),
                            bgcolor=ACCENT_CREAM,
                            padding=12,
                            border_radius=8,
                        ),
                        
                        ft.Container(height=10),
                        
                        # Order Type Display
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Icon(ft.Icons.RESTAURANT, size=16, color=TEXT_MID),
                                    ft.Text("Order Type:", size=12, color=TEXT_MID),
                                ], spacing=5),
                                order_type_display,
                            ], spacing=2),
                            bgcolor=ACCENT_CREAM,
                            padding=12,
                            border_radius=8,
                        ),
                        
                        ft.Container(height=15),
                        
                        # Items Summary (Scrollable)
                        ft.Text("Items Summary", size=14, weight=ft.FontWeight.W_600, color=TEXT_MID),
                        ft.Container(
                            content=ft.Column(
                                [order_summary_column],
                                scroll=ft.ScrollMode.AUTO,
                                expand=True,
                            ),
                            bgcolor=ft.Colors.with_opacity(0.5, ACCENT_CREAM),
                            padding=10,
                            border_radius=8,
                            height=200,
                            expand=True,
                        ),
                        
                        # Total Section
                        ft.Divider(height=20, color=ACCENT_WARM, thickness=1),
                        ft.Row(
                            [
                                ft.Text("Total:", size=18, weight=ft.FontWeight.W_600, color=TEXT_MID),
                                total_text,
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        
                        ft.Container(height=15),
                        
                        # Proceed to Payment Button
                        ft.ElevatedButton(
                            "Proceed to Payment",
                            icon=ft.Icons.PAYMENT,
                            bgcolor=PRIMARY_MID,
                            color=ACCENT_CREAM,
                            width=270,
                            height=50,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=12),
                                elevation=3,
                            ),
                            on_click=proceed_to_payment,
                        ),
                    ],
                    spacing=8,
                    scroll=ft.ScrollMode.AUTO,
                ),
            )

            # Main Layout with Order Panel and Order Details
            dashboard_view = ft.Row(
                [
                    making_orders_panel,
                    order_details_panel,
                ],
                spacing=20,
                expand=True,
            )

            main_content.content = ft.Container(
                padding=20,
                bgcolor=BG_LIGHT,
                content=dashboard_view,
                expand=True,
            )
            page.update()


  
 # PRODUCT MANAGEMENT
        def layout6():
            
            selected_product = [None]  # Use list for mutability
       
            # Load products from database for this business owner
            def load_products_from_db():
                db_products = get_products(current_user_id)  # Returns list of tuples (id, name, category, price)
                return [{"id": p[0], "name": p[1], "category": p[2], "price": p[3]} for p in db_products]
            
            products_list = load_products_from_db()
            
            # Search products        
            search_field = ft.TextField(
                hint_text="Search products...",
                prefix_icon=ft.Icons.SEARCH,
                width=350,
                bgcolor=BG_CARD,
                color=TEXT_DARK,
                border_color=ACCENT_WARM,
                focused_border_color=PRIMARY_MID,
                border_radius=10,
                on_change=lambda e: layout7()
            )
         
            def layout7():  # for refreshing the product list
                nonlocal products_list
                products_list = load_products_from_db()  # Reload from database
                main_content.content = layout8()
                page.update()
    
        
            # ADD PRODUCT DIALOG
            def layout8():
                query = search_field.value.lower() if search_field.value else ""
                
                filtered = [
                    p for p in products_list
                    if query in p["name"].lower()
                    or query in p["category"].lower()
                    or query in str(p["price"])
                ]
                
                table_rows = []
                for p in filtered:
                    table_rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(p["name"], color=TEXT_DARK)),
                                ft.DataCell(
                                    ft.Container(
                                        content=ft.Text(p["category"], size=12, color=ACCENT_CREAM),
                                        bgcolor=PRIMARY_LIGHT if p["category"] == "Coffee" else ACCENT_GOLD,
                                        padding=ft.padding.symmetric(horizontal=10, vertical=3),
                                        border_radius=12,
                                    )
                                ),
                                ft.DataCell(ft.Text(f"₱{p['price']:.2f}", color=TEXT_DARK, weight=ft.FontWeight.W_500)),
                                ft.DataCell(
                                    ft.Row([
                                        ft.IconButton(
                                            ft.Icons.EDIT,
                                            icon_color=PRIMARY_MID,
                                            on_click=lambda e, prod=p: open_edit(prod)
                                        ),
                                        ft.IconButton(
                                            ft.Icons.DELETE,
                                            icon_color=ERROR,
                                            on_click=lambda e, prod=p: delete_prod(prod)
                                        ),
                                    ])
                                )
                            ]
                        )   
                    )
                    
                # UI LAYOUT FOR PRODUCT TABLE
                return ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Icon(ft.Icons.INVENTORY_2, size=28, color=PRIMARY_MID),
                                    ft.Text("Product and Price Management", size=22, weight=ft.FontWeight.BOLD, color=PRIMARY_DARK),
                                ],
                                spacing=10,
                            ),
                            ft.Divider(height=20, color=ACCENT_CREAM, thickness=2),
                            ft.Row(
                                [
                                    search_field,
                                    ft.Container(expand=True),
                                    ft.ElevatedButton(
                                        "Add Product",
                                        icon=ft.Icons.ADD_CIRCLE,
                                        bgcolor=PRIMARY_MID,
                                        color=ACCENT_CREAM,
                                        style=ft.ButtonStyle(
                                            shape=ft.RoundedRectangleBorder(radius=10),
                                            elevation=2,
                                        ),
                                        on_click=open_add,
                                    ),
                                ],
                                spacing=15,
                            ),
                            ft.Container(height=15),
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.DataTable(
                                            columns=[
                                                ft.DataColumn(ft.Text("Product Name", weight=ft.FontWeight.W_600, color=PRIMARY_DARK)),
                                                ft.DataColumn(ft.Text("Category", weight=ft.FontWeight.W_600, color=PRIMARY_DARK)),
                                                ft.DataColumn(ft.Text("Price (₱)", weight=ft.FontWeight.W_600, color=PRIMARY_DARK)),
                                                ft.DataColumn(ft.Text("Actions", weight=ft.FontWeight.W_600, color=PRIMARY_DARK)),
                                            ],
                                            rows=table_rows,
                                            border=ft.border.all(1, ACCENT_WARM),
                                            border_radius=10,
                                            heading_row_color=ACCENT_CREAM,
                                            data_row_color={ft.ControlState.HOVERED: ft.Colors.with_opacity(0.1, ACCENT_WARM)},
                                        ),
                                    ],
                                    scroll=ft.ScrollMode.AUTO,
                                    expand=True,
                                ),
                                bgcolor=BG_CARD,
                                padding=20,
                                border_radius=15,
                                expand=True,
                                shadow=ft.BoxShadow(
                                    color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                                    blur_radius=15,
                                    offset=ft.Offset(0, 4)
                                ),
                            )
                        ],
                        expand=True,
                        scroll=ft.ScrollMode.AUTO,
                    ),
                    padding=20,
                    bgcolor=BG_LIGHT,
                    expand=True,
                )
                                          
            # ICON FOR ADD PRODUCT
            def open_add(e):
                selected_product[0] = None
                main_content.content = layout_add_edit()
                page.update()
                
            # Editing the product            
            def open_edit(product):
                selected_product[0] = product
                main_content.content = layout_add_edit(product)
                page.update()
                
            # Deleting product                
            def delete_prod(product):
                delete_product(product["id"])  # Delete from database
                page.snack_bar = ft.SnackBar(
                    ft.Text(f"Product '{product['name']}' deleted!", color=ACCENT_CREAM),
                    bgcolor=ERROR,
                )
                page.snack_bar.open = True
                layout7()
                
            def save_product_handler(e, name_field, category_field, price_field):
                name = name_field.value
                category = category_field.value
                
                if not name or not category or not price_field.value:
                    page.snack_bar = ft.SnackBar(
                        ft.Text("Please fill in all fields!", color=ACCENT_CREAM),
                        bgcolor=ERROR,
                    )
                    page.snack_bar.open = True
                    page.update()
                    return
                    
                try:
                    price = float(price_field.value)
                except ValueError:
                    page.snack_bar = ft.SnackBar(
                        ft.Text("Invalid price format!", color=ACCENT_CREAM),
                        bgcolor=ERROR,
                    )
                    page.snack_bar.open = True
                    page.update()
                    return
                
                if selected_product[0] is None:
                    # Add new product to database for this business owner
                    add_product(name, category, price, current_user_id)
                    page.snack_bar = ft.SnackBar(
                        ft.Text(f"Product '{name}' added successfully!", color=ACCENT_CREAM),
                        bgcolor=SUCCESS,
                    )
                else:
                    # Update existing product in database
                    update_product(selected_product[0]["id"], name, category, price)
                    page.snack_bar = ft.SnackBar(
                        ft.Text(f"Product '{name}' updated successfully!", color=ACCENT_CREAM),
                        bgcolor=SUCCESS,
                    )
                
                page.snack_bar.open = True
                # Reload products and go back to list view
                nonlocal products_list
                products_list = load_products_from_db()
                main_content.content = layout8()
                page.update()
                
            def layout_add_edit(prod=None):
                
                name_field = ft.TextField(
                    label="Product Name", width=350, color=TEXT_DARK,
                    border_color=ACCENT_WARM, focused_border_color=PRIMARY_MID,
                    label_style=ft.TextStyle(color=TEXT_MID),
                    border_radius=10,
                    value=prod["name"] if prod else ""
                )
                category_field = ft.Dropdown(
                    label="Category", width=350, color=TEXT_DARK,
                    border_color=ACCENT_WARM, focused_border_color=PRIMARY_MID,
                    label_style=ft.TextStyle(color=TEXT_MID),
                    border_radius=10,
                    value=prod["category"] if prod else None,
                    options=[
                        ft.dropdown.Option("Coffee"),
                        ft.dropdown.Option("Pastry"),
                    ]
                )
                price_field = ft.TextField(
                    label="Price (₱)", width=350, color=TEXT_DARK,
                    border_color=ACCENT_WARM, focused_border_color=PRIMARY_MID,
                    label_style=ft.TextStyle(color=TEXT_MID),
                    border_radius=10,
                    value=str(prod["price"]) if prod else ""
                )
                
                # Build product list rows for the sidebar
                product_list_rows = []
                for p in products_list:
                    product_list_rows.append(
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.Container(
                                        content=ft.Text(p["category"][0], size=12, color=ACCENT_CREAM, weight=ft.FontWeight.BOLD),
                                        bgcolor=PRIMARY_LIGHT if p["category"] == "Coffee" else ACCENT_GOLD,
                                        width=28,
                                        height=28,
                                        border_radius=14,
                                        alignment=ft.alignment.center,
                                    ),
                                    ft.Column(
                                        [
                                            ft.Text(p["name"], size=13, color=TEXT_DARK, weight=ft.FontWeight.W_500),
                                            ft.Text(f"₱{p['price']:.2f}", size=11, color=TEXT_MID),
                                        ],
                                        spacing=0,
                                        expand=True,
                                    ),
                                ],
                                spacing=10,
                            ),
                            padding=ft.padding.symmetric(horizontal=10, vertical=8),
                            border=ft.border.only(bottom=ft.BorderSide(1, ACCENT_CREAM)),
                        )
                    )
                
                return ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Icon(ft.Icons.INVENTORY_2, size=28, color=PRIMARY_MID),
                                    ft.Text("Product and Price Management", size=22, weight=ft.FontWeight.BOLD, color=PRIMARY_DARK),
                                ],
                                spacing=10,
                            ),
                            ft.Divider(height=20, color=ACCENT_CREAM, thickness=2),
                            
                            ft.Row(
                                [
                                    # Add/Edit Form
                                    ft.Container(
                                        content=ft.Column(
                                            [
                                                ft.Text(
                                                    "Edit Product" if prod else "Add New Product",
                                                    size=18, weight=ft.FontWeight.W_600, color=PRIMARY_DARK
                                                ),
                                                ft.Container(height=10),
                                                name_field,
                                                category_field,
                                                price_field,
                                                ft.Container(height=15),
                                                ft.Row(
                                                    [
                                                        ft.OutlinedButton(
                                                            "Cancel",
                                                            style=ft.ButtonStyle(
                                                                shape=ft.RoundedRectangleBorder(radius=10),
                                                                side=ft.BorderSide(2, PRIMARY_MID),
                                                            ),
                                                            on_click=lambda e: back_to_list()
                                                        ),
                                                        ft.ElevatedButton(
                                                            "Save Product",
                                                            icon=ft.Icons.SAVE,
                                                            bgcolor=PRIMARY_MID,
                                                            color=ACCENT_CREAM,
                                                            style=ft.ButtonStyle(
                                                                shape=ft.RoundedRectangleBorder(radius=10),
                                                                elevation=2,
                                                            ),
                                                            on_click=lambda e: save_product_handler(e, name_field, category_field, price_field)
                                                        ),
                                                    ],
                                                    spacing=20
                                                )
                                            ],
                                            spacing=15
                                        ),
                                        padding=30,
                                        bgcolor=BG_CARD,
                                        border_radius=15,
                                        shadow=ft.BoxShadow(
                                            color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                                            blur_radius=15,
                                            offset=ft.Offset(0, 4)
                                        ),
                                        width=450
                                    ),
                                    
                                    # Product List Panel
                                    ft.Container(
                                        content=ft.Column(
                                            [
                                                ft.Row(
                                                    [
                                                        ft.Icon(ft.Icons.LIST_ALT, size=20, color=PRIMARY_MID),
                                                        ft.Text("Current Products", size=16, weight=ft.FontWeight.W_600, color=PRIMARY_DARK),
                                                        ft.Container(expand=True),
                                                        ft.Text(f"{len(products_list)} items", size=12, color=TEXT_LIGHT),
                                                    ],
                                                    spacing=8,
                                                ),
                                                ft.Divider(height=10, color=ACCENT_CREAM),
                                                ft.Container(
                                                    content=ft.Column(
                                                        product_list_rows if product_list_rows else [
                                                            ft.Container(
                                                                content=ft.Text("No products yet", size=14, color=TEXT_LIGHT, italic=True),
                                                                padding=20,
                                                                alignment=ft.alignment.center,
                                                            )
                                                        ],
                                                        spacing=0,
                                                        scroll=ft.ScrollMode.AUTO,
                                                    ),
                                                    height=350,
                                                ),
                                            ],
                                            spacing=5,
                                        ),
                                        padding=20,
                                        bgcolor=BG_CARD,
                                        border_radius=15,
                                        shadow=ft.BoxShadow(
                                            color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                                            blur_radius=15,
                                            offset=ft.Offset(0, 4)
                                        ),
                                        width=350,
                                    ),
                                ],
                                spacing=30,
                                alignment=ft.MainAxisAlignment.START,
                            ),
                        ],
                        expand=True
                    ),
                    padding=20,
                    bgcolor=BG_LIGHT,
                    expand=True,
                )
                    
            def back_to_list():
                layout7()
            
            layout7()

        # ORDER HISTORY PAGE
        def layout_order_history():
            orders = get_all_orders()  # Get orders from database
            
            def refresh_orders():
                layout_order_history()
            
            def confirm_order_clicked(order_id):
                confirm_order(order_id)
                page.snack_bar = ft.SnackBar(
                    content=ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE, color=ACCENT_CREAM), ft.Text("Order confirmed!", color=ACCENT_CREAM)], spacing=10),
                    bgcolor=SUCCESS
                )
                page.snack_bar.open = True
                refresh_orders()
            
            def mark_paid_clicked(order_id):
                mark_order_paid(order_id)
                page.snack_bar = ft.SnackBar(
                    content=ft.Row([ft.Icon(ft.Icons.PAYMENTS, color=ACCENT_CREAM), ft.Text("Payment confirmed!", color=ACCENT_CREAM)], spacing=10),
                    bgcolor=SUCCESS
                )
                page.snack_bar.open = True
                refresh_orders()
            
            def complete_order_clicked(order_id):
                complete_order(order_id)
                page.snack_bar = ft.SnackBar(
                    content=ft.Row([ft.Icon(ft.Icons.DONE_ALL, color=ACCENT_CREAM), ft.Text("Order completed!", color=ACCENT_CREAM)], spacing=10),
                    bgcolor=SUCCESS
                )
                page.snack_bar.open = True
                refresh_orders()
            
            def cancel_order_clicked(order_id):
                def confirm_cancel(e):
                    cancel_order(order_id)
                    page.close(cancel_dialog)
                    page.snack_bar = ft.SnackBar(
                        content=ft.Row([ft.Icon(ft.Icons.CANCEL, color=ACCENT_CREAM), ft.Text("Order cancelled!", color=ACCENT_CREAM)], spacing=10),
                        bgcolor=ERROR
                    )
                    page.snack_bar.open = True
                    refresh_orders()
                
                cancel_dialog = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("Cancel Order", color=ERROR, weight=ft.FontWeight.BOLD),
                    content=ft.Text("Are you sure you want to cancel this order?"),
                    actions=[
                        ft.TextButton("No", on_click=lambda e: page.close(cancel_dialog)),
                        ft.ElevatedButton("Yes, Cancel", bgcolor=ERROR, color=ACCENT_CREAM, on_click=confirm_cancel),
                    ],
                )
                page.open(cancel_dialog)
            
            def print_receipt_clicked(order_id):
                # Get order info
                order_info = None
                for o in orders:
                    if o[0] == order_id:
                        order_info = o
                        break
                
                if not order_info:
                    page.snack_bar = ft.SnackBar(
                        content=ft.Row([ft.Icon(ft.Icons.ERROR, color=ACCENT_CREAM), ft.Text("Order not found!", color=ACCENT_CREAM)], spacing=10),
                        bgcolor=ERROR
                    )
                    page.snack_bar.open = True
                    page.update()
                    return
                
                # Get order items
                items = get_order_items(order_id)
                
                # Prepare items in the format expected by generate_pdf_receipt
                items_list = []
                for item in items:
                    # item = (product_name, category, price, quantity)
                    items_list.append({
                        'name': item[0],
                        'category': item[1],
                        'price': item[2],
                        'quantity': item[3]
                    })
                
                customer_name = order_info[1] if order_info[1] else "Walk-in"
                order_type = order_info[2] if order_info[2] else "Dine in"
                total = order_info[3]
                order_date = str(order_info[4])[:19] if order_info[4] else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                payment_status = order_info[6] if len(order_info) > 6 and order_info[6] else "unpaid"
                payment_method = "Paid" if payment_status == "paid" else "Unpaid"
                
                # File picker for choosing save location
                def on_folder_selected(e: ft.FilePickerResultEvent):
                    if e.path:
                        last_save_path["path"] = e.path
                        try:
                            # Generate PDF receipt
                            save_folder = e.path
                            if not os.path.exists(save_folder):
                                os.makedirs(save_folder)
                            
                            filename = f"receipt_order_{order_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                            filepath = os.path.join(save_folder, filename)
                            
                            # Create PDF document
                            doc = SimpleDocTemplate(filepath, pagesize=letter, 
                                                   rightMargin=50, leftMargin=50, 
                                                   topMargin=50, bottomMargin=50)
                            
                            # Create styles
                            styles = getSampleStyleSheet()
                            title_style = ParagraphStyle(
                                'CustomTitle',
                                parent=styles['Heading1'],
                                fontSize=24,
                                alignment=1,
                                spaceAfter=6,
                                textColor=colors.HexColor('#5D4037')
                            )
                            subtitle_style = ParagraphStyle(
                                'CustomSubtitle',
                                parent=styles['Normal'],
                                fontSize=12,
                                alignment=1,
                                spaceAfter=20,
                                textColor=colors.HexColor('#6D4C41')
                            )
                            normal_style = ParagraphStyle(
                                'CustomNormal',
                                parent=styles['Normal'],
                                fontSize=11,
                                spaceAfter=3,
                                textColor=colors.HexColor('#3E2723')
                            )
                            footer_style = ParagraphStyle(
                                'CustomFooter',
                                parent=styles['Normal'],
                                fontSize=12,
                                alignment=1,
                                spaceBefore=20,
                                textColor=colors.HexColor('#5D4037')
                            )
                            
                            # Build PDF elements
                            elements = []
                            
                            # Header
                            elements.append(Paragraph("☕ COFFEESTRY", title_style))
                            elements.append(Paragraph("Your Cozy Coffee Shop", subtitle_style))
                            
                            # Order details
                            elements.append(Paragraph(f"<b>Order #:</b> {order_id}", normal_style))
                            elements.append(Paragraph(f"<b>Date:</b> {order_date}", normal_style))
                            elements.append(Paragraph(f"<b>Customer:</b> {customer_name}", normal_style))
                            elements.append(Paragraph(f"<b>Order Type:</b> {order_type}", normal_style))
                            elements.append(Paragraph(f"<b>Payment Status:</b> {payment_method}", normal_style))
                            elements.append(Spacer(1, 20))
                            
                            # Items table
                            table_data = [['Item', 'Qty', 'Price', 'Total']]
                            subtotal = 0
                            for item in items_list:
                                item_total = item['price'] * item['quantity']
                                subtotal += item_total
                                table_data.append([
                                    item['name'],
                                    str(item['quantity']),
                                    f"₱{item['price']:.2f}",
                                    f"₱{item_total:.2f}"
                                ])
                            
                            # Create table with styling
                            table = Table(table_data, colWidths=[2.5*inch, 0.75*inch, 1*inch, 1*inch])
                            table.setStyle(TableStyle([
                                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#5D4037')),
                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                ('FONTSIZE', (0, 0), (-1, 0), 11),
                                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                                ('TOPPADDING', (0, 0), (-1, 0), 10),
                                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#FFF8E1')),
                                ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#3E2723')),
                                ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
                                ('ALIGN', (0, 1), (0, -1), 'LEFT'),
                                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                                ('FONTSIZE', (0, 1), (-1, -1), 10),
                                ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
                                ('TOPPADDING', (0, 1), (-1, -1), 8),
                                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#D4A574')),
                            ]))
                            elements.append(table)
                            elements.append(Spacer(1, 15))
                            
                            # Totals table
                            totals_data = [
                                ['Subtotal:', f'₱{subtotal:.2f}'],
                                ['Tax (0%):', '₱0.00'],
                                ['TOTAL:', f'₱{total:.2f}'],
                            ]
                            totals_table = Table(totals_data, colWidths=[4*inch, 1.25*inch])
                            totals_table.setStyle(TableStyle([
                                ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                                ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                                ('FONTNAME', (0, 0), (-1, 1), 'Helvetica'),
                                ('FONTNAME', (0, 2), (-1, 2), 'Helvetica-Bold'),
                                ('FONTSIZE', (0, 0), (-1, -1), 11),
                                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#3E2723')),
                                ('FONTSIZE', (0, 2), (-1, 2), 14),
                                ('TEXTCOLOR', (0, 2), (-1, 2), colors.HexColor('#5D4037')),
                                ('TOPPADDING', (0, 2), (-1, 2), 10),
                                ('LINEABOVE', (0, 2), (-1, 2), 2, colors.HexColor('#5D4037')),
                            ]))
                            elements.append(totals_table)
                            
                            # Footer
                            elements.append(Spacer(1, 30))
                            elements.append(Paragraph("Thank you for your purchase!", footer_style))
                            elements.append(Paragraph("Visit us again soon! ☕", footer_style))
                            
                            # Build PDF
                            doc.build(elements)
                            
                            page.snack_bar = ft.SnackBar(
                                content=ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE, color=ACCENT_CREAM), ft.Text(f"Receipt saved to {filepath}", color=ACCENT_CREAM)], spacing=10),
                                bgcolor=SUCCESS,
                                duration=4000,
                            )
                            page.snack_bar.open = True
                            page.update()
                        except Exception as ex:
                            page.snack_bar = ft.SnackBar(
                                content=ft.Row([ft.Icon(ft.Icons.ERROR, color=ACCENT_CREAM), ft.Text(f"Error saving receipt: {str(ex)}", color=ACCENT_CREAM)], spacing=10),
                                bgcolor=ERROR
                            )
                            page.snack_bar.open = True
                            page.update()
                
                folder_picker = ft.FilePicker(on_result=on_folder_selected)
                page.overlay.append(folder_picker)
                page.update()
                folder_picker.get_directory_path(
                    dialog_title="Choose where to save the receipt",
                    initial_directory=last_save_path["path"]
                )
            
            order_rows = []
            for order in orders:
                # order = (id, customer_name, order_type, total, order_date, status, payment_status)
                order_id = order[0]
                customer_name = order[1]
                order_type = order[2]
                total = order[3]
                order_date = order[4]
                status = order[5] if len(order) > 5 and order[5] else "pending"
                payment_status = order[6] if len(order) > 6 and order[6] else "unpaid"
                
                # Status badge colors
                status_colors = {
                    "pending": ("#FFA726", TEXT_DARK),  # Orange
                    "confirmed": (PRIMARY_MID, ACCENT_CREAM),  # Brown
                    "completed": (SUCCESS, ACCENT_CREAM),  # Green
                    "cancelled": (ERROR, ACCENT_CREAM),  # Red
                }
                payment_colors = {
                    "unpaid": (ERROR, ACCENT_CREAM),
                    "paid": (SUCCESS, ACCENT_CREAM),
                }
                
                status_bg, status_text = status_colors.get(status, ("#FFA726", TEXT_DARK))
                payment_bg, payment_text = payment_colors.get(payment_status, (ERROR, ACCENT_CREAM))
                
                # Action buttons based on status
                action_buttons = []
                if status == "pending":
                    action_buttons.append(
                        ft.IconButton(
                            icon=ft.Icons.CHECK_CIRCLE_OUTLINE,
                            icon_color=SUCCESS,
                            tooltip="Confirm Order",
                            icon_size=20,
                            on_click=lambda e, oid=order_id: confirm_order_clicked(oid)
                        )
                    )
                if payment_status == "unpaid" and status != "cancelled":
                    action_buttons.append(
                        ft.IconButton(
                            icon=ft.Icons.PAYMENTS,
                            icon_color=ACCENT_GOLD,
                            tooltip="Mark as Paid",
                            icon_size=20,
                            on_click=lambda e, oid=order_id: mark_paid_clicked(oid)
                        )
                    )
                if status == "confirmed" and payment_status == "paid":
                    action_buttons.append(
                        ft.IconButton(
                            icon=ft.Icons.DONE_ALL,
                            icon_color=SUCCESS,
                            tooltip="Complete Order",
                            icon_size=20,
                            on_click=lambda e, oid=order_id: complete_order_clicked(oid)
                        )
                    )
                if status not in ["completed", "cancelled"]:
                    action_buttons.append(
                        ft.IconButton(
                            icon=ft.Icons.CANCEL_OUTLINED,
                            icon_color=ERROR,
                            tooltip="Cancel Order",
                            icon_size=20,
                            on_click=lambda e, oid=order_id: cancel_order_clicked(oid)
                        )
                    )
                action_buttons.append(
                    ft.IconButton(
                        ft.Icons.VISIBILITY,
                        icon_color=PRIMARY_MID,
                        tooltip="View Details",
                        icon_size=20,
                        on_click=lambda e, oid=order_id: view_order_details(oid)
                    )
                )
                action_buttons.append(
                    ft.IconButton(
                        ft.Icons.PRINT,
                        icon_color=ACCENT_GOLD,
                        tooltip="Print Receipt",
                        icon_size=20,
                        on_click=lambda e, oid=order_id: print_receipt_clicked(oid)
                    )
                )
                
                order_rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(f"#{order_id}", color=PRIMARY_MID, weight=ft.FontWeight.W_600)),
                            ft.DataCell(ft.Text(customer_name or "Walk-in", color=TEXT_DARK)),
                            ft.DataCell(
                                ft.Container(
                                    content=ft.Text(order_type or "Dine in", size=11, color=ACCENT_CREAM),
                                    bgcolor=PRIMARY_LIGHT if order_type == "Dine in" else ACCENT_GOLD,
                                    padding=ft.padding.symmetric(horizontal=8, vertical=2),
                                    border_radius=10,
                                )
                            ),
                            ft.DataCell(ft.Text(f"₱{total:.2f}", color=TEXT_DARK, weight=ft.FontWeight.W_500)),
                            ft.DataCell(
                                ft.Container(
                                    content=ft.Text(status.capitalize(), size=11, color=status_text),
                                    bgcolor=status_bg,
                                    padding=ft.padding.symmetric(horizontal=8, vertical=2),
                                    border_radius=10,
                                )
                            ),
                            ft.DataCell(
                                ft.Container(
                                    content=ft.Text(payment_status.capitalize(), size=11, color=payment_text),
                                    bgcolor=payment_bg,
                                    padding=ft.padding.symmetric(horizontal=8, vertical=2),
                                    border_radius=10,
                                )
                            ),
                            ft.DataCell(ft.Text(str(order_date)[:16] if order_date else "", color=TEXT_MID, size=11)),
                            ft.DataCell(ft.Row(action_buttons, spacing=0)),
                        ]
                    )
                )
            
            def view_order_details(order_id):
                items = get_order_items(order_id)
                
                # Get the order info
                order_info = None
                for o in orders:
                    if o[0] == order_id:
                        order_info = o
                        break
                
                # Build items list with details
                items_list = []
                subtotal = 0
                for item in items:
                    # item = (product_name, category, price, quantity)
                    item_total = item[2] * item[3]
                    subtotal += item_total
                    items_list.append(
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.Container(
                                        content=ft.Text(item[1][0], size=11, color=ACCENT_CREAM, weight=ft.FontWeight.BOLD),
                                        bgcolor=PRIMARY_LIGHT if item[1] == "Coffee" else ACCENT_GOLD,
                                        width=24,
                                        height=24,
                                        border_radius=12,
                                        alignment=ft.alignment.center,
                                    ),
                                    ft.Column(
                                        [
                                            ft.Text(item[0], size=13, color=TEXT_DARK, weight=ft.FontWeight.W_500),
                                            ft.Text(f"₱{item[2]:.2f} x {item[3]}", size=11, color=TEXT_MID),
                                        ],
                                        spacing=0,
                                        expand=True,
                                    ),
                                    ft.Text(f"₱{item_total:.2f}", size=13, color=PRIMARY_MID, weight=ft.FontWeight.W_600),
                                ],
                                spacing=10,
                            ),
                            padding=ft.padding.symmetric(vertical=8),
                            border=ft.border.only(bottom=ft.BorderSide(1, ACCENT_CREAM)),
                        )
                    )
                
                def close_dialog(e):
                    page.close(dialog)
                
                dialog = ft.AlertDialog(
                    modal=True,
                    title=ft.Row(
                        [
                            ft.Icon(ft.Icons.RECEIPT_LONG, color=PRIMARY_MID, size=24),
                            ft.Text(f"Order #{order_id}", size=18, weight=ft.FontWeight.BOLD, color=PRIMARY_DARK),
                        ],
                        spacing=10,
                    ),
                    content=ft.Container(
                        content=ft.Column(
                            [
                                # Customer & Order Info
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            ft.Row(
                                                [
                                                    ft.Text("Customer:", size=12, color=TEXT_LIGHT),
                                                    ft.Text(order_info[1] if order_info and order_info[1] else "Walk-in", size=12, color=TEXT_DARK, weight=ft.FontWeight.W_500),
                                                ],
                                                spacing=10,
                                            ),
                                            ft.Row(
                                                [
                                                    ft.Text("Type:", size=12, color=TEXT_LIGHT),
                                                    ft.Container(
                                                        content=ft.Text(order_info[2] if order_info and order_info[2] else "Dine in", size=11, color=ACCENT_CREAM),
                                                        bgcolor=PRIMARY_LIGHT,
                                                        padding=ft.padding.symmetric(horizontal=8, vertical=2),
                                                        border_radius=8,
                                                    ),
                                                ],
                                                spacing=10,
                                            ),
                                            ft.Row(
                                                [
                                                    ft.Text("Date:", size=12, color=TEXT_LIGHT),
                                                    ft.Text(str(order_info[4])[:19] if order_info and order_info[4] else "", size=12, color=TEXT_DARK),
                                                ],
                                                spacing=10,
                                            ),
                                        ],
                                        spacing=5,
                                    ),
                                    padding=10,
                                    bgcolor=ACCENT_CREAM,
                                    border_radius=8,
                                ),
                                ft.Container(height=10),
                                ft.Text("Order Items:", size=14, weight=ft.FontWeight.W_600, color=TEXT_MID),
                                ft.Container(
                                    content=ft.Column(
                                        items_list if items_list else [
                                            ft.Text("No items found", size=13, color=TEXT_LIGHT, italic=True)
                                        ],
                                        spacing=0,
                                        scroll=ft.ScrollMode.AUTO,
                                    ),
                                    height=200 if len(items_list) > 3 else None,
                                ),
                                ft.Divider(height=15, color=ACCENT_WARM),
                                ft.Row(
                                    [
                                        ft.Text("Total:", size=16, weight=ft.FontWeight.BOLD, color=PRIMARY_DARK),
                                        ft.Container(expand=True),
                                        ft.Text(f"₱{order_info[3]:.2f}" if order_info else f"₱{subtotal:.2f}", size=18, weight=ft.FontWeight.BOLD, color=SUCCESS),
                                    ],
                                ),
                            ],
                            spacing=5,
                        ),
                        width=350,
                        padding=10,
                    ),
                    actions=[
                        ft.ElevatedButton(
                            "Close",
                            bgcolor=PRIMARY_MID,
                            color=ACCENT_CREAM,
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                            on_click=close_dialog,
                        ),
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                )
                
                page.open(dialog)
            
            main_content.content = ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Icon(ft.Icons.HISTORY, size=28, color=PRIMARY_MID),
                                ft.Text("Order History", size=22, weight=ft.FontWeight.BOLD, color=PRIMARY_DARK),
                                ft.Container(expand=True),
                                ft.ElevatedButton(
                                    "Refresh",
                                    icon=ft.Icons.REFRESH,
                                    bgcolor=PRIMARY_LIGHT,
                                    color=ACCENT_CREAM,
                                    on_click=lambda e: refresh_orders(),
                                ),
                            ],
                            spacing=10,
                        ),
                        ft.Text("Manage orders - Confirm orders and mark payments as received", size=13, color=TEXT_MID),
                        ft.Divider(height=20, color=ACCENT_CREAM, thickness=2),
                        ft.Container(
                            content=ft.Column([
                                ft.DataTable(
                                    columns=[
                                        ft.DataColumn(ft.Text("Order #", weight=ft.FontWeight.W_600, color=PRIMARY_DARK, size=12)),
                                        ft.DataColumn(ft.Text("Customer", weight=ft.FontWeight.W_600, color=PRIMARY_DARK, size=12)),
                                        ft.DataColumn(ft.Text("Type", weight=ft.FontWeight.W_600, color=PRIMARY_DARK, size=12)),
                                        ft.DataColumn(ft.Text("Total", weight=ft.FontWeight.W_600, color=PRIMARY_DARK, size=12)),
                                        ft.DataColumn(ft.Text("Status", weight=ft.FontWeight.W_600, color=PRIMARY_DARK, size=12)),
                                        ft.DataColumn(ft.Text("Payment", weight=ft.FontWeight.W_600, color=PRIMARY_DARK, size=12)),
                                        ft.DataColumn(ft.Text("Date", weight=ft.FontWeight.W_600, color=PRIMARY_DARK, size=12)),
                                        ft.DataColumn(ft.Text("Actions", weight=ft.FontWeight.W_600, color=PRIMARY_DARK, size=12)),
                                    ],
                                    rows=order_rows if order_rows else [],
                                    border=ft.border.all(1, ACCENT_WARM),
                                    border_radius=10,
                                    heading_row_color=ACCENT_CREAM,
                                    data_row_color={ft.ControlState.HOVERED: ft.Colors.with_opacity(0.1, ACCENT_WARM)},
                                    column_spacing=20,
                                ),
                            ], scroll=ft.ScrollMode.AUTO, horizontal_alignment=ft.CrossAxisAlignment.STRETCH),
                            bgcolor=BG_CARD,
                            padding=20,
                            border_radius=15,
                            shadow=ft.BoxShadow(
                                color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                                blur_radius=15,
                                offset=ft.Offset(0, 4)
                            ),
                            expand=True,
                        ) if order_rows else ft.Container(
                            content=ft.Column([
                                ft.Icon(ft.Icons.RECEIPT_LONG, size=60, color=TEXT_LIGHT),
                                ft.Text("No orders yet", size=18, color=TEXT_MID),
                                ft.Text("Orders will appear here after customers place orders", size=14, color=TEXT_LIGHT),
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                            bgcolor=BG_CARD,
                            padding=50,
                            border_radius=15,
                            alignment=ft.alignment.center,
                        ),
                    ],
                    expand=True
                ),
                padding=20,
                bgcolor=BG_LIGHT,
                expand=True,
            )
            page.update()
                                        
        # MY CUSTOMERS PAGE - Business Owner can create and manage customers
        def layout_customers():
            customers = get_customers_for_business(current_user_id) if current_user_id else []
            
            # Create customer form fields
            new_customer_username = ft.TextField(
                label="Username",
                hint_text="Enter customer username",
                width=250,
                border_color=PRIMARY_LIGHT,
                focused_border_color=PRIMARY_MID,
                border_radius=10,
            )
            new_customer_password = ft.TextField(
                label="Password",
                hint_text="Enter customer password",
                width=250,
                border_color=PRIMARY_LIGHT,
                focused_border_color=PRIMARY_MID,
                border_radius=10,
                password=True,
                can_reveal_password=True,
            )
            
            def create_customer_clicked(e):
                if not new_customer_username.value or not new_customer_password.value:
                    page.snack_bar = ft.SnackBar(ft.Text("Please fill in all fields", color=ACCENT_CREAM), bgcolor=ERROR)
                    page.snack_bar.open = True
                    page.update()
                    return
                
                success, message = create_customer(new_customer_username.value, new_customer_password.value, current_user_id)
                if success:
                    page.snack_bar = ft.SnackBar(
                        content=ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE, color=ACCENT_CREAM), ft.Text(message, color=ACCENT_CREAM)], spacing=10),
                        bgcolor=SUCCESS
                    )
                    new_customer_username.value = ""
                    new_customer_password.value = ""
                    layout_customers()  # Refresh
                else:
                    page.snack_bar = ft.SnackBar(ft.Text(message, color=ACCENT_CREAM), bgcolor=ERROR)
                page.snack_bar.open = True
                page.update()
            
            def delete_customer_clicked(customer_id):
                def confirm_delete(e):
                    delete_customer(customer_id)
                    page.close(delete_dialog)
                    page.snack_bar = ft.SnackBar(
                        content=ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE, color=ACCENT_CREAM), ft.Text("Customer deleted!", color=ACCENT_CREAM)], spacing=10),
                        bgcolor=SUCCESS
                    )
                    page.snack_bar.open = True
                    layout_customers()  # Refresh
                
                delete_dialog = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("Confirm Delete", color=ERROR),
                    content=ft.Text("Are you sure you want to delete this customer?"),
                    actions=[
                        ft.TextButton("Cancel", on_click=lambda e: page.close(delete_dialog)),
                        ft.ElevatedButton("Delete", bgcolor=ERROR, color=ACCENT_CREAM, on_click=confirm_delete),
                    ],
                )
                page.open(delete_dialog)
            
            # Build customer rows
            customer_rows = []
            for customer in customers:
                cust_id, cust_username, cust_password, cust_created = customer
                customer_rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(f"#{cust_id}", color=PRIMARY_MID, weight=ft.FontWeight.W_600)),
                            ft.DataCell(ft.Text(cust_username, color=TEXT_DARK)),
                            ft.DataCell(ft.Text("••••••••", color=TEXT_MID)),
                            ft.DataCell(ft.Text(str(cust_created)[:10] if cust_created else "", color=TEXT_MID, size=12)),
                            ft.DataCell(
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    icon_color=ERROR,
                                    icon_size=20,
                                    on_click=lambda e, cid=cust_id: delete_customer_clicked(cid),
                                )
                            ),
                        ]
                    )
                )
            
            main_content.content = ft.Container(
                content=ft.Column(
                    [
                        # Header
                        ft.Row([
                            ft.Icon(ft.Icons.PEOPLE_ROUNDED, size=28, color=PRIMARY_MID),
                            ft.Text("My Customers", size=26, weight=ft.FontWeight.BOLD, color=PRIMARY_DARK),
                        ], spacing=12),
                        ft.Text("Create and manage customer accounts", size=14, color=TEXT_MID),
                        ft.Divider(height=20, color=ACCENT_CREAM),
                        
                        # Create Customer Form
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Create New Customer", size=18, weight=ft.FontWeight.W_600, color=PRIMARY_DARK),
                                ft.Container(height=10),
                                ft.Row([
                                    new_customer_username,
                                    new_customer_password,
                                    ft.ElevatedButton(
                                        "Create Customer",
                                        icon=ft.Icons.PERSON_ADD,
                                        bgcolor=SUCCESS,
                                        color=ACCENT_CREAM,
                                        on_click=create_customer_clicked,
                                    ),
                                ], spacing=15),
                            ]),
                            padding=20,
                            bgcolor=BG_CARD,
                            border_radius=15,
                            border=ft.border.all(1, ACCENT_CREAM),
                        ),
                        ft.Container(height=20),
                        
                        # Customer Stats
                        ft.Row([
                            ft.Container(
                                content=ft.Column([
                                    ft.Text(str(len(customers)), size=32, weight=ft.FontWeight.BOLD, color=PRIMARY_MID),
                                    ft.Text("Total Customers", size=12, color=TEXT_MID),
                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                padding=20,
                                bgcolor=ACCENT_CREAM,
                                border_radius=12,
                                width=150,
                            ),
                        ]),
                        ft.Container(height=20),
                        
                        # Customers Table
                        ft.Container(
                            content=ft.DataTable(
                                columns=[
                                    ft.DataColumn(ft.Text("ID", weight=ft.FontWeight.W_600, color=PRIMARY_DARK)),
                                    ft.DataColumn(ft.Text("Username", weight=ft.FontWeight.W_600, color=PRIMARY_DARK)),
                                    ft.DataColumn(ft.Text("Password", weight=ft.FontWeight.W_600, color=PRIMARY_DARK)),
                                    ft.DataColumn(ft.Text("Created", weight=ft.FontWeight.W_600, color=PRIMARY_DARK)),
                                    ft.DataColumn(ft.Text("Actions", weight=ft.FontWeight.W_600, color=PRIMARY_DARK)),
                                ],
                                rows=customer_rows,
                                border=ft.border.all(1, ACCENT_WARM),
                                border_radius=10,
                                heading_row_color=ACCENT_CREAM,
                            ),
                            bgcolor=BG_CARD,
                            padding=20,
                            border_radius=15,
                        ) if customer_rows else ft.Container(
                            content=ft.Column([
                                ft.Icon(ft.Icons.PEOPLE_OUTLINE, size=60, color=TEXT_LIGHT),
                                ft.Text("No customers yet", size=18, color=TEXT_MID),
                                ft.Text("Create customer accounts above", size=14, color=TEXT_LIGHT),
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                            bgcolor=BG_CARD,
                            padding=50,
                            border_radius=15,
                            alignment=ft.alignment.center,
                        ),
                    ],
                    expand=True,
                    scroll=ft.ScrollMode.AUTO,
                ),
                padding=20,
                bgcolor=BG_LIGHT,
                expand=True,
            )
            page.update()
        
        # CUSTOMER ORDERS PAGE - Business Owner can view and manage customer orders
        def layout_customer_orders():
            orders = get_orders_for_business(current_user_id) if current_user_id else []
            pending_orders = get_pending_orders_for_business(current_user_id) if current_user_id else []
            
            def confirm_order_clicked(order_id):
                confirm_order(order_id)
                page.snack_bar = ft.SnackBar(
                    content=ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE, color=ACCENT_CREAM), ft.Text("Order confirmed!", color=ACCENT_CREAM)], spacing=10),
                    bgcolor=SUCCESS
                )
                page.snack_bar.open = True
                layout_customer_orders()  # Refresh
            
            def mark_paid_clicked(order_id):
                mark_order_paid(order_id)
                page.snack_bar = ft.SnackBar(
                    content=ft.Row([ft.Icon(ft.Icons.PAYMENT, color=ACCENT_CREAM), ft.Text("Payment confirmed!", color=ACCENT_CREAM)], spacing=10),
                    bgcolor=SUCCESS
                )
                page.snack_bar.open = True
                layout_customer_orders()  # Refresh
            
            def complete_order_clicked(order_id):
                complete_order(order_id)
                page.snack_bar = ft.SnackBar(
                    content=ft.Row([ft.Icon(ft.Icons.DONE_ALL, color=ACCENT_CREAM), ft.Text("Order completed!", color=ACCENT_CREAM)], spacing=10),
                    bgcolor=SUCCESS
                )
                page.snack_bar.open = True
                layout_customer_orders()  # Refresh
            
            def cancel_order_clicked(order_id):
                cancel_order(order_id)
                page.snack_bar = ft.SnackBar(
                    content=ft.Row([ft.Icon(ft.Icons.CANCEL, color=ACCENT_CREAM), ft.Text("Order cancelled!", color=ACCENT_CREAM)], spacing=10),
                    bgcolor=ERROR
                )
                page.snack_bar.open = True
                layout_customer_orders()  # Refresh
            
            def view_order_details(order_id, total):
                items = get_order_items(order_id)
                items_list = []
                for item in items:
                    item_name, item_category, item_price, item_qty = item
                    items_list.append(
                        ft.Container(
                            content=ft.Row([
                                ft.Text(item_name, size=13, color=TEXT_DARK, expand=True),
                                ft.Text(f"x{item_qty}", size=12, color=TEXT_MID),
                                ft.Text(f"₱{item_price * item_qty:.2f}", size=13, color=PRIMARY_MID, weight=ft.FontWeight.W_500),
                            ]),
                            padding=ft.padding.symmetric(vertical=8),
                            border=ft.border.only(bottom=ft.BorderSide(1, ACCENT_CREAM)),
                        )
                    )
                
                details_dialog = ft.AlertDialog(
                    modal=True,
                    title=ft.Text(f"Order #{order_id} Details", weight=ft.FontWeight.BOLD, color=PRIMARY_DARK),
                    content=ft.Container(
                        content=ft.Column([
                            ft.Container(
                                content=ft.Column(items_list if items_list else [ft.Text("No items", color=TEXT_LIGHT)], spacing=0),
                                height=200 if len(items_list) > 4 else None,
                                padding=10,
                            ),
                            ft.Divider(color=ACCENT_WARM),
                            ft.Row([
                                ft.Text("Total:", size=16, weight=ft.FontWeight.BOLD, color=PRIMARY_DARK),
                                ft.Container(expand=True),
                                ft.Text(f"₱{total:.2f}", size=18, weight=ft.FontWeight.BOLD, color=SUCCESS),
                            ]),
                        ], spacing=10),
                        width=350,
                    ),
                    actions=[ft.ElevatedButton("Close", bgcolor=PRIMARY_MID, color=ACCENT_CREAM, on_click=lambda e: page.close(details_dialog))],
                )
                page.open(details_dialog)
            
            # Build order rows
            order_rows = []
            for order in orders:
                ord_id, cust_name, ord_type, ord_total, ord_status, payment_status, ord_date, cust_username = order
                
                # Status badge color
                status_colors = {
                    'pending': ACCENT_GOLD,
                    'confirmed': PRIMARY_LIGHT,
                    'completed': SUCCESS,
                    'cancelled': ERROR
                }
                payment_color = SUCCESS if payment_status == 'paid' else ERROR
                
                # Action buttons based on status
                action_buttons = []
                if ord_status == 'pending':
                    action_buttons.append(
                        ft.IconButton(icon=ft.Icons.CHECK, icon_color=SUCCESS, tooltip="Confirm", on_click=lambda e, oid=ord_id: confirm_order_clicked(oid))
                    )
                    action_buttons.append(
                        ft.IconButton(icon=ft.Icons.CANCEL, icon_color=ERROR, tooltip="Cancel", on_click=lambda e, oid=ord_id: cancel_order_clicked(oid))
                    )
                elif ord_status == 'confirmed':
                    if payment_status == 'unpaid':
                        action_buttons.append(
                            ft.IconButton(icon=ft.Icons.PAYMENT, icon_color=SUCCESS, tooltip="Mark Paid", on_click=lambda e, oid=ord_id: mark_paid_clicked(oid))
                        )
                    action_buttons.append(
                        ft.IconButton(icon=ft.Icons.DONE_ALL, icon_color=PRIMARY_MID, tooltip="Complete", on_click=lambda e, oid=ord_id: complete_order_clicked(oid))
                    )
                
                action_buttons.append(
                    ft.IconButton(icon=ft.Icons.VISIBILITY, icon_color=PRIMARY_LIGHT, tooltip="View Details", on_click=lambda e, oid=ord_id, t=ord_total: view_order_details(oid, t))
                )
                
                order_rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(f"#{ord_id}", color=PRIMARY_MID, weight=ft.FontWeight.W_600)),
                            ft.DataCell(ft.Text(cust_username or cust_name or "Walk-in", color=TEXT_DARK)),
                            ft.DataCell(
                                ft.Container(
                                    content=ft.Text(ord_status.capitalize(), size=11, color=ACCENT_CREAM),
                                    bgcolor=status_colors.get(ord_status, TEXT_MID),
                                    padding=ft.padding.symmetric(horizontal=10, vertical=3),
                                    border_radius=12,
                                )
                            ),
                            ft.DataCell(
                                ft.Container(
                                    content=ft.Text(payment_status.capitalize(), size=11, color=ACCENT_CREAM),
                                    bgcolor=payment_color,
                                    padding=ft.padding.symmetric(horizontal=10, vertical=3),
                                    border_radius=12,
                                )
                            ),
                            ft.DataCell(ft.Text(f"₱{ord_total:.2f}", color=TEXT_DARK, weight=ft.FontWeight.W_500)),
                            ft.DataCell(ft.Text(str(ord_date)[:16] if ord_date else "", color=TEXT_MID, size=11)),
                            ft.DataCell(ft.Row(action_buttons, spacing=0)),
                        ]
                    )
                )
            
            main_content.content = ft.Container(
                content=ft.Column(
                    [
                        # Header
                        ft.Row([
                            ft.Icon(ft.Icons.SHOPPING_BAG_ROUNDED, size=28, color=PRIMARY_MID),
                            ft.Text("Customer Orders", size=26, weight=ft.FontWeight.BOLD, color=PRIMARY_DARK),
                        ], spacing=12),
                        ft.Text("Manage and confirm customer orders", size=14, color=TEXT_MID),
                        ft.Divider(height=20, color=ACCENT_CREAM),
                        
                        # Stats Row
                        ft.Row([
                            ft.Container(
                                content=ft.Column([
                                    ft.Text(str(len(pending_orders)), size=28, weight=ft.FontWeight.BOLD, color=ACCENT_GOLD),
                                    ft.Text("Pending", size=12, color=TEXT_MID),
                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                padding=15,
                                bgcolor=BG_CARD,
                                border_radius=12,
                                border=ft.border.all(2, ACCENT_GOLD),
                                width=100,
                            ),
                            ft.Container(
                                content=ft.Column([
                                    ft.Text(str(len([o for o in orders if o[4] == 'completed'])), size=28, weight=ft.FontWeight.BOLD, color=SUCCESS),
                                    ft.Text("Completed", size=12, color=TEXT_MID),
                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                padding=15,
                                bgcolor=BG_CARD,
                                border_radius=12,
                                border=ft.border.all(2, SUCCESS),
                                width=100,
                            ),
                            ft.Container(
                                content=ft.Column([
                                    ft.Text(str(len(orders)), size=28, weight=ft.FontWeight.BOLD, color=PRIMARY_MID),
                                    ft.Text("Total Orders", size=12, color=TEXT_MID),
                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                padding=15,
                                bgcolor=BG_CARD,
                                border_radius=12,
                                border=ft.border.all(2, PRIMARY_MID),
                                width=100,
                            ),
                        ], spacing=15),
                        ft.Container(height=20),
                        
                        # Orders Table
                        ft.Container(
                            content=ft.Column([
                                ft.DataTable(
                                    columns=[
                                        ft.DataColumn(ft.Text("Order", weight=ft.FontWeight.W_600, color=PRIMARY_DARK)),
                                        ft.DataColumn(ft.Text("Customer", weight=ft.FontWeight.W_600, color=PRIMARY_DARK)),
                                        ft.DataColumn(ft.Text("Status", weight=ft.FontWeight.W_600, color=PRIMARY_DARK)),
                                        ft.DataColumn(ft.Text("Payment", weight=ft.FontWeight.W_600, color=PRIMARY_DARK)),
                                        ft.DataColumn(ft.Text("Total", weight=ft.FontWeight.W_600, color=PRIMARY_DARK)),
                                        ft.DataColumn(ft.Text("Date", weight=ft.FontWeight.W_600, color=PRIMARY_DARK)),
                                        ft.DataColumn(ft.Text("Actions", weight=ft.FontWeight.W_600, color=PRIMARY_DARK)),
                                    ],
                                    rows=order_rows,
                                    border=ft.border.all(1, ACCENT_WARM),
                                    border_radius=10,
                                    heading_row_color=ACCENT_CREAM,
                                ),
                            ], scroll=ft.ScrollMode.AUTO),
                            bgcolor=BG_CARD,
                            padding=20,
                            border_radius=15,
                            expand=True,
                        ) if order_rows else ft.Container(
                            content=ft.Column([
                                ft.Icon(ft.Icons.SHOPPING_BAG_OUTLINED, size=60, color=TEXT_LIGHT),
                                ft.Text("No customer orders yet", size=18, color=TEXT_MID),
                                ft.Text("Customer orders will appear here", size=14, color=TEXT_LIGHT),
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                            bgcolor=BG_CARD,
                            padding=50,
                            border_radius=15,
                            alignment=ft.alignment.center,
                        ),
                    ],
                    expand=True,
                ),
                padding=20,
                bgcolor=BG_LIGHT,
                expand=True,
            )
            page.update()
                                        
        # SIDEBAR - Modern Coffee Shop Style
        def create_sidebar_button(text, icon, on_click, is_active=False):
            return ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(icon, size=20, color=ACCENT_CREAM if not is_active else PRIMARY_DARK),
                        ft.Text(text, size=13, color=ACCENT_CREAM if not is_active else PRIMARY_DARK, weight=ft.FontWeight.W_500),
                    ],
                    spacing=12,
                ),
                padding=ft.padding.symmetric(horizontal=15, vertical=12),
                border_radius=10,
                bgcolor=PRIMARY_LIGHT if is_active else ft.Colors.TRANSPARENT,
                on_click=on_click,
                on_hover=lambda e: setattr(e.control, 'bgcolor', ft.Colors.with_opacity(0.2, ACCENT_CREAM) if e.data == "true" else (PRIMARY_LIGHT if is_active else ft.Colors.TRANSPARENT)) or page.update(),
                ink=True,
            )

        sidebar = ft.Container(
            bgcolor=PRIMARY_DARK,
            width=250,
            padding=ft.padding.symmetric(horizontal=15, vertical=20),
            border_radius=ft.border_radius.only(top_right=20, bottom_right=20),
            shadow=ft.BoxShadow(
                color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
                blur_radius=20,
                offset=ft.Offset(4, 0)
            ),
            content=ft.Column(
                [
                    # Logo Section
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon(ft.Icons.LOCAL_CAFE, size=32, color=ACCENT_WARM),
                                ft.Text("Coffeestry", size=22, color=ACCENT_CREAM, weight=ft.FontWeight.BOLD),
                            ],
                            spacing=10,
                        ),
                        margin=ft.margin.only(bottom=10),
                    ),
                    ft.Divider(color=ft.Colors.with_opacity(0.3, ACCENT_CREAM), thickness=1),
                    ft.Container(height=15),
                    
                    # Navigation Section
                    ft.Text("MENU", size=11, color=TEXT_LIGHT, weight=ft.FontWeight.W_600),
                    ft.Container(height=10),
                    
                    create_sidebar_button("Dashboard", ft.Icons.DASHBOARD_ROUNDED, lambda e: layout5()),
                    ft.Container(height=5),
                    create_sidebar_button("Products & Prices", ft.Icons.INVENTORY_2_ROUNDED, lambda e: layout6()),
                    ft.Container(height=5),
                    create_sidebar_button("Order History", ft.Icons.HISTORY_ROUNDED, lambda e: layout_order_history()),
                    ft.Container(height=5),
                    create_sidebar_button("My Customers", ft.Icons.PEOPLE_ROUNDED, lambda e: layout_customers()),
                    ft.Container(height=5),
                    create_sidebar_button("Customer Orders", ft.Icons.SHOPPING_BAG_ROUNDED, lambda e: layout_customer_orders()),
                    
                    ft.Container(expand=True),
                    
                    # User Section
                    ft.Divider(color=ft.Colors.with_opacity(0.3, ACCENT_CREAM), thickness=1),
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Container(
                                    content=ft.Icon(ft.Icons.PERSON, size=20, color=PRIMARY_DARK),
                                    bgcolor=ACCENT_WARM,
                                    border_radius=20,
                                    padding=8,
                                ),
                                ft.Column(
                                    [
                                        ft.Text("Owner", size=13, color=ACCENT_CREAM, weight=ft.FontWeight.W_600),
                                        ft.Text("Admin", size=11, color=TEXT_LIGHT),
                                    ],
                                    spacing=0,
                                ),
                            ],
                            spacing=10,
                        ),
                        margin=ft.margin.symmetric(vertical=15),
                    ),
                    
                    # Logout Button
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon(ft.Icons.LOGOUT_ROUNDED, size=18, color=ACCENT_CREAM),
                                ft.Text("Logout", size=13, color=ACCENT_CREAM, weight=ft.FontWeight.W_500),
                            ],
                            spacing=10,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        padding=ft.padding.symmetric(horizontal=15, vertical=10),
                        border_radius=10,
                        bgcolor=ft.Colors.with_opacity(0.2, ERROR),
                        on_click=lambda e: layout1(),
                        on_hover=lambda e: setattr(e.control, 'bgcolor', ERROR if e.data == "true" else ft.Colors.with_opacity(0.2, ERROR)) or page.update(),
                        ink=True,
                    ),
                ],
                spacing=0,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            ),
        )

        layout = ft.Row([sidebar, main_content], expand=True, spacing=0)
        page.add(layout)
        page.update()

        # Load Dashboard by default
        layout5()

    # ============ SUPERADMIN DASHBOARD ============
    def superadmin_dashboard():
        page.clean()
        main_content = ft.Container(expand=True, bgcolor=BG_LIGHT)
        
        # Dashboard Overview
        def sa_dashboard():
            total_owners = get_total_business_owners()
            total_customers = get_total_customers()
            total_sales = get_total_sales()
            total_orders = get_total_orders()
            total_products = get_total_products()
            sales_data = get_sales_by_date(7)
            customers_data = get_customers_by_date(7)
            orders_data = get_orders_by_date(7)
            top_owners = get_top_business_owners(5)
            order_status = get_order_status_distribution()
            monthly_revenue = get_monthly_revenue(6)
            top_products = get_top_selling_products(5)
            
            # Build sales chart items (bar chart style)
            sales_chart_items = []
            max_sale = max([amt for _, amt in sales_data[-7:]], default=1)
            for date, amount in sales_data[-7:]:
                bar_height = max(15, (amount / max_sale) * 120) if max_sale > 0 else 15
                sales_chart_items.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Text(f"₱{amount:,.0f}", size=9, color=PRIMARY_MID, weight=ft.FontWeight.W_500),
                            ft.Container(
                                bgcolor=PRIMARY_MID,
                                width=35,
                                height=bar_height,
                                border_radius=ft.border_radius.only(top_left=5, top_right=5),
                            ),
                            ft.Text(date[-5:], size=9, color=TEXT_MID),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                    )
                )
            
            # Build orders chart items
            orders_chart_items = []
            max_orders = max([cnt for _, cnt in orders_data[-7:]], default=1)
            for date, count in orders_data[-7:]:
                bar_height = max(15, (count / max_orders) * 120) if max_orders > 0 else 15
                orders_chart_items.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Text(str(count), size=9, color=SUCCESS, weight=ft.FontWeight.W_500),
                            ft.Container(
                                bgcolor=SUCCESS,
                                width=35,
                                height=bar_height,
                                border_radius=ft.border_radius.only(top_left=5, top_right=5),
                            ),
                            ft.Text(date[-5:], size=9, color=TEXT_MID),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                    )
                )
            
            # Build monthly revenue chart
            monthly_chart_items = []
            max_monthly = max([rev for _, rev in monthly_revenue], default=1)
            for month, revenue in monthly_revenue:
                bar_height = max(15, (revenue / max_monthly) * 100) if max_monthly > 0 else 15
                month_name = month[-2:]  # Get just the month number
                monthly_chart_items.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Text(f"₱{revenue/1000:.1f}k" if revenue >= 1000 else f"₱{revenue:.0f}", size=9, color=ACCENT_GOLD, weight=ft.FontWeight.W_500),
                            ft.Container(
                                bgcolor=ACCENT_GOLD,
                                width=40,
                                height=bar_height,
                                border_radius=ft.border_radius.only(top_left=5, top_right=5),
                            ),
                            ft.Text(month, size=8, color=TEXT_MID),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                    )
                )
            
            # Build order status pie chart representation
            status_items = []
            status_colors = {'pending': "#FFC107", 'confirmed': PRIMARY_MID, 'completed': SUCCESS, 'cancelled': ERROR}
            status_icons = {'pending': ft.Icons.HOURGLASS_EMPTY, 'confirmed': ft.Icons.VERIFIED, 'completed': ft.Icons.CHECK_CIRCLE, 'cancelled': ft.Icons.CANCEL}
            total_status_orders = sum([cnt for _, cnt in order_status]) or 1
            for status, count in order_status:
                percentage = (count / total_status_orders) * 100
                status_items.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(status_icons.get(status, ft.Icons.CIRCLE), size=20, color=status_colors.get(status, TEXT_MID)),
                            ft.Column([
                                ft.Text(status.capitalize(), size=12, weight=ft.FontWeight.W_500, color=TEXT_DARK),
                                ft.Text(f"{count} orders ({percentage:.1f}%)", size=10, color=TEXT_MID),
                            ], spacing=2),
                            ft.Container(expand=True),
                            ft.Container(
                                bgcolor=status_colors.get(status, TEXT_MID),
                                width=max(10, percentage * 1.5),
                                height=20,
                                border_radius=10,
                            ),
                        ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=ft.padding.symmetric(vertical=8),
                    )
                )
            
            # Build top business owners table
            owner_rows = []
            for i, (username, total_sale, order_count) in enumerate(top_owners):
                medal_colors = [ACCENT_GOLD, "#C0C0C0", "#CD7F32", PRIMARY_LIGHT, TEXT_MID]
                owner_rows.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Container(
                                content=ft.Text(f"#{i+1}", size=11, color=ACCENT_CREAM, weight=ft.FontWeight.BOLD),
                                bgcolor=medal_colors[i] if i < 5 else TEXT_MID,
                                width=28,
                                height=28,
                                border_radius=14,
                                alignment=ft.alignment.center,
                            ),
                            ft.Container(width=10),
                            ft.Column([
                                ft.Text(username, size=13, weight=ft.FontWeight.W_500, color=TEXT_DARK),
                                ft.Text(f"{order_count} orders", size=10, color=TEXT_MID),
                            ], spacing=2),
                            ft.Container(expand=True),
                            ft.Text(f"₱{total_sale:,.2f}", size=14, weight=ft.FontWeight.BOLD, color=SUCCESS),
                        ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=ft.padding.symmetric(vertical=8, horizontal=10),
                        border_radius=8,
                        bgcolor=BG_LIGHT if i % 2 == 0 else BG_CARD,
                    )
                )
            
            # Build top selling products list
            product_rows = []
            for i, (product_name, qty_sold, revenue) in enumerate(top_products):
                product_rows.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.LOCAL_CAFE if i < 3 else ft.Icons.CAKE, size=20, color=PRIMARY_MID),
                            ft.Column([
                                ft.Text(product_name, size=12, weight=ft.FontWeight.W_500, color=TEXT_DARK),
                                ft.Text(f"{qty_sold} sold • ₱{revenue:,.2f}", size=10, color=TEXT_MID),
                            ], spacing=2),
                        ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=ft.padding.symmetric(vertical=6),
                    )
                )
            
            main_content.content = ft.Container(
                content=ft.Column([
                    # Header
                    ft.Row([
                        ft.Icon(ft.Icons.ADMIN_PANEL_SETTINGS, size=32, color=PRIMARY_MID),
                        ft.Text("SuperAdmin Dashboard", size=28, weight=ft.FontWeight.BOLD, color=PRIMARY_DARK),
                    ], spacing=12),
                    ft.Text("Platform Overview & Analytics", size=14, color=TEXT_MID),
                    ft.Divider(height=25, color=ACCENT_CREAM),
                    
                    # Stats Cards Row 1
                    ft.Row([
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(ft.Icons.STORE, size=32, color=PRIMARY_MID),
                                ft.Text(str(total_owners), size=32, weight=ft.FontWeight.BOLD, color=PRIMARY_DARK),
                                ft.Text("Business Owners", size=12, color=TEXT_MID),
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                            padding=20,
                            bgcolor=BG_CARD,
                            border_radius=15,
                            border=ft.border.all(2, PRIMARY_LIGHT),
                            expand=True,
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(ft.Icons.PEOPLE, size=32, color=SUCCESS),
                                ft.Text(str(total_customers), size=32, weight=ft.FontWeight.BOLD, color=PRIMARY_DARK),
                                ft.Text("Total Customers", size=12, color=TEXT_MID),
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                            padding=20,
                            bgcolor=BG_CARD,
                            border_radius=15,
                            border=ft.border.all(2, SUCCESS),
                            expand=True,
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(ft.Icons.MONETIZATION_ON, size=32, color=ACCENT_GOLD),
                                ft.Text(f"₱{total_sales:,.2f}", size=24, weight=ft.FontWeight.BOLD, color=PRIMARY_DARK),
                                ft.Text("Total Sales", size=12, color=TEXT_MID),
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                            padding=20,
                            bgcolor=BG_CARD,
                            border_radius=15,
                            border=ft.border.all(2, ACCENT_GOLD),
                            expand=True,
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(ft.Icons.RECEIPT_LONG, size=32, color=PRIMARY_MID),
                                ft.Text(str(total_orders), size=32, weight=ft.FontWeight.BOLD, color=PRIMARY_DARK),
                                ft.Text("Total Orders", size=12, color=TEXT_MID),
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                            padding=20,
                            bgcolor=BG_CARD,
                            border_radius=15,
                            border=ft.border.all(2, PRIMARY_MID),
                            expand=True,
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(ft.Icons.INVENTORY_2, size=32, color=PRIMARY_LIGHT),
                                ft.Text(str(total_products), size=32, weight=ft.FontWeight.BOLD, color=PRIMARY_DARK),
                                ft.Text("Total Products", size=12, color=TEXT_MID),
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                            padding=20,
                            bgcolor=BG_CARD,
                            border_radius=15,
                            border=ft.border.all(2, PRIMARY_LIGHT),
                            expand=True,
                        ),
                    ], spacing=15),
                    ft.Container(height=15),
                    
                    # Charts Row 1 - Sales and Orders
                    ft.Row([
                        # Sales Chart
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Icon(ft.Icons.TRENDING_UP, size=20, color=PRIMARY_MID),
                                    ft.Text("Sales (Last 7 Days)", size=14, weight=ft.FontWeight.W_600, color=PRIMARY_DARK),
                                ], spacing=8),
                                ft.Container(height=10),
                                ft.Row(
                                    sales_chart_items if sales_chart_items else [ft.Text("No sales data yet", color=TEXT_LIGHT)],
                                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                ),
                            ]),
                            padding=20,
                            bgcolor=BG_CARD,
                            border_radius=15,
                            expand=True,
                        ),
                        # Orders Chart
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Icon(ft.Icons.SHOPPING_BAG, size=20, color=SUCCESS),
                                    ft.Text("Orders (Last 7 Days)", size=14, weight=ft.FontWeight.W_600, color=PRIMARY_DARK),
                                ], spacing=8),
                                ft.Container(height=10),
                                ft.Row(
                                    orders_chart_items if orders_chart_items else [ft.Text("No orders data yet", color=TEXT_LIGHT)],
                                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                ),
                            ]),
                            padding=20,
                            bgcolor=BG_CARD,
                            border_radius=15,
                            expand=True,
                        ),
                    ], spacing=15),
                    ft.Container(height=15),
                    
                    # Charts Row 2 - Monthly Revenue and Order Status
                    ft.Row([
                        # Monthly Revenue Chart
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Icon(ft.Icons.BAR_CHART, size=20, color=ACCENT_GOLD),
                                    ft.Text("Monthly Revenue", size=14, weight=ft.FontWeight.W_600, color=PRIMARY_DARK),
                                ], spacing=8),
                                ft.Container(height=10),
                                ft.Row(
                                    monthly_chart_items if monthly_chart_items else [ft.Text("No revenue data yet", color=TEXT_LIGHT)],
                                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                ),
                            ]),
                            padding=20,
                            bgcolor=BG_CARD,
                            border_radius=15,
                            expand=True,
                        ),
                        # Order Status Distribution
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Icon(ft.Icons.PIE_CHART, size=20, color=PRIMARY_MID),
                                    ft.Text("Order Status", size=14, weight=ft.FontWeight.W_600, color=PRIMARY_DARK),
                                ], spacing=8),
                                ft.Container(height=10),
                                ft.Column(
                                    status_items if status_items else [ft.Text("No order status data", color=TEXT_LIGHT)],
                                    spacing=0,
                                ),
                            ]),
                            padding=20,
                            bgcolor=BG_CARD,
                            border_radius=15,
                            expand=True,
                        ),
                    ], spacing=15),
                    ft.Container(height=15),
                    
                    # Charts Row 3 - Top Business Owners and Top Products
                    ft.Row([
                        # Top Business Owners
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Icon(ft.Icons.LEADERBOARD, size=20, color=ACCENT_GOLD),
                                    ft.Text("Top Business Owners", size=14, weight=ft.FontWeight.W_600, color=PRIMARY_DARK),
                                ], spacing=8),
                                ft.Container(height=10),
                                ft.Column(
                                    owner_rows if owner_rows else [ft.Text("No business owners yet", color=TEXT_LIGHT)],
                                    spacing=5,
                                ),
                            ]),
                            padding=20,
                            bgcolor=BG_CARD,
                            border_radius=15,
                            expand=True,
                        ),
                        # Top Selling Products
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Icon(ft.Icons.STAR, size=20, color=PRIMARY_MID),
                                    ft.Text("Top Selling Products", size=14, weight=ft.FontWeight.W_600, color=PRIMARY_DARK),
                                ], spacing=8),
                                ft.Container(height=10),
                                ft.Column(
                                    product_rows if product_rows else [ft.Text("No product data yet", color=TEXT_LIGHT)],
                                    spacing=5,
                                ),
                            ]),
                            padding=20,
                            bgcolor=BG_CARD,
                            border_radius=15,
                            expand=True,
                        ),
                    ], spacing=15),
                ], scroll=ft.ScrollMode.AUTO, expand=True),
                padding=25,
                bgcolor=BG_LIGHT,
                expand=True,
            )
            page.update()
        
        # Manage Users Page
        def sa_manage_users():
            users = get_all_business_owners()
            
            def edit_user_clicked(user_id):
                user = get_user_by_id(user_id)
                if not user:
                    return
                
                edit_username = ft.TextField(value=user[1], label="Username", width=280, border_radius=10)
                edit_password = ft.TextField(value=user[2], label="Password", width=280, border_radius=10, password=True, can_reveal_password=True)
                edit_role = ft.Dropdown(
                    value=user[3],
                    label="Role",
                    width=280,
                    options=[
                        ft.dropdown.Option("owner", "Owner"),
                        ft.dropdown.Option("staff", "Staff"),
                    ],
                    border_radius=10,
                )
                
                def save_changes(e):
                    success, message = update_user(user_id, edit_username.value, edit_password.value, edit_role.value)
                    page.close(edit_dialog)
                    page.snack_bar = ft.SnackBar(
                        content=ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE if success else ft.Icons.ERROR, color=ACCENT_CREAM), ft.Text(message, color=ACCENT_CREAM)], spacing=10),
                        bgcolor=SUCCESS if success else ERROR
                    )
                    page.snack_bar.open = True
                    if success:
                        sa_manage_users()
                    page.update()
                
                edit_dialog = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("Edit User", weight=ft.FontWeight.BOLD, color=PRIMARY_DARK),
                    content=ft.Column([edit_username, edit_password, edit_role], spacing=15, tight=True),
                    actions=[
                        ft.TextButton("Cancel", on_click=lambda e: page.close(edit_dialog)),
                        ft.ElevatedButton("Save", bgcolor=SUCCESS, color=ACCENT_CREAM, on_click=save_changes),
                    ],
                )
                page.open(edit_dialog)
            
            def delete_user_clicked(user_id, username):
                def confirm_delete(e):
                    delete_user(user_id)
                    page.close(delete_dialog)
                    page.snack_bar = ft.SnackBar(
                        content=ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE, color=ACCENT_CREAM), ft.Text(f"User '{username}' deleted!", color=ACCENT_CREAM)], spacing=10),
                        bgcolor=SUCCESS
                    )
                    page.snack_bar.open = True
                    sa_manage_users()
                
                delete_dialog = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("Confirm Delete", color=ERROR, weight=ft.FontWeight.BOLD),
                    content=ft.Text(f"Are you sure you want to delete '{username}'?\nThis will also delete all their customers."),
                    actions=[
                        ft.TextButton("Cancel", on_click=lambda e: page.close(delete_dialog)),
                        ft.ElevatedButton("Delete", bgcolor=ERROR, color=ACCENT_CREAM, on_click=confirm_delete),
                    ],
                )
                page.open(delete_dialog)
            
            user_rows = []
            for user in users:
                uid, uname, upwd, urole, ucreated = user
                user_rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(f"#{uid}", color=PRIMARY_MID, weight=ft.FontWeight.W_600)),
                        ft.DataCell(ft.Text(uname, color=TEXT_DARK)),
                        ft.DataCell(
                            ft.Container(
                                content=ft.Text(urole.capitalize(), size=11, color=ACCENT_CREAM),
                                bgcolor=PRIMARY_MID if urole == 'owner' else PRIMARY_LIGHT,
                                padding=ft.padding.symmetric(horizontal=10, vertical=3),
                                border_radius=12,
                            )
                        ),
                        ft.DataCell(ft.Text(str(ucreated)[:10] if ucreated else "", color=TEXT_MID, size=12)),
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(icon=ft.Icons.EDIT, icon_color=PRIMARY_MID, tooltip="Edit", on_click=lambda e, u=uid: edit_user_clicked(u)),
                                ft.IconButton(icon=ft.Icons.DELETE, icon_color=ERROR, tooltip="Delete", on_click=lambda e, u=uid, n=uname: delete_user_clicked(u, n)),
                            ], spacing=0)
                        ),
                    ])
                )
            
            main_content.content = ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.MANAGE_ACCOUNTS, size=28, color=PRIMARY_MID),
                        ft.Text("Manage Users", size=26, weight=ft.FontWeight.BOLD, color=PRIMARY_DARK),
                    ], spacing=12),
                    ft.Text("View, edit, and delete business owners", size=14, color=TEXT_MID),
                    ft.Divider(height=20, color=ACCENT_CREAM),
                    
                    ft.Container(
                        content=ft.DataTable(
                            columns=[
                                ft.DataColumn(ft.Text("ID", weight=ft.FontWeight.W_600, color=PRIMARY_DARK)),
                                ft.DataColumn(ft.Text("Username", weight=ft.FontWeight.W_600, color=PRIMARY_DARK)),
                                ft.DataColumn(ft.Text("Role", weight=ft.FontWeight.W_600, color=PRIMARY_DARK)),
                                ft.DataColumn(ft.Text("Created", weight=ft.FontWeight.W_600, color=PRIMARY_DARK)),
                                ft.DataColumn(ft.Text("Actions", weight=ft.FontWeight.W_600, color=PRIMARY_DARK)),
                            ],
                            rows=user_rows,
                            border=ft.border.all(1, ACCENT_WARM),
                            border_radius=10,
                            heading_row_color=ACCENT_CREAM,
                        ),
                        bgcolor=BG_CARD,
                        padding=20,
                        border_radius=15,
                    ) if user_rows else ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.PEOPLE_OUTLINE, size=60, color=TEXT_LIGHT),
                            ft.Text("No business owners yet", size=18, color=TEXT_MID),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                        bgcolor=BG_CARD,
                        padding=50,
                        border_radius=15,
                    ),
                ], expand=True, scroll=ft.ScrollMode.AUTO),
                padding=25,
                bgcolor=BG_LIGHT,
                expand=True,
            )
            page.update()
        
        # Create Admin Page
        def sa_create_admin():
            new_admin_username = ft.TextField(
                label="Username",
                hint_text="Enter admin username",
                width=300,
                border_color=PRIMARY_LIGHT,
                focused_border_color=PRIMARY_MID,
                border_radius=10,
            )
            new_admin_password = ft.TextField(
                label="Password",
                hint_text="Enter admin password",
                width=300,
                border_color=PRIMARY_LIGHT,
                focused_border_color=PRIMARY_MID,
                border_radius=10,
                password=True,
                can_reveal_password=True,
            )
            new_admin_role = ft.Dropdown(
                label="Role",
                width=300,
                value="owner",
                options=[
                    ft.dropdown.Option("owner", "Owner (Full Admin)"),
                    ft.dropdown.Option("staff", "Staff (Limited Admin)"),
                ],
                border_radius=10,
            )
            
            def create_admin_clicked(e):
                if not new_admin_username.value or not new_admin_password.value:
                    page.snack_bar = ft.SnackBar(
                        content=ft.Row([ft.Icon(ft.Icons.ERROR, color=ACCENT_CREAM), ft.Text("Please fill in all fields", color=ACCENT_CREAM)], spacing=10),
                        bgcolor=ERROR
                    )
                    page.snack_bar.open = True
                    page.update()
                    return
                
                success, message = register_user(new_admin_username.value, new_admin_password.value, new_admin_role.value)
                if success:
                    page.snack_bar = ft.SnackBar(
                        content=ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE, color=ACCENT_CREAM), ft.Text(f"Admin '{new_admin_username.value}' created successfully!", color=ACCENT_CREAM)], spacing=10),
                        bgcolor=SUCCESS
                    )
                    new_admin_username.value = ""
                    new_admin_password.value = ""
                    new_admin_role.value = "owner"
                else:
                    page.snack_bar = ft.SnackBar(
                        content=ft.Row([ft.Icon(ft.Icons.ERROR, color=ACCENT_CREAM), ft.Text(message, color=ACCENT_CREAM)], spacing=10),
                        bgcolor=ERROR
                    )
                page.snack_bar.open = True
                page.update()
            
            main_content.content = ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.PERSON_ADD, size=28, color=PRIMARY_MID),
                        ft.Text("Create Admin", size=26, weight=ft.FontWeight.BOLD, color=PRIMARY_DARK),
                    ], spacing=12),
                    ft.Text("Create new business owner/admin accounts", size=14, color=TEXT_MID),
                    ft.Divider(height=20, color=ACCENT_CREAM),
                    
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.ADMIN_PANEL_SETTINGS, size=60, color=PRIMARY_MID),
                            ft.Text("New Admin Account", size=20, weight=ft.FontWeight.W_600, color=PRIMARY_DARK),
                            ft.Container(height=10),
                            ft.Text("Admins can:", size=14, color=TEXT_MID),
                            ft.Container(
                                content=ft.Column([
                                    ft.Row([ft.Icon(ft.Icons.CHECK, size=16, color=SUCCESS), ft.Text("Add and manage products", size=13, color=TEXT_DARK)], spacing=8),
                                    ft.Row([ft.Icon(ft.Icons.CHECK, size=16, color=SUCCESS), ft.Text("Create customer accounts", size=13, color=TEXT_DARK)], spacing=8),
                                    ft.Row([ft.Icon(ft.Icons.CHECK, size=16, color=SUCCESS), ft.Text("Process and confirm orders", size=13, color=TEXT_DARK)], spacing=8),
                                    ft.Row([ft.Icon(ft.Icons.CHECK, size=16, color=SUCCESS), ft.Text("View sales and order history", size=13, color=TEXT_DARK)], spacing=8),
                                ], spacing=5),
                                padding=ft.padding.only(left=20),
                            ),
                            ft.Container(height=20),
                            new_admin_username,
                            ft.Container(height=10),
                            new_admin_password,
                            ft.Container(height=10),
                            new_admin_role,
                            ft.Container(height=20),
                            ft.ElevatedButton(
                                "Create Admin",
                                icon=ft.Icons.PERSON_ADD,
                                bgcolor=SUCCESS,
                                color=ACCENT_CREAM,
                                width=300,
                                height=45,
                                on_click=create_admin_clicked,
                            ),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                        padding=40,
                        bgcolor=BG_CARD,
                        border_radius=20,
                        border=ft.border.all(2, ACCENT_CREAM),
                        width=450,
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO, expand=True),
                padding=25,
                bgcolor=BG_LIGHT,
                expand=True,
            )
            page.update()
        
        # Sidebar
        def sa_sidebar_button(text, icon, on_click):
            return ft.Container(
                content=ft.Row([
                    ft.Icon(icon, size=20, color=ACCENT_CREAM),
                    ft.Text(text, size=13, color=ACCENT_CREAM, weight=ft.FontWeight.W_500),
                ], spacing=12),
                padding=ft.padding.symmetric(horizontal=15, vertical=12),
                border_radius=10,
                on_click=on_click,
                on_hover=lambda e: setattr(e.control, 'bgcolor', ft.Colors.with_opacity(0.2, ACCENT_CREAM) if e.data == "true" else ft.Colors.TRANSPARENT) or page.update(),
                ink=True,
            )
        
        sidebar = ft.Container(
            bgcolor=ft.Colors.with_opacity(0.95, "#1a0a05"),
            width=250,
            padding=ft.padding.symmetric(horizontal=15, vertical=20),
            border_radius=ft.border_radius.only(top_right=20, bottom_right=20),
            content=ft.Column([
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.ADMIN_PANEL_SETTINGS, size=32, color=ERROR),
                        ft.Text("SuperAdmin", size=20, color=ACCENT_CREAM, weight=ft.FontWeight.BOLD),
                    ], spacing=10),
                    margin=ft.margin.only(bottom=10),
                ),
                ft.Divider(color=ft.Colors.with_opacity(0.3, ACCENT_CREAM)),
                ft.Container(height=15),
                ft.Text("MANAGEMENT", size=11, color=TEXT_LIGHT, weight=ft.FontWeight.W_600),
                ft.Container(height=10),
                sa_sidebar_button("Dashboard", ft.Icons.DASHBOARD_ROUNDED, lambda e: sa_dashboard()),
                ft.Container(height=5),
                sa_sidebar_button("Create Admin", ft.Icons.PERSON_ADD, lambda e: sa_create_admin()),
                ft.Container(height=5),
                sa_sidebar_button("Manage Users", ft.Icons.MANAGE_ACCOUNTS, lambda e: sa_manage_users()),
                ft.Container(expand=True),
                ft.Divider(color=ft.Colors.with_opacity(0.3, ACCENT_CREAM)),
                ft.Container(
                    content=ft.Row([
                        ft.Container(
                            content=ft.Icon(ft.Icons.SHIELD, size=20, color=ERROR),
                            bgcolor=ACCENT_CREAM,
                            border_radius=20,
                            padding=8,
                        ),
                        ft.Column([
                            ft.Text("SuperAdmin", size=13, color=ACCENT_CREAM, weight=ft.FontWeight.W_600),
                            ft.Text("Full Access", size=11, color=TEXT_LIGHT),
                        ], spacing=0),
                    ], spacing=10),
                    margin=ft.margin.symmetric(vertical=15),
                ),
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.LOGOUT_ROUNDED, size=18, color=ACCENT_CREAM),
                        ft.Text("Logout", size=13, color=ACCENT_CREAM, weight=ft.FontWeight.W_500),
                    ], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
                    padding=ft.padding.symmetric(horizontal=15, vertical=10),
                    border_radius=10,
                    bgcolor=ft.Colors.with_opacity(0.2, ERROR),
                    on_click=lambda e: layout1(),
                    on_hover=lambda e: setattr(e.control, 'bgcolor', ERROR if e.data == "true" else ft.Colors.with_opacity(0.2, ERROR)) or page.update(),
                    ink=True,
                ),
            ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.STRETCH),
        )
        
        layout = ft.Row([sidebar, main_content], expand=True, spacing=0)
        page.add(layout)
        page.update()
        sa_dashboard()

    # ============ CUSTOMER PORTAL ============
    def customer_portal(customer_id, customer_name, business_owner_id):
        page.clean()
        main_content = ft.Container(expand=True, bgcolor=BG_LIGHT)
        cart_items = []
        
        # Customer Dashboard with Best Sellers and Menu
        def cp_dashboard():
            best_sellers = get_best_sellers(business_owner_id, 3)
            all_products = get_products_for_customer(business_owner_id)
            products_list = [{"id": p[0], "name": p[1], "category": p[2], "price": p[3]} for p in all_products]
            
            # Best sellers cards
            best_seller_cards = []
            if best_sellers:
                for i, bs in enumerate(best_sellers):
                    name, category, price, sold = bs
                    medal_colors = [ACCENT_GOLD, "#C0C0C0", "#CD7F32"]  # Gold, Silver, Bronze
                    medal_icons = [ft.Icons.WORKSPACE_PREMIUM, ft.Icons.MILITARY_TECH, ft.Icons.EMOJI_EVENTS]
                    best_seller_cards.append(
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Icon(medal_icons[i], size=24, color=medal_colors[i]),
                                    ft.Text(f"#{i+1}", size=14, weight=ft.FontWeight.BOLD, color=medal_colors[i]),
                                ], alignment=ft.MainAxisAlignment.CENTER),
                                ft.Icon(ft.Icons.LOCAL_CAFE, size=40, color=PRIMARY_MID),
                                ft.Text(name, size=14, weight=ft.FontWeight.W_600, color=PRIMARY_DARK, text_align=ft.TextAlign.CENTER),
                                ft.Text(f"₱{price:.2f}", size=16, weight=ft.FontWeight.BOLD, color=SUCCESS),
                                ft.Text(f"{sold} sold", size=11, color=TEXT_LIGHT),
                                ft.ElevatedButton(
                                    "Add to Cart",
                                    bgcolor=PRIMARY_MID,
                                    color=ACCENT_CREAM,
                                    on_click=lambda e, n=name, c=category, p=price: add_to_cart(n, c, p),
                                ),
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                            padding=20,
                            bgcolor=BG_CARD,
                            border_radius=15,
                            border=ft.border.all(2, medal_colors[i]),
                            width=160,
                        )
                    )
            else:
                best_seller_cards.append(ft.Text("No best sellers yet - be the first to order!", color=TEXT_MID))
            
            def add_to_cart(name, category, price):
                # Check if item already in cart
                for item in cart_items:
                    if item['name'] == name:
                        item['quantity'] += 1
                        page.snack_bar = ft.SnackBar(
                            content=ft.Row([ft.Icon(ft.Icons.ADD_SHOPPING_CART, color=ACCENT_CREAM), ft.Text(f"Added another {name} to cart!", color=ACCENT_CREAM)], spacing=10),
                            bgcolor=SUCCESS, duration=1500,
                        )
                        page.snack_bar.open = True
                        page.update()
                        return
                
                cart_items.append({"name": name, "category": category, "price": price, "quantity": 1})
                page.snack_bar = ft.SnackBar(
                    content=ft.Row([ft.Icon(ft.Icons.ADD_SHOPPING_CART, color=ACCENT_CREAM), ft.Text(f"{name} added to cart!", color=ACCENT_CREAM)], spacing=10),
                    bgcolor=SUCCESS, duration=1500,
                )
                page.snack_bar.open = True
                page.update()
            
            # Product grid
            product_cards = []
            for product in products_list:
                product_cards.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.LOCAL_CAFE if product['category'] == 'Coffee' else ft.Icons.CAKE, size=32, color=PRIMARY_LIGHT),
                            ft.Text(product['name'], size=13, weight=ft.FontWeight.W_500, color=TEXT_DARK, text_align=ft.TextAlign.CENTER),
                            ft.Container(
                                content=ft.Text(product['category'], size=10, color=ACCENT_CREAM),
                                bgcolor=PRIMARY_LIGHT if product['category'] == 'Coffee' else ACCENT_GOLD,
                                padding=ft.padding.symmetric(horizontal=8, vertical=2),
                                border_radius=8,
                            ),
                            ft.Text(f"₱{product['price']:.2f}", size=14, weight=ft.FontWeight.BOLD, color=SUCCESS),
                            ft.IconButton(
                                icon=ft.Icons.ADD_CIRCLE,
                                icon_color=PRIMARY_MID,
                                icon_size=28,
                                on_click=lambda e, n=product['name'], c=product['category'], p=product['price']: add_to_cart(n, c, p),
                            ),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=3),
                        padding=15,
                        bgcolor=BG_CARD,
                        border_radius=12,
                        border=ft.border.all(1, ACCENT_CREAM),
                        width=140,
                    )
                )
            
            main_content.content = ft.Container(
                content=ft.Column([
                    # Welcome Header
                    ft.Row([
                        ft.Icon(ft.Icons.WAVING_HAND, size=28, color=ACCENT_WARM),
                        ft.Text(f"Welcome, {customer_name}!", size=24, weight=ft.FontWeight.BOLD, color=PRIMARY_DARK),
                    ], spacing=12),
                    ft.Text("Browse our menu and place your order", size=14, color=TEXT_MID),
                    ft.Divider(height=20, color=ACCENT_CREAM),
                    
                    # Best Sellers Section
                    ft.Text("🏆 Best Sellers - Top 3 Coffees", size=18, weight=ft.FontWeight.W_600, color=PRIMARY_DARK),
                    ft.Container(height=10),
                    ft.Row(best_seller_cards, spacing=15, scroll=ft.ScrollMode.AUTO),
                    ft.Container(height=25),
                    
                    # Menu Section
                    ft.Text("📋 Full Menu", size=18, weight=ft.FontWeight.W_600, color=PRIMARY_DARK),
                    ft.Container(height=10),
                    ft.Container(
                        content=ft.Row(
                            product_cards,
                            spacing=15,
                            wrap=True,
                            scroll=ft.ScrollMode.AUTO,
                        ),
                        expand=True,
                    ),
                ], scroll=ft.ScrollMode.AUTO, expand=True),
                padding=25,
                bgcolor=BG_LIGHT,
                expand=True,
            )
            page.update()
        
        # Cart Page
        def cp_cart():
            def update_cart_display():
                if not cart_items:
                    main_content.content = ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.SHOPPING_CART_OUTLINED, size=80, color=TEXT_LIGHT),
                            ft.Text("Your cart is empty", size=20, color=TEXT_MID),
                            ft.Text("Add items from the menu to get started", size=14, color=TEXT_LIGHT),
                            ft.ElevatedButton("Browse Menu", bgcolor=PRIMARY_MID, color=ACCENT_CREAM, on_click=lambda e: cp_dashboard()),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15, alignment=ft.MainAxisAlignment.CENTER),
                        padding=50,
                        bgcolor=BG_LIGHT,
                        expand=True,
                        alignment=ft.alignment.center,
                    )
                    page.update()
                    return
                
                cart_list = []
                total = 0
                for item in cart_items:
                    item_total = item['price'] * item['quantity']
                    total += item_total
                    
                    def make_remove(itm):
                        def remove(e):
                            cart_items.remove(itm)
                            update_cart_display()
                        return remove
                    
                    def make_qty_change(itm, delta):
                        def change(e):
                            itm['quantity'] = max(1, itm['quantity'] + delta)
                            update_cart_display()
                        return change
                    
                    cart_list.append(
                        ft.Container(
                            content=ft.Row([
                                ft.Icon(ft.Icons.LOCAL_CAFE if item['category'] == 'Coffee' else ft.Icons.CAKE, size=28, color=PRIMARY_MID),
                                ft.Column([
                                    ft.Text(item['name'], size=14, weight=ft.FontWeight.W_500, color=TEXT_DARK),
                                    ft.Text(f"₱{item['price']:.2f} each", size=12, color=TEXT_MID),
                                ], spacing=0, expand=True),
                                ft.Row([
                                    ft.IconButton(icon=ft.Icons.REMOVE_CIRCLE_OUTLINE, icon_size=20, on_click=make_qty_change(item, -1)),
                                    ft.Text(str(item['quantity']), size=14, weight=ft.FontWeight.W_600),
                                    ft.IconButton(icon=ft.Icons.ADD_CIRCLE_OUTLINE, icon_size=20, on_click=make_qty_change(item, 1)),
                                ], spacing=0),
                                ft.Text(f"₱{item_total:.2f}", size=14, weight=ft.FontWeight.W_600, color=SUCCESS),
                                ft.IconButton(icon=ft.Icons.DELETE, icon_color=ERROR, icon_size=20, on_click=make_remove(item)),
                            ], spacing=10),
                            padding=15,
                            bgcolor=BG_CARD,
                            border_radius=10,
                            border=ft.border.all(1, ACCENT_CREAM),
                        )
                    )
                
                def place_order(e):
                    if not cart_items:
                        return
                    
                    order_id = place_customer_order(
                        customer_id, customer_name, business_owner_id,
                        "Dine in", total, cart_items
                    )
                    cart_items.clear()
                    
                    page.snack_bar = ft.SnackBar(
                        content=ft.Row([
                            ft.Icon(ft.Icons.CHECK_CIRCLE, color=ACCENT_CREAM, size=24),
                            ft.Text(f"Order #{order_id} placed successfully! Waiting for confirmation.", color=ACCENT_CREAM),
                        ], spacing=10),
                        bgcolor=SUCCESS,
                        duration=4000,
                    )
                    page.snack_bar.open = True
                    cp_order_history()
                
                main_content.content = ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.SHOPPING_CART, size=28, color=PRIMARY_MID),
                            ft.Text("Your Cart", size=24, weight=ft.FontWeight.BOLD, color=PRIMARY_DARK),
                        ], spacing=12),
                        ft.Divider(height=20, color=ACCENT_CREAM),
                        
                        ft.Container(
                            content=ft.Column(cart_list, spacing=10, scroll=ft.ScrollMode.AUTO),
                            expand=True,
                        ),
                        
                        ft.Divider(height=15, color=ACCENT_WARM),
                        ft.Row([
                            ft.Text("Total:", size=20, weight=ft.FontWeight.BOLD, color=PRIMARY_DARK),
                            ft.Container(expand=True),
                            ft.Text(f"₱{total:.2f}", size=24, weight=ft.FontWeight.BOLD, color=SUCCESS),
                        ]),
                        ft.Container(height=15),
                        ft.ElevatedButton(
                            "Place Order",
                            icon=ft.Icons.SEND,
                            width=250,
                            height=50,
                            bgcolor=SUCCESS,
                            color=ACCENT_CREAM,
                            on_click=place_order,
                        ),
                    ], expand=True),
                    padding=25,
                    bgcolor=BG_LIGHT,
                    expand=True,
                )
                page.update()
            
            update_cart_display()
        
        # Order History
        def cp_order_history():
            orders = get_customer_orders(customer_id)
            
            def view_details(order_id, total):
                items = get_order_items(order_id)
                items_list = []
                for item in items:
                    name, cat, price, qty = item
                    items_list.append(
                        ft.Container(
                            content=ft.Row([
                                ft.Text(name, size=13, color=TEXT_DARK, expand=True),
                                ft.Text(f"x{qty}", size=12, color=TEXT_MID),
                                ft.Text(f"₱{price * qty:.2f}", size=13, color=PRIMARY_MID),
                            ]),
                            padding=ft.padding.symmetric(vertical=6),
                            border=ft.border.only(bottom=ft.BorderSide(1, ACCENT_CREAM)),
                        )
                    )
                
                dialog = ft.AlertDialog(
                    modal=True,
                    title=ft.Text(f"Order #{order_id}", weight=ft.FontWeight.BOLD, color=PRIMARY_DARK),
                    content=ft.Container(
                        content=ft.Column([
                            ft.Column(items_list, spacing=0),
                            ft.Divider(color=ACCENT_WARM),
                            ft.Row([ft.Text("Total:", weight=ft.FontWeight.BOLD), ft.Container(expand=True), ft.Text(f"₱{total:.2f}", weight=ft.FontWeight.BOLD, color=SUCCESS)]),
                        ], spacing=10),
                        width=300,
                    ),
                    actions=[ft.ElevatedButton("Close", bgcolor=PRIMARY_MID, color=ACCENT_CREAM, on_click=lambda e: page.close(dialog))],
                )
                page.open(dialog)
            
            order_rows = []
            for order in orders:
                oid, cname, otype, total, status, payment, odate = order
                status_color = {'pending': ACCENT_GOLD, 'confirmed': PRIMARY_LIGHT, 'completed': SUCCESS, 'cancelled': ERROR}.get(status, TEXT_MID)
                payment_color = SUCCESS if payment == 'paid' else ERROR
                
                order_rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(f"#{oid}", color=PRIMARY_MID, weight=ft.FontWeight.W_600)),
                        ft.DataCell(ft.Container(content=ft.Text(status.capitalize(), size=11, color=ACCENT_CREAM), bgcolor=status_color, padding=ft.padding.symmetric(horizontal=8, vertical=2), border_radius=10)),
                        ft.DataCell(ft.Container(content=ft.Text(payment.capitalize(), size=11, color=ACCENT_CREAM), bgcolor=payment_color, padding=ft.padding.symmetric(horizontal=8, vertical=2), border_radius=10)),
                        ft.DataCell(ft.Text(f"₱{total:.2f}", color=TEXT_DARK, weight=ft.FontWeight.W_500)),
                        ft.DataCell(ft.Text(str(odate)[:16] if odate else "", color=TEXT_MID, size=11)),
                        ft.DataCell(ft.IconButton(icon=ft.Icons.VISIBILITY, icon_color=PRIMARY_LIGHT, on_click=lambda e, o=oid, t=total: view_details(o, t))),
                    ])
                )
            
            main_content.content = ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.HISTORY, size=28, color=PRIMARY_MID),
                        ft.Text("Order History", size=24, weight=ft.FontWeight.BOLD, color=PRIMARY_DARK),
                    ], spacing=12),
                    ft.Text("View your past orders and their status", size=14, color=TEXT_MID),
                    ft.Divider(height=20, color=ACCENT_CREAM),
                    
                    ft.Container(
                        content=ft.DataTable(
                            columns=[
                                ft.DataColumn(ft.Text("Order", weight=ft.FontWeight.W_600, color=PRIMARY_DARK)),
                                ft.DataColumn(ft.Text("Status", weight=ft.FontWeight.W_600, color=PRIMARY_DARK)),
                                ft.DataColumn(ft.Text("Payment", weight=ft.FontWeight.W_600, color=PRIMARY_DARK)),
                                ft.DataColumn(ft.Text("Total", weight=ft.FontWeight.W_600, color=PRIMARY_DARK)),
                                ft.DataColumn(ft.Text("Date", weight=ft.FontWeight.W_600, color=PRIMARY_DARK)),
                                ft.DataColumn(ft.Text("", weight=ft.FontWeight.W_600, color=PRIMARY_DARK)),
                            ],
                            rows=order_rows,
                            border=ft.border.all(1, ACCENT_WARM),
                            border_radius=10,
                            heading_row_color=ACCENT_CREAM,
                        ),
                        bgcolor=BG_CARD,
                        padding=20,
                        border_radius=15,
                    ) if order_rows else ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.RECEIPT_LONG, size=60, color=TEXT_LIGHT),
                            ft.Text("No orders yet", size=18, color=TEXT_MID),
                            ft.ElevatedButton("Start Ordering", bgcolor=PRIMARY_MID, color=ACCENT_CREAM, on_click=lambda e: cp_dashboard()),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                        bgcolor=BG_CARD,
                        padding=50,
                        border_radius=15,
                    ),
                ], expand=True, scroll=ft.ScrollMode.AUTO),
                padding=25,
                bgcolor=BG_LIGHT,
                expand=True,
            )
            page.update()
        
        # Customer Sidebar
        def cp_sidebar_btn(text, icon, on_click):
            return ft.Container(
                content=ft.Row([ft.Icon(icon, size=20, color=ACCENT_CREAM), ft.Text(text, size=13, color=ACCENT_CREAM, weight=ft.FontWeight.W_500)], spacing=12),
                padding=ft.padding.symmetric(horizontal=15, vertical=12),
                border_radius=10,
                on_click=on_click,
                on_hover=lambda e: setattr(e.control, 'bgcolor', ft.Colors.with_opacity(0.2, ACCENT_CREAM) if e.data == "true" else ft.Colors.TRANSPARENT) or page.update(),
                ink=True,
            )
        
        sidebar = ft.Container(
            bgcolor=PRIMARY_DARK,
            width=240,
            padding=ft.padding.symmetric(horizontal=15, vertical=20),
            border_radius=ft.border_radius.only(top_right=20, bottom_right=20),
            content=ft.Column([
                ft.Container(
                    content=ft.Row([ft.Icon(ft.Icons.LOCAL_CAFE, size=28, color=ACCENT_WARM), ft.Text("Coffeestry", size=18, color=ACCENT_CREAM, weight=ft.FontWeight.BOLD)], spacing=10),
                    margin=ft.margin.only(bottom=10),
                ),
                ft.Divider(color=ft.Colors.with_opacity(0.3, ACCENT_CREAM)),
                ft.Container(height=15),
                ft.Text("MENU", size=11, color=TEXT_LIGHT, weight=ft.FontWeight.W_600),
                ft.Container(height=10),
                cp_sidebar_btn("Browse Menu", ft.Icons.RESTAURANT_MENU, lambda e: cp_dashboard()),
                ft.Container(height=5),
                cp_sidebar_btn("My Cart", ft.Icons.SHOPPING_CART, lambda e: cp_cart()),
                ft.Container(height=5),
                cp_sidebar_btn("Order History", ft.Icons.HISTORY, lambda e: cp_order_history()),
                ft.Container(expand=True),
                ft.Divider(color=ft.Colors.with_opacity(0.3, ACCENT_CREAM)),
                ft.Container(
                    content=ft.Row([
                        ft.Container(content=ft.Icon(ft.Icons.PERSON, size=18, color=PRIMARY_DARK), bgcolor=ACCENT_WARM, border_radius=18, padding=6),
                        ft.Column([ft.Text(customer_name, size=12, color=ACCENT_CREAM, weight=ft.FontWeight.W_600), ft.Text("Customer", size=10, color=TEXT_LIGHT)], spacing=0),
                    ], spacing=10),
                    margin=ft.margin.symmetric(vertical=15),
                ),
                ft.Container(
                    content=ft.Row([ft.Icon(ft.Icons.LOGOUT_ROUNDED, size=18, color=ACCENT_CREAM), ft.Text("Logout", size=13, color=ACCENT_CREAM)], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
                    padding=ft.padding.symmetric(horizontal=15, vertical=10),
                    border_radius=10,
                    bgcolor=ft.Colors.with_opacity(0.2, ERROR),
                    on_click=lambda e: layout1(),
                    on_hover=lambda e: setattr(e.control, 'bgcolor', ERROR if e.data == "true" else ft.Colors.with_opacity(0.2, ERROR)) or page.update(),
                    ink=True,
                ),
            ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.STRETCH),
        )
        
        layout = ft.Row([sidebar, main_content], expand=True, spacing=0)
        page.add(layout)
        page.update()
        cp_dashboard()

    # START
    layout1()

ft.app(target=main)