import flet as ft 
from database import get_connection, add_product, delete_product
from flet import TextField, ElevatedButton, Text, Row, Column
from prod import products
 

def main(page: ft.Page): #THE BROWN ONE IN THE TOP
    page.title = "Coffeestry System"
    page.bgcolor = ft.Colors.BROWN_100
    page.window_maximized = True
    page.window_resizable = True
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.appbar = ft.AppBar(
        title=ft.Text("Coffeestry System", size=15, color=ft.Colors.BROWN_50),
        center_title=True,
        bgcolor=ft.Colors.BROWN_500,
    )
    
    # HOME PAGE
    def layout1():
        page.clean()

        main_container = ft.Container(expand=True,bgcolor=ft.Colors.BROWN_200)

        page.add(main_container)    

        home_content = ft.Column(
            [
                ft.Container(
                    content=ft.Image(src="logo.png", width=400, height=300, fit=ft.ImageFit.CONTAIN),
                    alignment=ft.alignment.top_center,
                    margin=ft.margin.only(top=5, bottom=5),
                ),
                ft.Text("Welcome to Coffeestry", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.BROWN_900),
                ft.Text("Your cozy coffee shop system", size=16, color=ft.Colors.BROWN_600),
                ft.Container(
                    content=ft.ElevatedButton(
                        "Login", on_click=lambda e: layout3(),
                        bgcolor=ft.Colors.BROWN_400, color=ft.Colors.WHITE, width=250
                    ),
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    content=ft.ElevatedButton(
                        "About", on_click=lambda e: layout2(),
                        bgcolor=ft.Colors.BROWN_500, color=ft.Colors.WHITE, width=250
                    ),
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    content=ft.ElevatedButton(
                        "Exit", on_click=lambda e: page.window_close(),
                        bgcolor=ft.Colors.BROWN_600, color=ft.Colors.WHITE, width=250
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
        main_container.content = home_content
        page.update()


    # ABOUT COFFEESTRY PAGE
    def layout2():
        page.clean()
        page.add(
    ft.Container(
        content=ft.Column(
            [
                ft.Icon(ft.Icons.LOCAL_CAFE, size=60, color=ft.Colors.BROWN_700),
                ft.Text(
                    "About Coffeestry",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BROWN_900
                ),
                ft.Text(
                    "Coffeestry is a coffee shop that serves freshly brewed coffee and freshly baked pastries.\n"
                    "We aim to provide a cozy and inviting atmosphere for coffee and pastry lovers.",
                    size=16,
                    color=ft.Colors.BROWN_800,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.ElevatedButton(
                    "Back",
                    on_click=lambda e: layout1(),
                    width=200,
                    bgcolor=ft.Colors.BROWN_500,
                    color=ft.Colors.WHITE,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12))
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        ),
        padding=30,
        margin=20,
        border_radius=25,
        bgcolor=ft.Colors.BROWN_100,
        alignment=ft.alignment.center,
        expand=True,
        shadow=ft.BoxShadow(
            color=ft.Colors.BROWN_200, blur_radius=15, offset=ft.Offset(5, 5)
        ),
    )
)
   
    # LOGIN PAGE (need to create user roles in the database)
    def layout3():
        page.clean()

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
                    layout4()
                else:
                    page.snack_bar = ft.SnackBar(ft.Text("Redirecting to Staff Dashboard..."))
                    page.snack_bar.open = True
            else:
                message.value = "Invalid username or password!"
                message.color = ft.Colors.RED_700
                page.update()

        username_field = ft.TextField(label="Username", width=300, color=ft.Colors.BROWN_900, on_submit=lambda e: page.focus(password_field))
        password_field = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300, color=ft.Colors.BROWN_900, on_submit=login_clicked)
        message = ft.Text(value="", color=ft.Colors.RED_700)

        login_button = ft.ElevatedButton("Login", on_click=login_clicked, width=300, bgcolor=ft.Colors.BROWN_500, color=ft.Colors.WHITE)
        back_button = ft.OutlinedButton("Back", on_click=lambda e: layout1(), width=300)

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

# OWNER DASHBOARD
    def layout4():
        page.clean()
        main_content = ft.Container(expand=True)

# DASHBOARD PAGE ( date and input fields, product table, cart table, total amount)
        def layout5():
            def order_type_changed(e):
                if e.control:
                    print("Selected Order Type:", e.control.value)

            owner_title = ft.Text("Making Orders", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BROWN_900)

            cart_items = []

            cart_table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Product", color=ft.Colors.BROWN_700)),
                    ft.DataColumn(ft.Text("Category", color=ft.Colors.BROWN_700)),
                    ft.DataColumn(ft.Text("Price", color=ft.Colors.BROWN_700)),
                    ft.DataColumn(ft.Text("Quantity", color=ft.Colors.BROWN_700)),
                    ft.DataColumn(ft.Text("Total", color=ft.Colors.BROWN_700)),
                    ft.DataColumn(ft.Text("Remove", color=ft.Colors.BROWN_700)),
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
                qty_text = ft.Text(value="1", size=16, width=40, text_align=ft.TextAlign.CENTER)

                def decrease_qty(e, qty_text=qty_text):
                    qty = int(qty_text.value)
                    if qty > 1:
                        qty_text.value = str(qty - 1)
                        page.update()

                def increase_qty(e, qty_text=qty_text):
                    qty_text.value = str(int(qty_text.value) + 1)
                    page.update()

                def add_to_cart(e, prod=product, qty_text=qty_text):
                    qty = int(qty_text.value)
                    cart_items.append({
                        "name": prod["name"],
                        "category": prod["category"],
                        "price": prod["price"],
                        "quantity": qty
                    })
                    update_cart_table()

                product_rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(product["name"])),
                        ft.DataCell(ft.Text(product["category"])),
                        ft.DataCell(ft.Text(f"{product['price']:.2f}")),
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(ft.Icons.REMOVE, on_click=decrease_qty),
                                qty_text,
                                ft.IconButton(ft.Icons.ADD, on_click=increase_qty)
                            ], alignment=ft.MainAxisAlignment.CENTER)
                        ),
                        ft.DataCell(ft.IconButton(ft.Icons.CHECK, on_click=add_to_cart))
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


  
 # PRODUCT MANAGEMENT
 # NEED SOME CHANGES PA HEREEEEE
        
        
