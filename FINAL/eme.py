import flet as ft

def main(page: ft.Page):
    page.title = "Coffeestry System"
    page.window_maximized = True

    # --- Temporary list to simulate DB ---
    products = []    # each item: {"id":1, "name":"...", "category":"...", "price":120}

    selected_product = None  # for edit mode

    # Main container where pages will be swapped
    main_container = ft.Container(expand=True)

    # ----------- FUNCTION: SHOW PRODUCT LIST (WIREFRAME 1) ----------
    def layout_products():

        # Define the table rows
        table_rows = []
        for p in products:
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

        # Build screen layout
        return ft.Column(
            [
                ft.Text("Product and Price Management", size=20, weight=ft.FontWeight.BOLD),
                ft.Row(
                    [
                        ft.TextField(hint_text="Search Products...", width=250),
                        ft.IconButton(ft.Icons.ADD_CIRCLE, on_click=open_add),
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
            expand=True
        )

    # -------- FUNCTION: OPEN ADD FORM (WIREFRAME 2) -----------
    def open_add(e):
        nonlocal selected_product
        selected_product = None
        main_container.content = layout_add_edit()
        page.update()

    # -------- FUNCTION: OPEN EDIT FORM -----------
    def open_edit(product):
        nonlocal selected_product
        selected_product = product
        main_container.content = layout_add_edit(product)
        page.update()

    # -------- FUNCTION: DELETE PRODUCT -----------
    def delete_product(product):
        products.remove(product)
        main_container.content = layout_products()
        page.update()

    # -------- FUNCTION: SAVE PRODUCT (ADD/EDIT) -----------
    def save_product(e, name_field, category_field, price_field):
        name = name_field.value
        category = category_field.value
        price = float(price_field.value)

        nonlocal selected_product

        if selected_product is None:
            # Add new
            products.append({
                "id": len(products)+1,
                "name": name,
                "category": category,
                "price": price,
            })
        else:
            # Edit existing
            selected_product["name"] = name
            selected_product["category"] = category
            selected_product["price"] = price

        main_container.content = layout_products()
        page.update()

    # -------- FUNCTION: BUILD ADD/EDIT FORM -----------
    def layout_add_edit(prod=None):

        name_field = ft.TextField(label="Product Name", width=350,
                                  value=prod["name"] if prod else "")

        category_field = ft.TextField(label="Category", width=350,
                                      value=prod["category"] if prod else "Coffee")

        price_field = ft.TextField(label="Price", width=350,
                                   value=str(prod["price"]) if prod else "")

        return ft.Column(
            [
                ft.Text("Product and Price Management", size=20, weight=ft.FontWeight.BOLD),
                ft.Row(
                    [
                        ft.TextField(hint_text="Search Products...", width=250),
                        ft.IconButton(ft.Icons.ADD_CIRCLE),
                    ],
                    spacing=10
                ),
                ft.Container(
                    ft.Column(
                        [
                            name_field,
                            category_field,
                            price_field,
                            ft.Row(
                                [
                                    ft.ElevatedButton("Cancel",
                                        on_click=lambda e: back_to_list()),
                                    ft.ElevatedButton("Save Product",
                                        on_click=lambda e: save_product(
                                            e, name_field, category_field, price_field
                                        )),
                                ],
                                spacing=20
                            )
                        ],
                        spacing=20
                    ),
                    padding=20,
                    border=ft.border.all(1),
                    border_radius=8,
                    width=500
                )
            ],
            expand=True
        )

    # -------- BACK TO PRODUCT LIST ----------
    def back_to_list():
        main_container.content = layout_products()
        page.update()

    # INITIAL LOAD
    main_container.content = layout_products()
    page.add(main_container)


ft.app(target=main)