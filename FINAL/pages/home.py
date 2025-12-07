import flet as ft
from config import *

def create_home_page(page, go_to_login, go_to_about):
    """Create and return the home page content"""
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
                on_click=lambda e: print("Sign Up button clicked"),  # Replace with actual function when defined
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


def create_about_page(page, go_back):
    """Create and return the about page content"""
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
                    on_click=lambda e: go_back(),
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
