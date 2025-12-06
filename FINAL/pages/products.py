import flet as ft
from config import *
from database_new import get_all_products, add_product, update_product, delete_product

def create_products_view(page, main_content):
    """Create the Product Management view"""
    
    selected_product = {"data": None}  # Use dict to handle nonlocal
    
    def refresh_product_list():
        """Refresh the product list from database"""
        products = get_all_products()
        
        table_rows = []
        for p in products:
            table_rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(p["name"], color=TEXT_DARK)),
                        ft.DataCell(
                            ft.Container(
                                content=ft.Text(p["category"], size=11, color=ACCENT_CREAM),
                                bgcolor=PRIMARY_LIGHT if p["category"] == "Coffee" else ACCENT_GOLD,
                                padding=ft.padding.symmetric(horizontal=8, vertical=2),
                                border_radius=10,
                            )
                        ),
                        ft.DataCell(ft.Text(f"₱{p['price']:.2f}", color=TEXT_DARK, weight=ft.FontWeight.W_500)),
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(
                                    ft.Icons.EDIT,
                                    icon_color=PRIMARY_MID,
                                    icon_size=20,
                                    on_click=lambda e, prod=p: show_edit_form(prod)
                                ),
                                ft.IconButton(
                                    ft.Icons.DELETE,
                                    icon_color=ERROR,
                                    icon_size=20,
                                    on_click=lambda e, prod=p: confirm_delete(prod)
                                ),
                            ], spacing=0)
                        )
                    ]
                )   
            )
        
        # Product list view
        product_list_view = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.INVENTORY_2, size=26, color=PRIMARY_MID),
                            ft.Text("Product & Price Management", size=20, weight=ft.FontWeight.BOLD, color=PRIMARY_DARK),
                        ],
                        spacing=10,
                    ),
                    ft.Divider(height=15, color=ACCENT_CREAM, thickness=2),
                    ft.Row(
                        [
                            ft.Container(expand=True),
                            ft.ElevatedButton(
                                "Add Product",
                                icon=ft.Icons.ADD_CIRCLE,
                                bgcolor=PRIMARY_MID,
                                color=ACCENT_CREAM,
                                height=45,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                    elevation=2,
                                ),
                                on_click=lambda e: show_add_form(),
                            ),
                        ],
                        spacing=15,
                    ),
                    ft.Container(height=10),
                    ft.Container(
                        content=ft.DataTable(
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
                        ),
                        bgcolor=BG_CARD,
                        padding=15,
                        border_radius=15,
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
            padding=15,
            bgcolor=BG_LIGHT,
            expand=True,
        )
        
        main_content.content = product_list_view
        page.update()

    def show_add_form():
        """Show the add product form"""
        selected_product["data"] = None
        show_product_form(None)

    def show_edit_form(product):
        """Show the edit product form"""
        selected_product["data"] = product
        show_product_form(product)

    def show_product_form(product=None):
        """Show product add/edit form"""
        name_field = ft.TextField(
            label="Product Name", 
            width=320, 
            color=TEXT_DARK,
            border_color=ACCENT_WARM, 
            focused_border_color=PRIMARY_MID,
            label_style=ft.TextStyle(color=TEXT_MID),
            border_radius=10,
            value=product["name"] if product else ""
        )
        
        category_field = ft.Dropdown(
            label="Category", 
            width=320, 
            color=TEXT_DARK,
            border_color=ACCENT_WARM, 
            focused_border_color=PRIMARY_MID,
            label_style=ft.TextStyle(color=TEXT_MID),
            border_radius=10,
            value=product["category"] if product else None,
            options=[
                ft.dropdown.Option("Coffee"),
                ft.dropdown.Option("Pastry"),
            ]
        )
        
        price_field = ft.TextField(
            label="Price (₱)", 
            width=320, 
            color=TEXT_DARK,
            border_color=ACCENT_WARM, 
            focused_border_color=PRIMARY_MID,
            label_style=ft.TextStyle(color=TEXT_MID),
            border_radius=10,
            keyboard_type=ft.KeyboardType.NUMBER,
            value=str(product["price"]) if product else ""
        )
        
        error_text = ft.Text("", color=ERROR, size=13)

        def save_clicked(e):
            name = name_field.value.strip()
            category = category_field.value
            price_str = price_field.value.strip()
            
            # Validation
            if not name:
                error_text.value = "Please enter product name!"
                page.update()
                return
            
            if not category:
                error_text.value = "Please select a category!"
                page.update()
                return
            
            try:
                price = float(price_str)
                if price <= 0:
                    raise ValueError()
            except:
                error_text.value = "Please enter a valid price!"
                page.update()
                return
            
            if product:
                # Update existing product
                update_product(product["id"], name, category, price)
                page.snack_bar = ft.SnackBar(
                    ft.Text(f"Product '{name}' updated successfully!", color=ACCENT_CREAM),
                    bgcolor=SUCCESS,
                )
            else:
                # Add new product
                add_product(name, category, price)
                page.snack_bar = ft.SnackBar(
                    ft.Text(f"Product '{name}' added successfully!", color=ACCENT_CREAM),
                    bgcolor=SUCCESS,
                )
            
            page.snack_bar.open = True
            refresh_product_list()

        form_view = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.INVENTORY_2, size=26, color=PRIMARY_MID),
                            ft.Text("Product & Price Management", size=20, weight=ft.FontWeight.BOLD, color=PRIMARY_DARK),
                        ],
                        spacing=10,
                    ),
                    ft.Divider(height=15, color=ACCENT_CREAM, thickness=2),
                    
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(
                                    "Edit Product" if product else "Add New Product",
                                    size=18, 
                                    weight=ft.FontWeight.W_600, 
                                    color=PRIMARY_DARK
                                ),
                                ft.Container(height=15),
                                name_field,
                                category_field,
                                price_field,
                                error_text,
                                ft.Container(height=15),
                                ft.Row(
                                    [
                                        ft.OutlinedButton(
                                            "Cancel",
                                            width=140,
                                            height=45,
                                            style=ft.ButtonStyle(
                                                shape=ft.RoundedRectangleBorder(radius=10),
                                                side=ft.BorderSide(2, PRIMARY_MID),
                                            ),
                                            on_click=lambda e: refresh_product_list()
                                        ),
                                        ft.ElevatedButton(
                                            "Save Product",
                                            icon=ft.Icons.SAVE,
                                            width=160,
                                            height=45,
                                            bgcolor=PRIMARY_MID,
                                            color=ACCENT_CREAM,
                                            style=ft.ButtonStyle(
                                                shape=ft.RoundedRectangleBorder(radius=10),
                                                elevation=2,
                                            ),
                                            on_click=save_clicked
                                        ),
                                    ],
                                    spacing=15
                                )
                            ],
                            spacing=12,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        padding=30,
                        bgcolor=BG_CARD,
                        border_radius=15,
                        shadow=ft.BoxShadow(
                            color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                            blur_radius=15,
                            offset=ft.Offset(0, 4)
                        ),
                        width=400,
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=15,
            bgcolor=BG_LIGHT,
            expand=True,
        )
        
        main_content.content = form_view
        page.update()

    def confirm_delete(product):
        """Show delete confirmation dialog"""
        def do_delete(e):
            delete_product(product["id"])
            page.dialog.open = False
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Product '{product['name']}' deleted!", color=ACCENT_CREAM),
                bgcolor=SUCCESS,
            )
            page.snack_bar.open = True
            refresh_product_list()

        def cancel_delete(e):
            page.dialog.open = False
            page.update()

        page.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirm Delete", color=PRIMARY_DARK),
            content=ft.Text(f"Are you sure you want to delete '{product['name']}'?", color=TEXT_MID),
            actions=[
                ft.TextButton("Cancel", on_click=cancel_delete),
                ft.ElevatedButton(
                    "Delete", 
                    bgcolor=ERROR, 
                    color=ACCENT_CREAM,
                    on_click=do_delete
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.dialog.open = True
        page.update()

    # Initial load
    refresh_product_list()