# REFRESH PRODUCTS
#NEED SOME CHANGES PA HEREEEEE
        
        # PRODUCT MANAGEMENT (FULLY FUNCTIONAL)
        def layout6():
            # Temporary product list (replace with actual DB later)
            product_list = []

            selected_product = None
            product_container = ft.Container(expand=True)

            # ---------- SHOW PRODUCT LIST ----------
            def layout_products():
                table_rows = []

                for p in product_list:
                    table_rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(p["name"])),
                                ft.DataCell(ft.Text(p["category"])),
                                ft.DataCell(ft.Text(str(p["price"]))),
                                ft.DataCell(
                                    ft.Row([
                                        ft.IconButton(ft.Icons.EDIT,
                                              on_click=lambda e, prod=p: open_edit(prod)),
                                        ft.IconButton(ft.Icons.DELETE,
                                              on_click=lambda e, prod=p: delete_product(prod)),
                                    ])
                                )
                            ]
                        )
                    )

                product_container.content = ft.Column(
                    [
                        ft.Text("Product and Price Management", size=22,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BROWN_900),

                        ft.Row(
                            [
                                ft.TextField(hint_text="Search Products...",
                                             width=250, bgcolor=ft.Colors.WHITE),
                                ft.IconButton(ft.Icons.ADD_CIRCLE,
                                              on_click=open_add,
                                              icon_color=ft.Colors.BROWN_700),
                            ],
                            spacing=10
                        ),

                        ft.DataTable(
                            columns=[
                                ft.DataColumn(ft.Text("Product")),
                                ft.DataColumn(ft.Text("Category")),
                                ft.DataColumn(ft.Text("Price")),
                                ft.DataColumn(ft.Text("Action")),
                            ],
                            rows=table_rows,
                            width=800
                        )
                    ],
                    spacing=20
                )

                page.update()

            # ---------- OPEN ADD PRODUCT FORM ----------
            def open_add(e=None):
                nonlocal selected_product
                selected_product = None
                product_container.content = layout_add_edit()
                page.update()

            # ---------- OPEN EDIT PRODUCT FORM ----------
            def open_edit(product):
                nonlocal selected_product
                selected_product = product
                product_container.content = layout_add_edit(product)
                page.update()

            # ---------- DELETE PRODUCT ----------
            def delete_product(product):
                product_list.remove(product)
                layout_products()

            # ---------- SAVE PRODUCT ----------
            def save_product(e, name_field, category_field, price_field):
                nonlocal selected_product
                name = name_field.value
                category = category_field.value
                price = float(price_field.value)

                if selected_product is None:
                    product_list.append({
                        "id": len(product_list) + 1,
                        "name": name,
                        "category": category,
                        "price": price,
                    })
                else:
                    selected_product["name"] = name
                    selected_product["category"] = category
                    selected_product["price"] = price

                layout_products()

            # ---------- ADD/EDIT FORM ----------
            def layout_add_edit(prod=None):
                name_field = ft.TextField(
                    label="Product Name", width=350,
                    value=prod["name"] if prod else ""
                )

                category_field = ft.TextField(
                    label="Category", width=350,
                    value=prod["category"] if prod else "Coffee"
                )

                price_field = ft.TextField(
                    label="Price", width=350,
                    value=str(prod["price"]) if prod else ""
                )

                return ft.Column(
                    [
                        ft.Text("Product and Price Management", size=22,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BROWN_900),

                        ft.Container(
                            ft.Column(
                                [
                                    name_field,
                                    category_field,
                                    price_field,
                                    ft.Row(
                                        [
                                            ft.ElevatedButton("Cancel",
                                                              on_click=lambda e: layout_products()),
                                            ft.ElevatedButton("Save Product",
                                                              on_click=lambda e: save_product(
                                                                  e, name_field, category_field, price_field)),
                                        ],
                                        spacing=20
                                    )
                                ],
                                spacing=20
                            ),
                            padding=20,
                            border=ft.border.all(1),
                            border_radius=10,
                            bgcolor=ft.Colors.WHITE,
                            width=500
                        )
                    ],
                    spacing=20
                )

            # INITIAL LOAD
            product_container.content = layout_products()

            # Place inside main content
            main_content.content = ft.Container(
                padding=20,
                bgcolor=ft.Colors.BROWN_100,
                content=product_container
            )
            page.update()

