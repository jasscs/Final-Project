"""
Coffeestry POS System
A Point of Sale system for coffee shops
"""

import flet as ft
from config import *

# Import database module to initialize database
import database_new

# Import page modules
from pages.auth import create_login_page, create_signup_page
from pages.dashboard import create_dashboard


def main(page: ft.Page):
    """Main application entry point"""
    
    # Page configuration
    page.title = "Coffeestry System"
    page.bgcolor = BG_LIGHT
    page.window_maximized = True
    page.window_resizable = True
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT

    # App bar
    page.appbar = ft.AppBar(
        title=ft.Text("Coffeestry System", size=18, color=ACCENT_CREAM, weight=ft.FontWeight.W_600),
        center_title=True,
        bgcolor=PRIMARY_DARK,
        elevation=4,
    )

    # Navigation functions
    def go_to_home():
        show_home_page()

    def go_to_login():
        create_login_page(page, go_to_home, go_to_dashboard, go_to_signup)

    def go_to_signup():
        create_signup_page(page, go_to_home, go_to_login)

    def go_to_about():
        show_about_page()

    def go_to_dashboard(role, username):
        create_dashboard(page, go_to_home, role, username)

    # Home Page
    def show_home_page():
        page.clean()

        home_content = ft.Column(
            [
                ft.Container(
                    content=ft.Icon(ft.Icons.LOCAL_CAFE, size=120, color=PRIMARY_MID),
                    alignment=ft.alignment.center,
                    margin=ft.margin.only(top=20, bottom=10),
                ),
                ft.Text("Welcome to Coffeestry", size=36, weight=ft.FontWeight.BOLD, color=PRIMARY_DARK),
                ft.Text("Your cozy coffee shop system", size=18, color=TEXT_MID, italic=True),
                ft.Container(height=30),
                ft.ElevatedButton(
                    "Login", 
                    on_click=lambda e: go_to_login(),
                    bgcolor=PRIMARY_MID, 
                    color=ACCENT_CREAM, 
                    width=280,
                    height=50,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=25),
                        elevation=3,
                    )
                ),
                ft.ElevatedButton(
                    "Sign Up", 
                    on_click=lambda e: go_to_signup(),
                    bgcolor=ACCENT_WARM, 
                    color=PRIMARY_DARK, 
                    width=280,
                    height=50,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=25),
                        elevation=3,
                    )
                ),
                ft.ElevatedButton(
                    "About", 
                    on_click=lambda e: go_to_about(),
                    bgcolor=PRIMARY_LIGHT, 
                    color=ACCENT_CREAM, 
                    width=280,
                    height=50,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=25),
                        elevation=3,
                    )
                ),
                ft.Container(height=40),
                ft.Text("© 2025 Coffeestry", size=12, color=TEXT_LIGHT,
                        italic=True, text_align=ft.TextAlign.CENTER),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=12,
        )

        main_container = ft.Container(
            content=home_content,
            expand=True, 
            bgcolor=BG_LIGHT,
            alignment=ft.alignment.center,
        )

        page.add(main_container)
        page.update()

    # About Page
    def show_about_page():
        page.clean()
        
        about_content = ft.Container(
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
                        on_click=lambda e: go_to_home(),
                        width=200,
                        height=45,
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
        
        page.add(about_content)
        page.update()

    # Start with home page
    show_home_page()


# Run the application
if __name__ == "__main__":
    ft.app(target=main)
