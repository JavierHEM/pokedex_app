# views/main_view.py
import customtkinter as ctk
from views.search_view import SearchView

class MainView(ctk.CTkFrame):
    def __init__(self, master, user: dict):
        super().__init__(master)
        self.master = master
        self.user = user
        
        # Configurar grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.setup_ui()

    def setup_ui(self):
        # Barra superior
        self.setup_top_bar()
        
        # Contenido principal
        self.setup_main_content()

    def setup_top_bar(self):
        top_bar = ctk.CTkFrame(self)
        top_bar.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        
        # Título
        title = ctk.CTkLabel(
            top_bar,
            text="Pokédex App",
            font=("Roboto", 20, "bold")
        )
        title.pack(side="left", padx=10)
        
        # Usuario actual
        user_label = ctk.CTkLabel(
            top_bar,
            text=f"Usuario: {self.user['username']}",
            font=("Roboto", 12)
        )
        user_label.pack(side="right", padx=10)

    def setup_main_content(self):
        # Crear vista de búsqueda
        search_view = SearchView(self, self.user['id'])
        search_view.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)