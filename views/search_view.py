# views/search_view.py
import customtkinter as ctk
from views.components.pokemon_card import PokemonCard
from views.components.stats_chart import StatsRadarChart
from controllers.pokemon_controller import PokemonController

class SearchView(ctk.CTkFrame):
    def __init__(self, master, user_id):
        super().__init__(master)
        self.user_id = user_id
        self.pokemon_controller = PokemonController()
        self.setup_ui()

    def setup_ui(self):
        # Configurar grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Frame de búsqueda
        self.search_frame = ctk.CTkFrame(self)
        self.search_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        # Entrada de búsqueda
        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="Buscar Pokémon...",
            width=300
        )
        self.search_entry.pack(side="left", padx=10, pady=10)
        self.search_entry.bind("<Return>", lambda e: self.search_pokemon())

        # Botón de búsqueda
        self.search_button = ctk.CTkButton(
            self.search_frame,
            text="Buscar",
            command=self.search_pokemon
        )
        self.search_button.pack(side="left", padx=10)

        # Frame para búsquedas recientes
        self.recent_frame = ctk.CTkFrame(self)
        self.recent_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        self.recent_label = ctk.CTkLabel(
            self.recent_frame,
            text="Búsquedas Recientes",
            font=("Roboto", 16, "bold")
        )
        self.recent_label.pack(pady=10)

        self.recent_searches = ctk.CTkScrollableFrame(self.recent_frame)
        self.recent_searches.pack(fill="both", expand=True, padx=5, pady=5)

        # Frame para resultados
        self.results_frame = ctk.CTkFrame(self)
        self.results_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        self.results_scroll = ctk.CTkScrollableFrame(self.results_frame)
        self.results_scroll.pack(fill="both", expand=True, padx=5, pady=5)

        # Frame para detalles del Pokémon
        self.details_frame = ctk.CTkFrame(self)
        
        # Cargar búsquedas recientes
        self.load_recent_searches()

    def search_pokemon(self):
        query = self.search_entry.get()
        if not query:
            return

        # Limpiar resultados anteriores
        for widget in self.results_scroll.winfo_children():
            widget.destroy()

        # Realizar búsqueda
        results, message = self.pokemon_controller.search_pokemon(query, self.user_id)

        if not results:
            no_results = ctk.CTkLabel(
                self.results_scroll,
                text=message,
                font=("Roboto", 14)
            )
            no_results.pack(pady=20)
            return

        # Mostrar resultados
        for pokemon in results:
            card = PokemonCard(
                self.results_scroll,
                pokemon,
                on_click=self.show_pokemon_details
            )
            card.pack(pady=10, padx=10, fill="x")

        # Actualizar búsquedas recientes
        self.load_recent_searches()

    def show_pokemon_details(self, pokemon_data):
        # Obtener detalles completos
        details, message = self.pokemon_controller.get_pokemon_details(pokemon_data['name'])
        
        if not details:
            return

        # Limpiar y mostrar frame de detalles
        for widget in self.details_frame.winfo_children():
            widget.destroy()

        self.details_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.results_frame.grid_remove()

        # Botón para volver
        back_button = ctk.CTkButton(
            self.details_frame,
            text="← Volver",
            command=self.show_results
        )
        back_button.pack(pady=10, padx=10, anchor="w")

        # Información básica
        info_frame = ctk.CTkFrame(self.details_frame)
        info_frame.pack(fill="x", padx=10, pady=10)

        # Crear tarjeta de Pokémon
        card = PokemonCard(info_frame, pokemon_data)
        card.pack(side="left", padx=20, pady=10)

        # Información adicional
        details_text = ctk.CTkTextbox(info_frame, height=150, width=400)
        details_text.pack(side="left", fill="both", expand=True, padx=20, pady=10)
        
        details_text.insert("1.0", f"""Descripción: {details['description']}

Altura: {details['height']} m
Peso: {details['weight']} kg

Movimientos:
{chr(10).join('- ' + move for move in details['moves'])}

Evoluciones:
{chr(10).join('- ' + evo for evo in details['evolution_chain'])}
""")
        details_text.configure(state="disabled")

        # Gráfico de estadísticas
        stats_chart = StatsRadarChart(
            self.details_frame,
            details['stats'],
            width=300,
            height=300
        )
        stats_chart.pack(pady=20)

    def show_results(self):
        self.details_frame.grid_remove()
        self.results_frame.grid()

    def load_recent_searches(self):
        # Limpiar búsquedas anteriores
        for widget in self.recent_searches.winfo_children():
            widget.destroy()

        # Cargar búsquedas recientes
        recent = self.pokemon_controller.get_recent_searches(self.user_id)

        for search in recent:
            search_button = ctk.CTkButton(
                self.recent_searches,
                text=search['search_term'],
                command=lambda term=search['search_term']: self.quick_search(term)
            )
            search_button.pack(pady=5, padx=10, fill="x")

    def quick_search(self, term):
        self.search_entry.delete(0, 'end')
        self.search_entry.insert(0, term)
        self.search_pokemon()