import flet as ft
from config import *
from database_new import authenticate_user, register_user, check_username_exists

def create_login_page(page, go_back, go_to_dashboard, go_to_signup):
    """Create and return the login page content"""
    page.clean()

    def login_clicked(e):
        username = username_field.value.strip()
        password = password_field.value

        if not username or not password:
            message.value = "Please enter both username and password!"
            message.color = ERROR
            page.update()
            return

        role = authenticate_user(username, password)

        if role:
            message.value = f"Welcome, {role.capitalize()}!"
            message.color = SUCCESS
            page.update()
            go_to_dashboard(role, username)
        else:
            message.value = "Invalid username or password!"
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
        on_submit=lambda e: password_field.focus()
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
        on_submit=login_clicked
    )
    
    message = ft.Text(value="", color=ERROR, size=14)

    login_content = ft.Container(
        content=ft.Row(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(ft.Icons.COFFEE, size=60, color=PRIMARY_MID),
                            ft.Text("Login to Coffeestry", size=26, weight=ft.FontWeight.BOLD, color=PRIMARY_DARK),
                            ft.Text("Enter your credentials", size=14, color=TEXT_MID),
                            ft.Container(height=20),
                            username_field,
                            password_field,
                            ft.Container(height=15),
                            ft.ElevatedButton(
                                "Login", 
                                on_click=login_clicked, 
                                width=320,
                                height=50,
                                bgcolor=PRIMARY_MID, 
                                color=ACCENT_CREAM,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=25),
                                    elevation=3,
                                )
                            ),
                            ft.Container(height=5),
                            ft.Row(
                                [
                                    ft.Text("Don't have an account?", size=13, color=TEXT_MID),
                                    ft.TextButton(
                                        "Sign Up",
                                        on_click=lambda e: go_to_signup(),
                                        style=ft.ButtonStyle(color=PRIMARY_MID),
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            ft.OutlinedButton(
                                "Back to Home", 
                                on_click=lambda e: go_back(), 
                                width=320,
                                height=45,
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
                    padding=50,
                    width=450,
                    bgcolor=BG_CARD,
                    border_radius=25,
                    shadow=ft.BoxShadow(
                        color=ft.Colors.with_opacity(0.12, ft.Colors.BLACK),
                        blur_radius=30,
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

    page.add(login_content)
    page.update()


def create_signup_page(page, go_back, go_to_login):
    """Create and return the signup page content"""
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
            # Show success snackbar
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Account '{username}' created successfully!", color=ACCENT_CREAM),
                bgcolor=SUCCESS,
            )
            page.snack_bar.open = True
            page.update()
            # Navigate to login
            go_to_login()
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
        autofocus=True,
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

    signup_content = ft.Container(
        content=ft.Row(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(ft.Icons.PERSON_ADD, size=60, color=PRIMARY_MID),
                            ft.Text("Create Account", size=26, weight=ft.FontWeight.BOLD, color=PRIMARY_DARK),
                            ft.Text("Join Coffeestry today", size=14, color=TEXT_MID),
                            ft.Container(height=20),
                            username_field,
                            password_field,
                            confirm_password_field,
                            ft.Container(height=15),
                            ft.ElevatedButton(
                                "Sign Up", 
                                on_click=signup_clicked, 
                                width=320,
                                height=50,
                                bgcolor=PRIMARY_MID, 
                                color=ACCENT_CREAM,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=25),
                                    elevation=3,
                                )
                            ),
                            ft.Container(height=5),
                            ft.Row(
                                [
                                    ft.Text("Already have an account?", size=13, color=TEXT_MID),
                                    ft.TextButton(
                                        "Login",
                                        on_click=lambda e: go_to_login(),
                                        style=ft.ButtonStyle(color=PRIMARY_MID),
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            ft.OutlinedButton(
                                "Back to Home", 
                                on_click=lambda e: go_back(), 
                                width=320,
                                height=45,
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
                    padding=50,
                    width=450,
                    bgcolor=BG_CARD,
                    border_radius=25,
                    shadow=ft.BoxShadow(
                        color=ft.Colors.with_opacity(0.12, ft.Colors.BLACK),
                        blur_radius=30,
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

    page.add(signup_content)
    page.update()
