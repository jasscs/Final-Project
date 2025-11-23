import flet as ft

def main(page: ft.Page):
    page.title = "Coffeestry Cart Example"
    page.window_maximized = True

    # Sample product list
    products = [
        {"name": "Espresso", "category": "Coffee", "price": 90},
        {"name": "Latte", "category": "Coffee", "price": 90},
        {"name": "Croissant", "category": "Pastry", "price": 90},
    ]

    cart_items = []

    # Cart DataTable
    cart_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Product")),
            ft.DataColumn(ft.Text("Quantity")),
            ft.DataColumn(ft.Text("Price")),
            ft.DataColumn(ft.Text("Total")),
            ft.DataColumn(ft.Text("Remove")),
        ],
        rows=[]
    )

    total_text = ft.Text("Total: 0.00", size=16)

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
                    ft.DataCell(ft.Text(str(item["quantity"]))),
                    ft.DataCell(ft.Text(f"{item['price']:.2f}")),
                    ft.DataCell(ft.Text(f"{total_item:.2f}")),
                    ft.DataCell(ft.IconButton(ft.Icons.DELETE, on_click=remove_item))
                ])
            )
        cart_table.rows = rows
        total_text.value = f"Total: {total:.2f}"
        page.update()

    # Create product DataTable
    product_rows = []
    for product in products:
        qty_field = ft.TextField(width=60, value="1", keyboard_type=ft.KeyboardType.NUMBER)

        def add_to_cart(e, prod=product, qty_field=qty_field):
            try:
                qty = int(qty_field.value)
                if qty <= 0:
                    raise ValueError
                cart_items.append({
                    "name": prod["name"],
                    "category": prod["category"],
                    "price": prod["price"],
                    "quantity": qty
                })
                update_cart_table()
            except ValueError:
                page.snack_bar = ft.SnackBar(ft.Text("Quantity must be a positive number"))
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
            ft.DataColumn(ft.Text("Product")),
            ft.DataColumn(ft.Text("Category")),
            ft.DataColumn(ft.Text("Price")),
            ft.DataColumn(ft.Text("Quantity")),
            ft.DataColumn(ft.Text("Add")),
        ],
        rows=product_rows
    )

    page.add(
        ft.Column([
            ft.Text("Product List:", size=18),
            product_table,
            ft.Divider(thickness=2),
            ft.Text("Cart:", size=18),
            cart_table,
            total_text
        ], spacing=15)
    )

ft.app(target=main)
