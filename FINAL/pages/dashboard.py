import flet as ft
from config import *
from pages.orders import create_orders_view
from pages.products import create_products_view

def create_dashboard(page, go_to_home, user_role, username):
    """Create the main dashboard with sidebar"""
    page.clean()
    
    # Main content area
    main_content = ft.Container(expand=True, bgcolor=BG_LIGHT)
    
    # Current view tracker
    current_view = {"name": "dashboard"}

    def show_orders():
        current_view["name"] = "dashboard"
        create_orders_view(page, main_content)

    def show_products():
        current_view["name"] = "products"
        create_products_view(page, main_content)

    def show_history():
        current_view["name"] = "history"
        # Placeholder for order history
        main_content.content = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.HISTORY, size=80, color=PRIMARY_LIGHT),
                    ft.Text("Order History", size=24, weight=ft.FontWeight.BOLD, color=PRIMARY_DARK),
                    ft.Text("Coming soon...", size=16, color=TEXT_MID),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            expand=True,
            bgcolor=BG_LIGHT,
            alignment=ft.alignment.center,
        )
        page.update()

    def logout():
        go_to_home()

    # Sidebar button creator
    def create_nav_button(text, icon, on_click):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(icon, size=20, color=ACCENT_CREAM),
                    ft.Text(text, size=13, color=ACCENT_CREAM, weight=ft.FontWeight.W_500),
                ],
                spacing=12,
            ),
            padding=ft.padding.symmetric(horizontal=15, vertical=12),
            border_radius=10,
            bgcolor=ft.Colors.TRANSPARENT,
            on_click=on_click,
            ink=True,
        )

    # Sidebar
    sidebar = ft.Container(
        bgcolor=PRIMARY_DARK,
        width=240,
        padding=ft.padding.symmetric(horizontal=15, vertical=20),
        content=ft.Column(
            [
                # Logo Section
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.LOCAL_CAFE, size=30, color=ACCENT_WARM),
                            ft.Text("Coffeestry", size=20, color=ACCENT_CREAM, weight=ft.FontWeight.BOLD),
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
                
                create_nav_button("Dashboard", ft.Icons.DASHBOARD_ROUNDED, lambda e: show_orders()),
                ft.Container(height=5),
                create_nav_button("Products & Prices", ft.Icons.INVENTORY_2_ROUNDED, lambda e: show_products()),
                ft.Container(height=5),
                create_nav_button("Order History", ft.Icons.HISTORY_ROUNDED, lambda e: show_history()),
                
                ft.Container(expand=True),
                
                # User Section
                ft.Divider(color=ft.Colors.with_opacity(0.3, ACCENT_CREAM), thickness=1),
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Container(
                                content=ft.Icon(ft.Icons.PERSON, size=18, color=PRIMARY_DARK),
                                bgcolor=ACCENT_WARM,
                                border_radius=18,
                                padding=8,
                            ),
                            ft.Column(
                                [
                                    ft.Text(username, size=13, color=ACCENT_CREAM, weight=ft.FontWeight.W_600),
                                    ft.Text(user_role.capitalize(), size=11, color=TEXT_LIGHT),
                                ],
                                spacing=0,
                            ),
                        ],
                        spacing=10,
                    ),
                    margin=ft.margin.symmetric(vertical=12),
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
                    on_click=lambda e: logout(),
                    ink=True,
                ),
            ],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        ),
    )

    # Main layout
    layout = ft.Row([sidebar, main_content], expand=True, spacing=0)
    page.add(layout)
    page.update()

    # Load default view (Making Orders)
    show_orders()
