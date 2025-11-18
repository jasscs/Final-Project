import flet as ft
from database import get_connection

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

    # HOME SCREEN
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
                    content=ft.ElevatedButton("Login", on_click=lambda e: show_login(),
                        bgcolor=ft.Colors.BROWN_500, color=ft.Colors.WHITE, width=220),
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    content=ft.ElevatedButton("About", on_click=lambda e: show_about(),
                        bgcolor=ft.Colors.BROWN_300, width=220),
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    content=ft.ElevatedButton("Exit", on_click=lambda e: page.window_close(),
                        bgcolor=ft.Colors.BROWN_700, color=ft.Colors.WHITE, width=220),
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

    # ABOUT SCREEN
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
                        ft.ElevatedButton("Back", on_click=lambda e: show_home(),
                                          width=200, bgcolor=ft.Colors.BROWN_500, color=ft.Colors.WHITE),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=15,
                ),
                alignment=ft.alignment.center,
                expand=True,
            )
        )

    # LOGIN SCREEN
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

    # MENU DATA
    menu_items_data = [
        {"name": "Americano", "desc": "A black coffee", "price": 99.00, "image": "americano.png"},
        {"name": "Espresso", "desc": "A strong black coffee", "price": 99.00, "image": "espresso.png"},
        {"name": "Pilipino", "desc": "A roasted rice coffee", "price": 99.00, "image": "pilipino.png"},
        {"name": "Croissant", "desc": "With different fillings", "price": 75.00, "image": "croissant.png"},
    ]

    # OWNER DASHBOARD
    def show_owner_dashboard():
        page.clean()
        main_content = ft.Container(expand=True)

        menu_grid = ft.ResponsiveRow(spacing=20)

        def refresh_menu():
            menu_grid.controls.clear()
            for idx, item in enumerate(menu_items_data):
                menu_grid.controls.append(
                    ft.Container(
                        content=menu_card(item, idx),
                        col={"xs": 12, "sm": 6, "md": 4, "lg": 3}
                    )
                )
            page.update()

        def menu_card(item, index):
            return ft.Container(
                width=220,
                height=280,
                bgcolor=ft.Colors.BROWN_50,
                border_radius=12,
                padding=10,
                content=ft.Column(
                    [
                        ft.Stack(
                            [ft.Image(
                                src=item["image"],
                                width=220,
                                height=140,
                                fit=ft.ImageFit.COVER,
                                border_radius=8
                            ),
                            ft.IconButton(
                                ft.Icons.EDIT,
                                icon_size=20,
                                icon_color=ft.Colors.WHITE,
                                bgcolor=ft.Colors.BROWN_700,
                                right=5,
                                top=5,
                                on_click=lambda e, i=index: show_edit_menu_dialog(i)
                            )
                            ]
                        ),
                        ft.Text(item["name"], weight=ft.FontWeight.BOLD, color=ft.Colors.BROWN_900),
                        ft.Text(item["desc"], size=12, color=ft.Colors.BROWN_600),
                        ft.Text(f"₱ {item['price']:.2f}", size=13, weight=ft.FontWeight.BOLD, color=ft.Colors.BROWN_800),
                    ],
                    spacing=6,
                ) 
            )

        def show_edit_menu_dialog(index):
            item = menu_items_data[index]
            name_field = ft.TextField(label="Product Name", value=item["name"])
            desc_field = ft.TextField(label="Description", value=item["desc"])
            price_field = ft.TextField(label="Price", value=str(item["price"]))
            img_preview = ft.Image(src=item["image"], width=200, height=120, fit=ft.ImageFit.COVER)
            selected_image = {"path": item["image"]}

            def pick_image_result(e: ft.FieldPickerResultEvent):
                if e.files:
                    selected_image["path"] = e.files[0].path
                    img_preview.src = selected_image["path"]
                    page.update()
            
            file_picker = ft.FilePicker(on_result=pick_image_result)
            page.overlay.append(file_picker)

            edit_dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Edit Menu Item"),
                content=ft.Column(
                    [
                        name_field,
                        desc_field,
                        price_field,
                        img_preview,
                        ft.ElevatedButton("Select Image", on_click=lambda e: file_picker.pick_files(allow_multiple=False, allowed_extensions=["png", "jpg", "jpeg"]))
                    ],
                    tight=True,
                ),
                actions=[
                    ft.TextButton("Delete", on_click=lambda e: delete_menu_item(index, edit_dialog)),
                    ft.TextButton("Save", on_click=lambda e: save_menu_item(index, name_field, desc_field, price_field, selected_image, edit_dialog)),
                    ft.TextButton("Cancel", on_click=lambda e: close_dialog(edit_dialog)),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )

            page.dialog = edit_dialog
            edit_dialog.open = True
            page.update()

        def save_menu_item(index, name_field, desc_field, price_field, selected_image, dialog):
            menu_items_data[index]["name"] = name_field.value
            menu_items_data[index]["desc"] = desc_field.value
            menu_items_data[index]["price"] = float(price_field.value)
            menu_items_data[index]["image"] = selected_image["path"]
            dialog.open = False
            refresh_menu()
            page.update()

        def delete_menu_item(index, dialog):
            menu_items_data.pop(index)
            dialog.open = False
            refresh_menu()
            page.update()

        def close_dialog(dialog):
            dialog.open = False
            page.update()

        # DASHBOARD LAYOUT
        owner_title = ft.Text("Owner Dashboard", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BROWN_900)
        dashboard_view = ft.Column(
            [
                owner_title,
                ft.Container(
                    padding=15,
                    margin=ft.margin.only(top=10),
                    border=ft.border.all(1, ft.Colors.BROWN_300),
                    border_radius=10,
                    bgcolor=ft.Colors.WHITE,
                    content=ft.Column([ft.Text("Dashboard Overview", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BROWN_900)], spacing=10)
                ),
                ft.Container(
                    padding=15,
                    margin=ft.margin.only(top=20),
                    border=ft.border.all(1, ft.Colors.BROWN_300),
                    border_radius=10,
                    bgcolor=ft.Colors.WHITE,
                    content=ft.Column(
                        [ft.Text("Menu Items", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BROWN_900),
                         ft.Container(height=5),
                         menu_grid],
                        spacing=10,
                    )
                )
            ],
            spacing=20,
            scroll=ft.ScrollMode.AUTO
        )

        main_content.content = ft.Container(
            padding=20,
            bgcolor=ft.Colors.BROWN_100,
            content=dashboard_view
        )

        # SIDEBAR
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
                        on_click=lambda e: page.update(),
                    ),
                    ft.ElevatedButton(
                        "Add Menu Item",
                        icon=ft.Icons.ADD,
                        width=190,
                        bgcolor=ft.Colors.BROWN_500,
                        color=ft.Colors.WHITE,
                        on_click=lambda e: add_new_menu_item(),
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
                ],
                spacing=15,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

        layout = ft.Row([sidebar, main_content], expand=True)
        page.add(layout)
        refresh_menu()

        def add_new_menu_item():
            menu_items_data.append({"name": "New Item", "desc": "", "price": 0.0, "image": "default.png"})
            refresh_menu()
            # automatically open edit dialog for new item
            show_edit_menu_dialog(len(menu_items_data)-1)

    # Start with home
    show_home()

ft.app(target=main)
