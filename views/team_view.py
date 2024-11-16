# views/team_view.py
import customtkinter as ctk
from views.components.pokemon_card import PokemonCard
from views.components.stats_chart import StatsRadarChart
from controllers.team_controller import TeamController
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import io

class TeamView(ctk.CTkFrame):
    def __init__(self, master, user_data):
        super().__init__(master)
        self.user_data = user_data
        self.team_controller = TeamController()
        self.setup_ui()

    def setup_ui(self):
        # Configurar grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Panel izquierdo (lista de Pokémon)
        self.setup_pokemon_list()

        # Panel derecho (estadísticas)
        self.setup_stats_panel()

        # Cargar datos
        self.load_team_data()

    def setup_pokemon_list(self):
        # Frame para la lista de Pokémon
        list_frame = ctk.CTkFrame(self)
        list_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Título y contador
        title_frame = ctk.CTkFrame(list_frame, fg_color="transparent")
        title_frame.pack(fill="x", padx=10, pady=10)

        title = ctk.CTkLabel(
            title_frame,
            text="Mi Equipo",
            font=("Roboto", 20, "bold")
        )
        title.pack(side="left")

        self.counter_label = ctk.CTkLabel(
            title_frame,
            text="0/10",
            font=("Roboto", 14)
        )
        self.counter_label.pack(side="right")

        # Scroll frame para los Pokémon
        self.pokemon_list = ctk.CTkScrollableFrame(list_frame)
        self.pokemon_list.pack(fill="both", expand=True, padx=5, pady=5)

    def setup_stats_panel(self):
        # Frame para estadísticas
        self.stats_frame = ctk.CTkFrame(self)
        self.stats_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Título
        title = ctk.CTkLabel(
            self.stats_frame,
            text="Estadísticas del Equipo",
            font=("Roboto", 20, "bold")
        )
        title.pack(pady=10)

        # Frame para gráficos
        self.graphs_frame = ctk.CTkFrame(self.stats_frame)
        self.graphs_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def load_team_data(self):
        # Obtener datos del equipo
        pokemon_list = self.team_controller.get_team_pokemon(self.user_data['id'])
        team_stats = self.team_controller.get_detailed_stats(self.user_data['id'])

        # Actualizar contador
        self.counter_label.configure(text=f"{len(pokemon_list)}/10")

        # Limpiar lista actual
        for widget in self.pokemon_list.winfo_children():
            widget.destroy()

        # Mostrar Pokémon
        for pokemon in pokemon_list:
            self.create_pokemon_card(pokemon)

        # Actualizar estadísticas
        self.update_stats_display(team_stats)

    def create_pokemon_card(self, pokemon_data):
        # Frame para la tarjeta y botones
        card_frame = ctk.CTkFrame(self.pokemon_list)
        card_frame.pack(fill="x", pady=5, padx=5)

        # Crear tarjeta de Pokémon
        pokemon_card = PokemonCard(
            card_frame,
            pokemon_data,
            on_click=lambda: self.show_pokemon_details(pokemon_data)
        )
        pokemon_card.pack(side="left", fill="both", expand=True)

        # Frame para botones
        buttons_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        buttons_frame.pack(side="right", padx=5)

        # Botón de editar apodo
        edit_btn = ctk.CTkButton(
            buttons_frame,
            text="Editar Apodo",
            command=lambda: self.edit_nickname(pokemon_data['id'])
        )
        edit_btn.pack(pady=2)

        # Botón de eliminar
        delete_btn = ctk.CTkButton(
            buttons_frame,
            text="Eliminar",
            fg_color="red",
            hover_color="dark red",
            command=lambda: self.remove_pokemon(pokemon_data['id'])
        )
        delete_btn.pack(pady=2)

    def update_stats_display(self, stats):
        # Limpiar gráficos anteriores
        for widget in self.graphs_frame.winfo_children():
            widget.destroy()

        if not stats['total_pokemon']:
            no_stats = ctk.CTkLabel(
                self.graphs_frame,
                text="No hay Pokémon en el equipo",
                font=("Roboto", 14)
            )
            no_stats.pack(pady=20)
            return

        # Información general
        info_frame = ctk.CTkFrame(self.graphs_frame)
        info_frame.pack(fill="x", pady=10, padx=10)

        # Grid para información
        general_stats = ctk.CTkFrame(info_frame, fg_color="transparent")
        general_stats.pack(fill="x", pady=5)
        general_stats.grid_columnconfigure((0,1), weight=1)

        # Pokémon más fuerte
        if stats['strongest_pokemon']:
            strongest = ctk.CTkLabel(
                general_stats,
                text=f"Pokémon más fuerte: {stats['strongest_pokemon']}",
                font=("Roboto", 14)
            )
            strongest.grid(row=0, column=0, pady=5, sticky="w")

        # Pokémon más rápido
        if stats['fastest_pokemon']:
            fastest = ctk.CTkLabel(
                general_stats,
                text=f"Pokémon más rápido: {stats['fastest_pokemon']}",
                font=("Roboto", 14)
            )
            fastest.grid(row=0, column=1, pady=5, sticky="w")

        # Estadísticas promedio
        stats_chart = StatsRadarChart(
            self.graphs_frame,
            stats['average_stats']
        )
        stats_chart.pack(pady=10)

        # Distribución de tipos
        self.create_type_distribution_chart(stats['types_distribution'])

    def create_type_distribution_chart(self, type_distribution):
        if not type_distribution:
            return

        # Crear figura de matplotlib
        fig, ax = plt.subplots(figsize=(8, 4))
        types = list(type_distribution.keys())
        counts = list(type_distribution.values())

        # Crear gráfico de barras horizontal
        bars = ax.barh(types, counts)
        ax.set_title("Distribución de Tipos")
        
        # Personalizar gráfico
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.tight_layout()

        # Crear widget de canvas
        canvas = FigureCanvasTkAgg(fig, self.graphs_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, pady=10)

    def show_pokemon_details(self, pokemon_data):
        # Crear ventana de detalles
        details_window = ctk.CTkToplevel(self)
        details_window.title(f"Detalles de {pokemon_data['pokemon_name']}")
        details_window.geometry("600x700")

        # Frame principal
        main_frame = ctk.CTkFrame(details_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Información básica
        basic_info = ctk.CTkFrame(main_frame)
        basic_info.pack(fill="x", pady=10)

        # Nombre y apodo
        name_frame = ctk.CTkFrame(basic_info, fg_color="transparent")
        name_frame.pack(fill="x")

        ctk.CTkLabel(
            name_frame,
            text=pokemon_data['pokemon_name'],
            font=("Roboto", 24, "bold")
        ).pack(side="left", padx=10)

        if pokemon_data['nickname']:
            ctk.CTkLabel(
                name_frame,
                text=f'"{pokemon_data["nickname"]}"',
                font=("Roboto", 16, "italic")
            ).pack(side="left")

        # Estadísticas
        stats = {
            'hp': pokemon_data['stats_hp'],
            'attack': pokemon_data['stats_attack'],
            'defense': pokemon_data['stats_defense'],
            'sp_attack': pokemon_data['stats_sp_attack'],
            'sp_defense': pokemon_data['stats_sp_defense'],
            'speed': pokemon_data['stats_speed']
        }
        
        stats_chart = StatsRadarChart(main_frame, stats)
        stats_chart.pack(pady=20)

        # Movimientos
        moves_frame = ctk.CTkFrame(main_frame)
        moves_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(
            moves_frame,
            text="Movimientos",
            font=("Roboto", 16, "bold")
        ).pack(pady=5)

        for move in pokemon_data['moves']:
            ctk.CTkLabel(
                moves_frame,
                text=move
            ).pack(pady=2)

        # Información adicional
        info_frame = ctk.CTkFrame(main_frame)
        info_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(
            info_frame,
            text=f"Altura: {pokemon_data['height']}m | "
                 f"Peso: {pokemon_data['weight']}kg | "
                 f"Experiencia base: {pokemon_data['base_experience']}",
            font=("Roboto", 12)
        ).pack(pady=5)

        # Fecha de unión al equipo
        ctk.CTkLabel(
            info_frame,
            text=f"Se unió al equipo: {pokemon_data['joined_at'].strftime('%d/%m/%Y')}",
            font=("Roboto", 12)
        ).pack(pady=5)

    def edit_nickname(self, pokemon_id):
        # Crear ventana de edición
        edit_window = ctk.CTkToplevel(self)
        edit_window.title("Editar Apodo")
        edit_window.geometry("300x150")
        edit_window.resizable(False, False)

        # Entrada para el nuevo apodo
        nickname_entry = ctk.CTkEntry(
            edit_window,
            placeholder_text="Nuevo apodo"
        )
        nickname_entry.pack(padx=20, pady=20)

        # Botón de guardar
        def save_nickname():
            new_nickname = nickname_entry.get()
            success, message = self.team_controller.update_pokemon_nickname(
                pokemon_id, new_nickname
            )
            if success:
                self.load_team_data()
                edit_window.destroy()
            else:
                error_label.configure(text=message)

        save_btn = ctk.CTkButton(
            edit_window,
            text="Guardar",
            command=save_nickname
        )
        save_btn.pack(pady=10)

        # Label para errores
        error_label = ctk.CTkLabel(
            edit_window,
            text="",
            text_color="red"
        )
        error_label.pack()

    def remove_pokemon(self, pokemon_id):
        # Crear ventana de confirmación
        confirm_window = ctk.CTkToplevel(self)
        confirm_window.title("Confirmar Eliminación")
        confirm_window.geometry("300x150")
        confirm_window.resizable(False, False)

        ctk.CTkLabel(
            confirm_window,
            text="¿Estás seguro de que quieres\neliminar este Pokémon del equipo?",
            font=("Roboto", 14)
        ).pack(pady=20)

        buttons_frame = ctk.CTkFrame(confirm_window, fg_color="transparent")
        buttons_frame.pack(pady=10)

        def confirm_remove():
            success, message = self.team_controller.remove_pokemon_from_team(pokemon_id)
            if success:
                self.load_team_data()
                confirm_window.destroy()

        ctk.CTkButton(
            buttons_frame,
            text="Cancelar",
            command=confirm_window.destroy
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            buttons_frame,
            text="Eliminar",
            fg_color="red",
            hover_color="dark red",
            command=confirm_remove
        ).pack(side="left", padx=10)