# ADD PRODUCT DIALOG
#WALA PA MAN ITONG FUNCTION
        

# SIDEBAR
        sidebar = ft.Container(
            bgcolor=ft.Colors.BROWN_500,
            width=220,
            padding=15,
            content=ft.Column(
                [
                    ft.Text("Coffeestry", size=24, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                    ft.Divider(color=ft.Colors.BROWN_500, thickness=2),
                    ft.ElevatedButton(
                        "Dashboard",
                        icon=ft.Icons.DASHBOARD,
                        bgcolor=ft.Colors.BROWN_700,
                        color=ft.Colors.WHITE,
                        width=200,
                        on_click=lambda e: layout5(),
                    ),
                    ft.ElevatedButton(
                        "Products and Price Management",
                        icon=ft.Icons.INVENTORY,
                        width=200,
                        bgcolor=ft.Colors.BROWN_700,
                        color=ft.Colors.WHITE,
                        on_click=lambda e: layout6(),
                    ),
                    ft.ElevatedButton(
                        "Financial Reports",
                        icon=ft.Icons.ASSESSMENT,
                        width=200,
                        bgcolor=ft.Colors.BROWN_700,
                        color=ft.Colors.WHITE,
                    ),
                    ft.ElevatedButton(
                        "Inventory & Supplier Management",
                        icon=ft.Icons.STORE,
                        width=200,
                        bgcolor=ft.Colors.BROWN_700,
                        color=ft.Colors.WHITE,
                    ),
                    ft.ElevatedButton(
                        "User Management",
                        icon=ft.Icons.MANAGE_ACCOUNTS,
                        width=200,
                        bgcolor=ft.Colors.BROWN_700,
                        color=ft.Colors.WHITE,
                    ),
                    ft.Container(expand=True),
                    ft.ElevatedButton(
                        "Logout",
                        icon=ft.Icons.LOGOUT,
                        bgcolor=ft.Colors.GREY_400,
                        color=ft.Colors.BROWN_900,
                        width=200,
                        on_click=lambda e: layout1(),
                    ),            
                ],
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

        layout = ft.Row([sidebar, main_content], expand=True)
        page.add(layout)

#LOG OUT BUTTON KAILANGAN MAY FUNCTION NA SIYA
        layout5()

# START
    layout1()
ft.app(target=main)        