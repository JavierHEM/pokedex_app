# views/admin_view.py
import customtkinter as ctk
from controllers.admin_controller import AdminController
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AdminView(ctk.CTkFrame):
    def __init__(self, master, user_data):
        super().__init__(master)
        
        # Verificar si el usuario es administrador
        if user_data['role_name'] != 'admin':
            self.show_access_denied()
            return

        self.user_data = user_data
        self.admin_controller = AdminController()
        self.setup_ui()
        self.load_dashboard_data()

    def setup_ui(self):
        # Configurar grid principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Barra lateral con opciones
        self.setup_sidebar()

        # Contenedor principal
        self.main_container = ctk.CTkFrame(self)
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Mostrar dashboard por defecto
        self.show_dashboard()

    def setup_sidebar(self):
        sidebar = ctk.CTkFrame(self)
        sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Título
        title = ctk.CTkLabel(
            sidebar,
            text="Panel Admin",
            font=("Roboto", 20, "bold")
        )
        title.pack(pady=20)

        # Botones de navegación
        buttons_data = [
            ("Dashboard", self.show_dashboard),
            ("Usuarios", self.show_users_list),
            ("Actividad", self.show_activity_logs),
            ("Estadísticas", self.show_statistics)
        ]

        for text, command in buttons_data:
            btn = ctk.CTkButton(
                sidebar,
                text=text,
                command=command,
                width=200
            )
            btn.pack(pady=10, padx=20)

    def show_dashboard(self):
        """
        Muestra el dashboard principal del panel de administración
        """
        self.clear_main_container()
        
        # Título
        title = ctk.CTkLabel(
            self.main_container,
            text="Dashboard",
            font=("Roboto", 24, "bold")
        )
        title.pack(pady=20)

        # Grid de estadísticas
        stats_frame = ctk.CTkFrame(self.main_container)
        stats_frame.pack(fill="x", padx=20, pady=10)
        stats_frame.grid_columnconfigure((0,1,2), weight=1)

        # Obtener estadísticas
        stats = self.admin_controller.get_dashboard_stats()

        # Tarjetas de estadísticas principales
        self.create_stat_card(stats_frame, "Usuarios Totales", 
                            str(stats['total_users']), 0, 0)
        self.create_stat_card(stats_frame, "Búsquedas Totales", 
                            str(stats['total_searches']), 0, 1)
        self.create_stat_card(stats_frame, "Pokémon en Equipos", 
                            str(stats['total_pokemon']), 0, 2)

        # Frame para gráficos
        charts_frame = ctk.CTkFrame(self.main_container)
        charts_frame.pack(fill="both", expand=True, padx=20, pady=10)
        charts_frame.grid_columnconfigure((0,1), weight=1)
        charts_frame.grid_rowconfigure((0,1), weight=1)

        # Gráfico de búsquedas de los últimos 7 días
        self.create_line_chart(
            charts_frame,
            stats['searches_last_7_days'],
            "Búsquedas últimos 7 días",
            0, 0
        )

        # Gráfico de usuarios por rol
        self.create_pie_chart(
            charts_frame,
            stats['users_by_role'],
            "Distribución de Roles",
            0, 1
        )

        # Frame para información adicional
        info_frame = ctk.CTkFrame(self.main_container)
        info_frame.pack(fill="x", padx=20, pady=10)
        info_frame.grid_columnconfigure((0,1), weight=1)

        # Registros recientes
        recent_frame = ctk.CTkFrame(info_frame)
        recent_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        ctk.CTkLabel(
            recent_frame,
            text="Registros Recientes",
            font=("Roboto", 16, "bold")
        ).pack(pady=10)

        for user in stats['recent_registrations']:
            user_frame = ctk.CTkFrame(recent_frame)
            user_frame.pack(fill="x", padx=10, pady=2)
            
            ctk.CTkLabel(
                user_frame,
                text=user['username'],
                font=("Roboto", 12, "bold")
            ).pack(side="left", padx=5)
            
            ctk.CTkLabel(
                user_frame,
                text=user['created_at'].strftime('%d/%m/%Y'),
                font=("Roboto", 12)
            ).pack(side="right", padx=5)

        # Pokémon populares
        popular_frame = ctk.CTkFrame(info_frame)
        popular_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        ctk.CTkLabel(
            popular_frame,
            text="Pokémon más Populares",
            font=("Roboto", 16, "bold")
        ).pack(pady=10)

        for pokemon in stats['popular_pokemon']:
            pokemon_frame = ctk.CTkFrame(popular_frame)
            pokemon_frame.pack(fill="x", padx=10, pady=2)
            
            ctk.CTkLabel(
                pokemon_frame,
                text=pokemon['pokemon_name'],
                font=("Roboto", 12, "bold")
            ).pack(side="left", padx=5)
            
            ctk.CTkLabel(
                pokemon_frame,
                text=f"× {pokemon['total']}",
                font=("Roboto", 12)
            ).pack(side="right", padx=5)

        # Actualización automática
        self.after(300000, self.show_dashboard)  # Actualizar cada 5 minutos

    def create_stat_card(self, parent, title: str, value: str, row: int, column: int):
        """
        Crea una tarjeta de estadística
        """
        card = ctk.CTkFrame(parent)
        card.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(
            card,
            text=title,
            font=("Roboto", 14)
        ).pack(pady=(10, 0))

        ctk.CTkLabel(
            card,
            text=value,
            font=("Roboto", 24, "bold")
        ).pack(pady=(0, 10))

    def show_users_list(self):
        """
        Muestra la lista de usuarios
        """
        self.clear_main_container()

        # Título
        title_frame = ctk.CTkFrame(self.main_container)
        title_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            title_frame,
            text="Gestión de Usuarios",
            font=("Roboto", 24, "bold")
        ).pack(side="left", pady=10)

        # Tabla de usuarios
        table_frame = ctk.CTkScrollableFrame(self.main_container)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Encabezados
        headers = ["Usuario", "Email", "Rol", "Registro", "Búsquedas", "Pokémon", "Acciones"]
        for i, header in enumerate(headers):
            ctk.CTkLabel(
                table_frame,
                text=header,
                font=("Roboto", 12, "bold")
            ).grid(row=0, column=i, padx=5, pady=5, sticky="w")

        # Obtener y mostrar usuarios
        users = self.admin_controller.get_users_list()
        for i, user in enumerate(users, start=1):
            # Usuario
            ctk.CTkLabel(
                table_frame,
                text=user['username']
            ).grid(row=i, column=0, padx=5, pady=5, sticky="w")

            # Email
            ctk.CTkLabel(
                table_frame,
                text=user['email']
            ).grid(row=i, column=1, padx=5, pady=5, sticky="w")

            # Rol
            role_frame = ctk.CTkFrame(table_frame)
            role_frame.grid(row=i, column=2, padx=5, pady=5)

            role_var = ctk.StringVar(value=user['role_name'])
            role_menu = ctk.CTkOptionMenu(
                role_frame,
                values=['user', 'admin'],
                variable=role_var,
                command=lambda uid=user['id'], rv=role_var: self.update_user_role(uid, rv.get())
            )
            role_menu.pack()

            # Fecha de registro
            ctk.CTkLabel(
                table_frame,
                text=user['created_at'].strftime('%d/%m/%Y')
            ).grid(row=i, column=3, padx=5, pady=5)

            # Búsquedas
            ctk.CTkLabel(
                table_frame,
                text=str(user['total_searches'])
            ).grid(row=i, column=4, padx=5, pady=5)

            # Pokémon
            ctk.CTkLabel(
                table_frame,
                text=str(user['total_pokemon'])
            ).grid(row=i, column=5, padx=5, pady=5)

            # Botones de acción
            actions_frame = ctk.CTkFrame(table_frame)
            actions_frame.grid(row=i, column=6, padx=5, pady=5)

            ctk.CTkButton(
                actions_frame,
                text="Detalles",
                command=lambda uid=user['id']: self.show_user_details(uid)
            ).pack(side="left", padx=2)

            ctk.CTkButton(
                actions_frame,
                text="Eliminar",
                fg_color="red",
                hover_color="dark red",
                command=lambda uid=user['id']: self.confirm_delete_user(uid)
            ).pack(side="left", padx=2)

    def show_activity_logs(self):
        """
        Muestra los logs de actividad
        """
        self.clear_main_container()

        # Título
        ctk.CTkLabel(
            self.main_container,
            text="Logs de Actividad",
            font=("Roboto", 24, "bold")
        ).pack(pady=20)

        # Filtros
        filters_frame = ctk.CTkFrame(self.main_container)
        filters_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            filters_frame,
            text="Filtrar por:",
            font=("Roboto", 12)
        ).pack(side="left", padx=10)

        filter_var = ctk.StringVar(value="Todos")
        filter_menu = ctk.CTkOptionMenu(
            filters_frame,
            values=["Todos", "Búsquedas", "Equipos"],
            variable=filter_var,
            command=self.filter_activity_logs
        )
        filter_menu.pack(side="left", padx=10)

        # Tabla de logs
        logs_frame = ctk.CTkScrollableFrame(self.main_container)
        logs_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Encabezados
        headers = ["Fecha", "Usuario", "Actividad", "Detalle"]
        for i, header in enumerate(headers):
            ctk.CTkLabel(
                logs_frame,
                text=header,
                font=("Roboto", 12, "bold")
            ).grid(row=0, column=i, padx=5, pady=5, sticky="w")

        # Obtener y mostrar logs
        logs = self.admin_controller.get_recent_activity()
        for i, log in enumerate(logs, start=1):
            # Fecha
            ctk.CTkLabel(
                logs_frame,
                text=log['activity_date'].strftime('%d/%m/%Y %H:%M')
            ).grid(row=i, column=0, padx=5, pady=5)

            # Usuario
            ctk.CTkLabel(
                logs_frame,
                text=log['username']
            ).grid(row=i, column=1, padx=5, pady=5)

            # Tipo de actividad
            activity_label = ctk.CTkLabel(
                logs_frame,
                text=log['type'].capitalize()
            )
            activity_label.grid(row=i, column=2, padx=5, pady=5)

            # Color según tipo
            if log['type'] == 'search':
                activity_label.configure(text_color="blue")
            elif log['type'] == 'team_update':
                activity_label.configure(text_color="green")

            # Detalle
            ctk.CTkLabel(
                logs_frame,
                text=log['detail']
            ).grid(row=i, column=3, padx=5, pady=5)

    def show_statistics(self):
        """
        Muestra estadísticas detalladas
        """
        self.clear_main_container()

        # Título
        ctk.CTkLabel(
            self.main_container,
            text="Estadísticas del Sistema",
            font=("Roboto", 24, "bold")
        ).pack(pady=20)

        stats = self.admin_controller.get_dashboard_stats()

        # Grid de gráficos
        charts_frame = ctk.CTkFrame(self.main_container)
        charts_frame.pack(fill="both", expand=True, padx=20, pady=10)
        charts_frame.grid_columnconfigure((0,1), weight=1)
        charts_frame.grid_rowconfigure((0,1), weight=1)

        # Gráfico de usuarios por rol
        self.create_pie_chart(
            charts_frame,
            stats['users_by_role'],
            "Usuarios por Rol",
            0, 0
        )

        # Gráfico de búsquedas últimos 7 días
        self.create_line_chart(
            charts_frame,
            stats['searches_last_7_days'],
            "Búsquedas últimos 7 días",
            0, 1
        )

        # Gráfico de pokémon populares
        self.create_bar_chart(
            charts_frame,
            stats['popular_pokemon'],
            "Pokémon más Populares",
            1, 0
        )

        # Gráfico de regiones populares
        self.create_bar_chart(
            charts_frame,
            stats['popular_regions'],
            "Regiones más Populares",
            1, 1
        )

    def create_pie_chart(self, parent, data: dict, title: str, row: int, column: int):
        """
        Crea un gráfico circular
        """
        frame = ctk.CTkFrame(parent)
        frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.pie(
            data.values(),
            labels=data.keys(),
            autopct='%1.1f%%',
            startangle=90
        )
        ax.set_title(title)

        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def create_line_chart(self, parent, data: list, title: str, row: int, column: int):
        """
        Crea un gráfico de línea
        """
        frame = ctk.CTkFrame(parent)
        frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

        fig, ax = plt.subplots(figsize=(6, 4))
        dates = [row['date'] for row in data]
        values = [row['total'] for row in data]
        
        ax.plot(dates, values, marker='o')
        ax.set_title(title)
        ax.tick_params(axis='x', rotation=45)
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def create_bar_chart(self, parent, data: list, title: str, row: int, column: int):
        """
        Crea un gráfico de barras
        """
        frame = ctk.CTkFrame(parent)
        frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

        fig, ax = plt.subplots(figsize=(6, 4))
        names = [row['name'] if 'name' in row else row['pokemon_name'] 
                for row in data]
        values = [row['total'] for row in data]
        
        ax.bar(names, values)
        ax.set_title(title)
        ax.tick_params(axis='x', rotation=45)
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def update_user_role(self, user_id: int, new_role: str):
        """
        Actualiza el rol de un usuario
        """
        success, message = self.admin_controller.update_user_role(user_id, new_role)
        if success:
            self.show_message(message)
            self.show_users_list()  # Recargar lista
        else:
            self.show_error(message)

    def confirm_delete_user(self, user_id: int):
        """
        Muestra diálogo de confirmación para eliminar usuario
        """
        dialog = ctk.CTkToplevel(self)
        dialog.title("Confirmar Eliminación")
        dialog.geometry("300x150")
        dialog.resizable(False, False)

        ctk.CTkLabel(
            dialog,
            text="¿Estás seguro de que quieres\neliminar este usuario?",
            font=("Roboto", 14)
        ).pack(pady=20)

        buttons_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        buttons_frame.pack(pady=10)

        ctk.CTkButton(
            buttons_frame,
            text="Cancelar",
            command=dialog.destroy
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            buttons_frame,
            text="Eliminar",
            fg_color="red",
            hover_color="dark red",
            command=lambda: self.delete_user(user_id, dialog)
        ).pack(side="left", padx=10)

    def delete_user(self, user_id: int, dialog=None):
        """
        Elimina un usuario
        """
        success, message = self.admin_controller.delete_user(user_id)
        if success:
            self.show_message(message)
            if dialog:
                dialog.destroy()
            self.show_users_list()  # Recargar lista
        else:
            self.show_error(message)

    def show_user_details(self, user_id: int):
        """
        Muestra los detalles de un usuario
        """
        success, user_data = self.admin_controller.get_user_details(user_id)
        if not success:
            self.show_error(user_data.get('error', "Error al obtener detalles"))
            return

        # Crear ventana de detalles
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"Detalles de Usuario: {user_data['username']}")
        dialog.geometry("500x600")

        # Frame principal
        main_frame = ctk.CTkFrame(dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Información básica
        ctk.CTkLabel(
            main_frame,
            text="Información de Usuario",
            font=("Roboto", 16, "bold")
        ).pack(pady=10)

        info_frame = ctk.CTkFrame(main_frame)
        info_frame.pack(fill="x", pady=10)

        # Datos del usuario
        details = [
            ("Usuario:", user_data['username']),
            ("Email:", user_data['email']),
            ("Rol:", user_data['role_name']),
            ("Registro:", user_data['created_at'].strftime('%d/%m/%Y')),
        ]

        for label, value in details:
            row = ctk.CTkFrame(info_frame)
            row.pack(fill="x", pady=2)
            
            ctk.CTkLabel(
                row,
                text=label,
                font=("Roboto", 12, "bold")
            ).pack(side="left", padx=5)
            
            ctk.CTkLabel(
                row,
                text=str(value)
            ).pack(side="left", padx=5)

        # Información del entrenador
        ctk.CTkLabel(
            main_frame,
            text="Información de Entrenador",
            font=("Roboto", 16, "bold")
        ).pack(pady=(20,10))

        trainer_frame = ctk.CTkFrame(main_frame)
        trainer_frame.pack(fill="x", pady=10)

        trainer_details = [
            ("Nombre:", user_data.get('trainer_name', 'No especificado')),
            ("Edad:", str(user_data.get('trainer_age', 'No especificada'))),
            ("Región:", user_data.get('trainer_region', 'No especificada')),
        ]

        for label, value in trainer_details:
            row = ctk.CTkFrame(trainer_frame)
            row.pack(fill="x", pady=2)
            
            ctk.CTkLabel(
                row,
                text=label,
                font=("Roboto", 12, "bold")
            ).pack(side="left", padx=5)
            
            ctk.CTkLabel(
                row,
                text=value
            ).pack(side="left", padx=5)

        # Estadísticas del usuario
        stats = self.admin_controller.get_user_stats(user_id)
        
        ctk.CTkLabel(
            main_frame,
            text="Estadísticas",
            font=("Roboto", 16, "bold")
        ).pack(pady=(20,10))

        stats_frame = ctk.CTkFrame(main_frame)
        stats_frame.pack(fill="x", pady=10)

        stats_details = [
            ("Total de búsquedas:", str(stats['total_searches'])),
            ("Pokémon en equipo:", f"{stats['total_pokemon']}/10"),
            ("Última búsqueda:", 
            stats['last_search'].strftime('%d/%m/%Y %H:%M') if stats['last_search'] else 'Nunca'),
        ]

        for label, value in stats_details:
            row = ctk.CTkFrame(stats_frame)
            row.pack(fill="x", pady=2)
            
            ctk.CTkLabel(
                row,
                text=label,
                font=("Roboto", 12, "bold")
            ).pack(side="left", padx=5)
            
            ctk.CTkLabel(
                row,
                text=value
            ).pack(side="left", padx=5)

        # Botones de acción
        buttons_frame = ctk.CTkFrame(main_frame)
        buttons_frame.pack(fill="x", pady=20)

        # Botón de cambiar rol
        role_frame = ctk.CTkFrame(buttons_frame)
        role_frame.pack(side="left", padx=5)

        ctk.CTkLabel(
            role_frame,
            text="Rol:",
            font=("Roboto", 12)
        ).pack(side="left", padx=5)

        role_var = ctk.StringVar(value=user_data['role_name'])
        role_menu = ctk.CTkOptionMenu(
            role_frame,
            values=['user', 'admin'],
            variable=role_var,
            command=lambda v: self.update_user_role(user_id, v)
        )
        role_menu.pack(side="left", padx=5)

        # Botón de eliminar
        ctk.CTkButton(
            buttons_frame,
            text="Eliminar Usuario",
            fg_color="red",
            hover_color="dark red",
            command=lambda: self.confirm_delete_user(user_id)
        ).pack(side="right", padx=5)

        # Botón de cerrar
        ctk.CTkButton(
            main_frame,
            text="Cerrar",
            command=dialog.destroy
        ).pack(pady=10)

        # Centrar la ventana
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'+{x}+{y}')