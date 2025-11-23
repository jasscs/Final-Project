import flet as ft
from database import get_connection, add_product, get_products, delete_product

def main(page: ft.Page):
    page.title = "Coffeestry System"
    page.bgcolor = ft.Colors.BROWN_100
    page.window_maximized = True
    page.window_resizable = True
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.appbar = ft.AppBar(
        title=ft.Text("Coffeestry System", size=18, color=ft.Colors.WHITE),
        center_title=True,
        bgcolor=ft.Colors.BROWN_700,
    )

    # ----------------------
    # HOME SCREEN
    # ----------------------
    def show_home():
        page.clean()

        bg_image = ft.Container(
            content=ft.Image(src="coffebg.png", fit=ft.ImageFit.COVER, opacity=0.25),
            expand=True,
        )

        home_content = ft.Column(
            [
                ft.Container(
                    content=ft.Image(src="logo.png", width=300, height=300, fit=ft.ImageFit.CONTAIN),
                    alignment=ft.alignment.top_center,
                    margin=ft.margin.only(top=5, bottom=5),
                ),
                ft.Text("Welcome to Coffeestry", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.BROWN_900),
                ft.Text("Your cozy coffee shop system", size=16, color=ft.Colors.BROWN_600),
                ft.Container(
                    content=ft.ElevatedButton(
                        "Login", on_click=lambda e: show_login(),
                        bgcolor=ft.Colors.BROWN_500, color=ft.Colors.WHITE, width=220
                    ),
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    content=ft.ElevatedButton(
                        "About", on_click=lambda e: show_about(),
                        bgcolor=ft.Colors.BROWN_300, width=220
                    ),
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    content=ft.ElevatedButton(
                        "Exit", on_click=lambda e: page.window_close(),
                        bgcolor=ft.Colors.BROWN_700, color=ft.Colors.WHITE, width=220
                    ),
                    alignment=ft.alignment.center,
                ),
                ft.Text("© 2025 Coffeestry", size=12, color=ft.Colors.BROWN_400,
                        italic=True, text_align=ft.TextAlign.CENTER),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=15,
        )

        page.add(
            ft.Stack([
                bg_image,
                ft.Container(content=home_content, alignment=ft.alignment.center, expand=True)
            ])
        )

    # ----------------------
    # ABOUT SCREEN
    # ----------------------
    def show_about():
        page.clean()
        page.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("About Coffeestry", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BROWN_800),
                        ft.Text(
                            "Coffeestry is a coffee shop that serves fresh brewed coffee and freshly baked pastries.\n"
                            "Coffeestry aims to provide a cozy and inviting atmosphere for coffee and pastry lovers.",
                            size=14, color=ft.Colors.BROWN_700, text_align=ft.TextAlign.CENTER,
                        ),
                        ft.ElevatedButton(
                            "Back", on_click=lambda e: show_home(),
                            width=200, bgcolor=ft.Colors.BROWN_500, color=ft.Colors.WHITE
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=15,
                ),
                alignment=ft.alignment.center,
                expand=True,
            )
        )

    # ----------------------
    # LOGIN SCREEN
    # ----------------------
    def show_login():
        page.clean()

        username_field = ft.TextField(label="Username", width=300, color=ft.Colors.BROWN_900)
        password_field = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300, color=ft.Colors.BROWN_900)
        message = ft.Text(value="", color=ft.Colors.RED_700)

        def login_clicked(e):
            username = username_field.value
            password = password_field.value

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
            result = cursor.fetchone()
            conn.close()

            if result:
                role = result[0].lower()
                message.value = f"Welcome, {role.capitalize()}!"
                message.color = ft.Colors.GREEN_700
                page.update()

                if role == "owner":
                    show_owner_dashboard()
                else:
                    page.snack_bar = ft.SnackBar(ft.Text("Redirecting to Staff Dashboard..."))
                    page.snack_bar.open = True
            else:
                message.value = "Invalid username or password!"
                message.color = ft.Colors.RED_700
                page.update()

        login_button = ft.ElevatedButton("Login", on_click=login_clicked, width=300, bgcolor=ft.Colors.BROWN_500, color=ft.Colors.WHITE)
        back_button = ft.OutlinedButton("Back", on_click=lambda e: show_home(), width=300)

        page.add(
            ft.Container(
                content=ft.Row(
                    [
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Login to Coffeestry", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BROWN_800),
                                    username_field,
                                    password_field,
                                    login_button,
                                    back_button,
                                    message,
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=10,
                            ),
                            padding=30,
                            width=350,
                            bgcolor=ft.Colors.WHITE,
                            border_radius=15,
                            shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.GREY_400),
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True,
                ),
                expand=True,
            )
        )

    # ----------------------
    # OWNER DASHBOARD
    # ----------------------
    def show_owner_dashboard():
        page.clean()
        main_content = ft.Container(expand=True)

        # ----------------------
        # DASHBOARD PAGE
        # ----------------------
        def show_dashboard_page():

            def order_type_changed(e):
                if e.control:
                    print("Selected Order Type:", e.control.value)

            owner_title = ft.Text("Making Orders", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BROWN_900)

            products = [
                {"name": "Espresso", "category": "Coffee", "price": 120.00},
                {"name": "Cappuccino", "category": "Coffee", "price": 150.00},
                {"name": "Latte", "category": "Coffee", "price": 160.00},
                {"name": "Blueberry Muffin", "category": "Pastry", "price": 80.00},
                {"name": "Chocolate Croissant", "category": "Pastry", "price": 90.00},
            ]

            cart_items = []

            cart_table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Product", color=ft.Colors.BROWN_700)),
                    ft.DataColumn(ft.Text("Category", color=ft.Colors.BROWN_700)),
                    ft.DataColumn(ft.Text("Price", color=ft.Colors.BROWN_700)),
                    ft.DataColumn(ft.Text("Quantity", color=ft.Colors.BROWN_700)),
                    ft.DataColumn(ft.Text("Add", color=ft.Colors.BROWN_700)),
                ],
                rows=[]
            )

            total_text = ft.Text("Total: 0.00", size=16, color=ft.Colors.BROWN_900)

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
                            ft.DataCell(ft.Text(item["name"])),
                            ft.DataCell(ft.Text(item["category"])),
                            ft.DataCell(ft.Text(f"{item['price']:.2f}")),
                            ft.DataCell(ft.Text(str(item["quantity"]))),
                            ft.DataCell(ft.Text(f"{total_item:.2f}")),
                            ft.DataCell(ft.IconButton(ft.Icons.DELETE, on_click=remove_item))
                        ])
                    )
                cart_table.rows = rows
                total_text.value = f"Total: {total:.2f}"
                page.update()

            product_rows = []
            for product in products:
                qty_field = ft.TextField(width=50, value="1", keyboard_type=ft.KeyboardType.NUMBER)

                def add_to_cart(e, p=product, qty_field=qty_field):
                    try:
                        qty = int(qty_field.value)
                        if qty <= 0:
                            raise ValueError

                        cart_items.append({
                            "name": p["name"],
                            "category": p["category"],
                            "price": p["price"],
                            "quantity": qty
                        })
                        update_cart_table()
                    except ValueError:
                        page.snack_bar = ft.SnackBar(ft.Text("Only positive number for Quantity"))
                        page.snack_bar.open = True
                        page.update()
                
                product_rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(product["name"])),
                        ft.DataCell(ft.Text(product["category"])),
                        ft.DataCell(ft.Text(f"{product['price']:.2f}")),
                        ft.DataCell(qty_field),
                        ft.DataCell(ft.IconButton(ft.Icons.ADD, on_click=add_to_cart))
                    ])
                )

            product_table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Product", color=ft.Colors.BROWN_700)),
                    ft.DataColumn(ft.Text("Category", color=ft.Colors.BROWN_700)),
                    ft.DataColumn(ft.Text("Price", color=ft.Colors.BROWN_700)),
                    ft.DataColumn(ft.Text("Quantity", color=ft.Colors.BROWN_700)),
                    ft.DataColumn(ft.Text("Add", color=ft.Colors.BROWN_700)),
                ],
                rows=product_rows
            )

            dashboard_section = ft.Container(
                bgcolor=ft.Colors.WHITE,
                padding=20,
                border_radius=10,
                border=ft.border.all(1, ft.Colors.BROWN_200),
                content=ft.Column(
                [
                    ft.Row(
                        spacing=100,
                        controls=[
                            ft.Text("Customer Name", size=15, color=ft.Colors.BROWN_900),
                            ft.Text("Order Date", size=15, color=ft.Colors.BROWN_900),
                        ]
                    ),
                    # INPUT FIELDS
                    ft.Row(
                        spacing=60,
                        controls=[
                            ft.TextField(hint_text="Enter customer name", bgcolor=ft.Colors.WHITE, color=ft.Colors.BROWN_900, border_radius=5, width=200, filled=True),
                            ft.TextField(hint_text="Enter Order Date", bgcolor=ft.Colors.WHITE, color=ft.Colors.BROWN_900, border_radius=5, width=200, filled=True),
                        ]
                    ),
                    ft.Text("Order Type", size=15, color=ft.Colors.BROWN_900),
                    
                    ft.Row(
                        spacing=60,
                        controls=[
                            ft.Dropdown(
                                width=200,
                                color=ft.Colors.BROWN_600,
                                value="Dine in",
                                bgcolor=ft.Colors.WHITE,
                                border=ft.InputBorder.OUTLINE,
                                options=[
                                    ft.dropdown.Option("Dine in"),
                                    ft.dropdown.Option("Take out"),
                                ],
                                on_change=order_type_changed
                            ),
                        ]
                    ),
                    
                    ft.Row(
                        spacing=60,
                        controls=[
                            ft.TextField(hint_text="Search Product...", color=ft.Colors.BROWN_900, bgcolor=ft.Colors.WHITE, border=ft.InputBorder.OUTLINE, border_radius=5, width=200, filled=True),
                            ft.Dropdown(
                                width=200,
                                border=ft.InputBorder.OUTLINE,
                                border_radius=5,
                                hint_text="Category",
                                bgcolor=ft.Colors.WHITE,
                                color=ft.Colors.BROWN_900,
                                options=[
                                    ft.dropdown.Option("Coffee"),
                                    ft.dropdown.Option("Pastry"),
                                ]
                            ),
                        ]
                    ),
                    
                    ft.Divider(height=20, color=ft.Colors.BROWN_200),
                    product_table,
                    ft.Divider(height=20, color=ft.Colors.BROWN_200),
                    cart_table,
                    ft.Divider(height=20, color=ft.Colors.BROWN_200),
                    total_text,
                ],
                spacing=15,
            )
            )
            
                


            dashboard_view = ft.Column(
                [
                    owner_title,
                    dashboard_section,
                ],
                spacing=20,
                scroll=ft.ScrollMode.AUTO
            )

            main_content.content = ft.Container(
                padding=20,
                bgcolor=ft.Colors.BROWN_100,
                content=dashboard_view
            )
            page.update()

        # ----------------------
        # PRODUCT MANAGEMENT
        #NEED SOME CHANGES PA HEREEEEE
        # ----------------------
        def show_product_management_page():
            title = ft.Text(
                "Product and Price Management",
                size=22,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BROWN_900,
            )

            search_field = ft.TextField(
                hint_text="Search products...",
                prefix_icon=ft.Icons.SEARCH,
                width=400,
                bgcolor=ft.Colors.WHITE,
            )

            table_container = ft.Container(
                bgcolor=ft.Colors.WHITE,
                padding=15,
                border_radius=10,
                border=ft.border.all(1, ft.Colors.BROWN_300),
            )

            # REFRESH PRODUCTS
             #NEED SOME CHANGES PA HEREEEEE

            def refresh_products():
                products = get_products()
                rows = []

                for p in products:
                    product_id, name, category, price = p
                    rows.append(
                        ft.Row(
                            [
                                ft.Text(name, width=150, color=ft.Colors.BROWN_800),
                                ft.Text(category, width=150, color=ft.Colors.BROWN_800),
                                ft.Text(f"{price:.2f}", width=100, color=ft.Colors.BROWN_800),
                                ft.Row([
                                    ft.ElevatedButton("Edit", width=70, bgcolor=ft.Colors.BROWN_400, color=ft.Colors.WHITE),
                                    ft.ElevatedButton(
                                        "Delete",
                                        width=70,
                                        bgcolor=ft.Colors.RED_400,
                                        color=ft.Colors.WHITE,
                                        on_click=lambda e, pid=product_id: delete_product(pid) or refresh_products()
                                    ),
                                ], spacing=5),
                            ]
                        )
                    )

                table_container.content = ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text("Product", weight=ft.FontWeight.BOLD, width=150, color=ft.Colors.BROWN_900),
                                ft.Text("Category", weight=ft.FontWeight.BOLD, width=150, color=ft.Colors.BROWN_900),
                                ft.Text("Price (₱)", weight=ft.FontWeight.BOLD, width=100, color=ft.Colors.BROWN_900),
                                ft.Text("Action", weight=ft.FontWeight.BOLD, width=150, color=ft.Colors.BROWN_900),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        *rows
                    ],
                    spacing=8,
                )
                page.update()

            # ADD PRODUCT DIALOG
            #WALA PA MAN ITONG FUNCTION
            def show_add_product_dialog(e):
                name_field = ft.TextField(label="Product Name", width=300)
                category_field = ft.TextField(label="Category", width=300)
                price_field = ft.TextField(label="Price (₱)", width=300, keyboard_type=ft.KeyboardType.NUMBER)

                def add_to_db(ev):
                    if not name_field.value.strip() or not category_field.value.strip() or not price_field.value.strip():
                        page.snack_bar = ft.SnackBar(ft.Text("All fields are required!"))
                        page.snack_bar.open = True
                        page.update()
                        return

                    try:
                        add_product(name_field.value.strip(), category_field.value.strip(), float(price_field.value.strip()))
                        page.dialog.open = False
                        refresh_products()
                    except ValueError:
                        page.snack_bar = ft.SnackBar(ft.Text("Price must be a number!"))
                        page.snack_bar.open = True
                    page.update()

                page.dialog = ft.AlertDialog(
                    title=ft.Text("Add New Product"),
                    content=ft.Column([name_field, category_field, price_field], spacing=10),
                    actions=[
                        ft.ElevatedButton("Add", on_click=add_to_db, bgcolor=ft.Colors.BROWN_500, color=ft.Colors.WHITE),
                        ft.TextButton("Cancel", on_click=lambda ev: setattr(page.dialog, "open", False) or page.update()),
                    ],
                )
                page.dialog.open = True
                page.update()

            add_button = ft.IconButton(
                icon=ft.Icons.ADD,
                tooltip="Add new product",
                icon_color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BROWN_700,
                on_click=show_add_product_dialog,
            )

            search_row = ft.Row([search_field, add_button], spacing=10)

            product_management_view = ft.Column(
                [title, search_row, table_container],
                spacing=20,
                scroll=ft.ScrollMode.AUTO,
            )

            main_content.content = ft.Container(
                padding=20,
                bgcolor=ft.Colors.BROWN_100,
                content=product_management_view,
            )
            page.update()
            refresh_products()

        # ----------------------
        # SIDEBAR
        # ----------------------
        sidebar = ft.Container(
            bgcolor=ft.Colors.BROWN_600,
            width=220,
            padding=15,
            content=ft.Column(
                [
                    ft.Text("Coffeestry", size=24, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                    ft.Divider(color=ft.Colors.BROWN_300, thickness=1),
                    ft.ElevatedButton(
                        "Dashboard",
                        icon=ft.Icons.DASHBOARD,
                        bgcolor=ft.Colors.BROWN_300,
                        color=ft.Colors.BROWN_900,
                        width=190,
                        on_click=lambda e: show_dashboard_page(),
                    ),
                    ft.ElevatedButton(
                        "Products and Price Management",
                        icon=ft.Icons.INVENTORY,
                        width=190,
                        bgcolor=ft.Colors.BROWN_500,
                        color=ft.Colors.WHITE,
                        on_click=lambda e: show_product_management_page(),
                    ),
                    ft.ElevatedButton(
                        "Financial Reports",
                        icon=ft.Icons.ASSESSMENT,
                        width=190,
                        bgcolor=ft.Colors.BROWN_500,
                        color=ft.Colors.WHITE,
                    ),
                    ft.ElevatedButton(
                        "Inventory & Supplier Management",
                        icon=ft.Icons.STORE,
                        width=190,
                        bgcolor=ft.Colors.BROWN_500,
                        color=ft.Colors.WHITE,
                    ),
                    ft.ElevatedButton(
                        "User Management",
                        icon=ft.Icons.MANAGE_ACCOUNTS,
                        width=190,
                        bgcolor=ft.Colors.BROWN_500,
                        color=ft.Colors.WHITE,
                    ),
                    ft.Container(expand=True),
                    ft.ElevatedButton(
                        "Logout",
                        icon=ft.Icons.LOGOUT,
                        bgcolor=ft.Colors.GREY_400,
                        color=ft.Colors.BROWN_900,
                        width=190,
                        on_click=lambda e: show_home(),
                    ),

                    #LOG OUT BUTTON KAILANGAN MAY FUNCTION NA SIYA
                ],
                spacing=15,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

        layout = ft.Row([sidebar, main_content], expand=True)
        page.add(layout)

        show_dashboard_page()

    # ----------------------
    # START
    # ----------------------
    show_home()

ft.app(target=main)