
# views/login_view.py
import customtkinter as ctk
from controllers.auth_controller import AuthController

class LoginView(ctk.CTkFrame):
    def __init__(self, master, show_main_view_callback):
        super().__init__(master)
        self.master = master
        self.show_main_view = show_main_view_callback
        self.auth_controller = AuthController()
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.setup_ui()

    def setup_ui(self):
        # Main container
        self.container = ctk.CTkFrame(self)
        self.container.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        # Title
        self.title = ctk.CTkLabel(
            self.container,
            text="Pokédex App",
            font=("Roboto", 24, "bold")
        )
        self.title.pack(pady=20)

        # Tabs
        self.tabview = ctk.CTkTabview(self.container)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Login tab
        login_tab = self.tabview.add("Login")
        self.setup_login_tab(login_tab)
        
        # Register tab
        register_tab = self.tabview.add("Registro")
        self.setup_register_tab(register_tab)

    def setup_login_tab(self, parent):
        # Username
        self.login_username = ctk.CTkEntry(
            parent,
            placeholder_text="Nombre de usuario"
        )
        self.login_username.pack(padx=20, pady=10, fill="x")
        
        # Password
        self.login_password = ctk.CTkEntry(
            parent,
            placeholder_text="Contraseña",
            show="*"
        )
        self.login_password.pack(padx=20, pady=10, fill="x")
        
        # Login button
        self.login_button = ctk.CTkButton(
            parent,
            text="Iniciar Sesión",
            command=self.handle_login
        )
        self.login_button.pack(padx=20, pady=20)
        
        # Error label
        self.login_error = ctk.CTkLabel(
            parent,
            text="",
            text_color="red"
        )
        self.login_error.pack(pady=10)

    def setup_register_tab(self, parent):
        # Username
        self.register_username = ctk.CTkEntry(
            parent,
            placeholder_text="Nombre de usuario"
        )
        self.register_username.pack(padx=20, pady=10, fill="x")
        
        # Email
        self.register_email = ctk.CTkEntry(
            parent,
            placeholder_text="Email"
        )
        self.register_email.pack(padx=20, pady=10, fill="x")
        
        # Password
        self.register_password = ctk.CTkEntry(
            parent,
            placeholder_text="Contraseña",
            show="*"
        )
        self.register_password.pack(padx=20, pady=10, fill="x")
        
        # Confirm Password
        self.register_confirm = ctk.CTkEntry(
            parent,
            placeholder_text="Confirmar Contraseña",
            show="*"
        )
        self.register_confirm.pack(padx=20, pady=10, fill="x")
        
        # Register button
        self.register_button = ctk.CTkButton(
            parent,
            text="Registrarse",
            command=self.handle_register
        )
        self.register_button.pack(padx=20, pady=20)
        
        # Error label
        self.register_error = ctk.CTkLabel(
            parent,
            text="",
            text_color="red"
        )
        self.register_error.pack(pady=10)

    def handle_login(self):
        username = self.login_username.get()
        password = self.login_password.get()
        
        success, message, user = self.auth_controller.login_user(username, password)
        
        if success:
            self.show_main_view(user)
        else:
            self.login_error.configure(text=message)

    def handle_register(self):
        username = self.register_username.get()
        email = self.register_email.get()
        password = self.register_password.get()
        confirm = self.register_confirm.get()
        
        if password != confirm:
            self.register_error.configure(text="Las contraseñas no coinciden")
            return
        
        success, message = self.auth_controller.register_user(
            username, password, email
        )
        
        if success:
            self.tabview.set("Login")
            self.register_error.configure(
                text="Registro exitoso. Por favor inicia sesión.",
                text_color="green"
            )
            # Clear registration fields
            self.register_username.delete(0, 'end')
            self.register_email.delete(0, 'end')
            self.register_password.delete(0, 'end')
            self.register_confirm.delete(0, 'end')
        else:
            self.register_error.configure(text=message)