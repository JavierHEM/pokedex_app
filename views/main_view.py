# views/main_view.py
import customtkinter as ctk
from views.search_view import SearchView
from views.team_view import TeamView  
from datetime import datetime
from views.profile_view import ProfileView

class MainView(ctk.CTkFrame):
    def __init__(self, master, user_data):
        super().__init__(master)
        self.user_data = user_data
        self.current_view = None
        self.setup_ui()

    def setup_ui(self):
        # Configurar grid principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Barra lateral
        self.setup_sidebar()

        # Contenedor principal
        self.main_container = ctk.CTkFrame(self)
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

        # Mostrar dashboard por defecto
        self.show_dashboard()

    def setup_sidebar(self):
        # Frame de la barra lateral
        sidebar = ctk.CTkFrame(self, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_rowconfigure(7, weight=1)  # Espacio flexible antes del botón de logout

        # Logo o título
        logo_label = ctk.CTkLabel(
            sidebar,
            text="PokéDex App",
            font=("Roboto", 20, "bold")
        )
        logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Información del usuario
        user_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        user_frame.grid(row=1, column=0, padx=20, pady=(0, 20))

        user_label = ctk.CTkLabel(
            user_frame,
            text=f"¡Hola, {self.user_data['username']}!",
            font=("Roboto", 12)
        )
        user_label.pack()

        role_label = ctk.CTkLabel(
            user_frame,
            text=f"Rol: {self.user_data['role_name']}",
            font=("Roboto", 12)
        )
        role_label.pack()

        # Botones de navegación
        self.nav_buttons = []

        # Dashboard
        dashboard_btn = ctk.CTkButton(
            sidebar,
            text="Dashboard",
            command=self.show_dashboard,
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w"
        )
        dashboard_btn.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.nav_buttons.append(dashboard_btn)

        # Búsqueda
        search_btn = ctk.CTkButton(
            sidebar,
            text="Buscar Pokémon",
            command=self.show_search,
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w"
        )
        search_btn.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        self.nav_buttons.append(search_btn)

        # Mi Equipo
        team_btn = ctk.CTkButton(
            sidebar,
            text="Mi Equipo",
            command=self.show_team,
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w"
        )
        team_btn.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        self.nav_buttons.append(team_btn)

        # Perfil
        profile_btn = ctk.CTkButton(
            sidebar,
            text="Mi Perfil",
            command=self.show_profile,
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w"
        )
        profile_btn.grid(row=5, column=0, padx=20, pady=10, sticky="ew")
        self.nav_buttons.append(profile_btn)

        # Panel de Admin (solo si es admin)
        if self.user_data['role_name'] == 'admin':
            admin_btn = ctk.CTkButton(
                sidebar,
                text="Panel Admin",
                command=self.show_admin_panel,
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray70", "gray30"),
                anchor="w"
            )
            admin_btn.grid(row=6, column=0, padx=20, pady=10, sticky="ew")
            self.nav_buttons.append(admin_btn)

        # Botón de cerrar sesión
        logout_btn = ctk.CTkButton(
            sidebar,
            text="Cerrar Sesión",
            command=self.logout,
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w"
        )
        logout_btn.grid(row=8, column=0, padx=20, pady=20, sticky="ew")

    def show_dashboard(self):
        self.clear_main_container()
        self.set_active_button(0)
        
        # Crear dashboard
        dashboard = ctk.CTkFrame(self.main_container)
        dashboard.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        dashboard.grid_columnconfigure((0,1), weight=1)
        
        # Título
        title = ctk.CTkLabel(
            dashboard,
            text="Dashboard",
            font=("Roboto", 24, "bold")
        )
        title.grid(row=0, column=0, columnspan=2, pady=20, sticky="w")

        # Fecha actual
        date_label = ctk.CTkLabel(
            dashboard,
            text=f"Fecha: {datetime.now().strftime('%d/%m/%Y')}",
            font=("Roboto", 12)
        )
        date_label.grid(row=1, column=0, columnspan=2, pady=(0, 20), sticky="w")

        # Widgets del dashboard (placeholder)
        # Aquí puedes añadir estadísticas, gráficos, etc.
        stats_frame = ctk.CTkFrame(dashboard)
        stats_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        
        ctk.CTkLabel(
            stats_frame,
            text="Estadísticas",
            font=("Roboto", 16, "bold")
        ).pack(pady=10)
        
        # Añadir más widgets según necesites

    def show_search(self):
        self.clear_main_container()
        self.set_active_button(1)
        search_view = SearchView(self.main_container, self.user_data['id'])
        search_view.grid(row=0, column=0, sticky="nsew")

    def show_team(self):
        self.clear_main_container()
        self.set_active_button(2)
        # Aquí implementaremos la vista del equipo más adelante

    def show_profile(self):
        self.clear_main_container()
        self.set_active_button(3)
        profile_view = ProfileView(self.main_container, self.user_data)
        profile_view.grid(row=0, column=0, sticky="nsew")

    def show_admin_panel(self):
        if self.user_data['role_name'] != 'admin':
            return
        
        self.clear_main_container()
        self.set_active_button(4)
        # Aquí implementaremos el panel de administración más adelante

    def clear_main_container(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def set_active_button(self, index):
        for i, button in enumerate(self.nav_buttons):
            if i == index:
                button.configure(fg_color=("gray75", "gray25"))
            else:
                button.configure(fg_color="transparent")

    def logout(self):
        self.master.show_login()

    def show_team(self):
        self.clear_main_container()
        self.set_active_button(2)
        team_view = TeamView(self.main_container, self.user_data)
        team_view.grid(row=0, column=0, sticky="nsew")