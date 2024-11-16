# views/search_view.py
import customtkinter as ctk
from controllers.pokemon_controller import PokemonController
import os
from PIL import Image, ImageTk
import requests
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
from typing import Dict, Optional

class SearchView(ctk.CTkFrame):
    def __init__(self, master, user_id: int):
        super().__init__(master)
        self.master = master
        self.user_id = user_id
        self.pokemon_controller = PokemonController()
        
        # Cache para las imágenes
        self.image_cache = {}
        
        # Variable para el Pokémon seleccionado actualmente
        self.current_pokemon: Optional[Dict] = None
        
        self.setup_ui()

    def setup_ui(self):
        # Configurar el grid principal
        self.grid_columnconfigure(1, weight=3)  # Columna central más ancha
        self.grid_columnconfigure(0, weight=1)  # Barra lateral izquierda
        self.grid_columnconfigure(2, weight=1)  # Barra lateral derecha
        self.grid_rowconfigure(1, weight=1)

        # Barra de búsqueda superior
        self.setup_search_bar()
        
        # Panel izquierdo - Búsquedas recientes
        self.setup_recent_searches()
        
        # Panel central - Resultados de búsqueda
        self.setup_results_area()
        
        # Panel derecho - Detalles del Pokémon
        self.setup_details_panel()

    def setup_search_bar(self):
        search_frame = ctk.CTkFrame(self)
        search_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Buscar Pokémon...",
            width=300
        )
        self.search_entry.pack(side="left", padx=10, pady=10, fill="x", expand=True)
        
        self.search_button = ctk.CTkButton(
            search_frame,
            text="Buscar",
            command=self.perform_search
        )
        self.search_button.pack(side="right", padx=10, pady=10)
        
        # Bind Enter key to search
        self.search_entry.bind("<Return>", lambda event: self.perform_search())

    def setup_recent_searches(self):
        recent_frame = ctk.CTkFrame(self)
        recent_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        # Título
        title = ctk.CTkLabel(
            recent_frame,
            text="Búsquedas Recientes",
            font=("Roboto", 16, "bold")
        )
        title.pack(pady=10, padx=5)
        
        # Scrollable frame para las búsquedas recientes
        self.recent_scrollable = ctk.CTkScrollableFrame(recent_frame)
        self.recent_scrollable.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Cargar búsquedas recientes
        self.load_recent_searches()

    def setup_results_area(self):
        results_frame = ctk.CTkFrame(self)
        results_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        # Título
        self.results_title = ctk.CTkLabel(
            results_frame,
            text="Resultados de Búsqueda",
            font=("Roboto", 16, "bold")
        )
        self.results_title.pack(pady=10)
        
        # Scrollable frame para los resultados
        self.results_scrollable = ctk.CTkScrollableFrame(results_frame)
        self.results_scrollable.pack(fill="both", expand=True, padx=5, pady=5)

    def setup_details_panel(self):
        self.details_frame = ctk.CTkFrame(self)
        self.details_frame.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")
        
        # Título
        title = ctk.CTkLabel(
            self.details_frame,
            text="Detalles del Pokémon",
            font=("Roboto", 16, "bold")
        )
        title.pack(pady=10)
        
        # Frame para la imagen y detalles básicos
        self.pokemon_info_frame = ctk.CTkFrame(self.details_frame)
        self.pokemon_info_frame.pack(fill="x", padx=10, pady=5)
        
        # Label para la imagen
        self.pokemon_image_label = ctk.CTkLabel(self.pokemon_info_frame, text="")
        self.pokemon_image_label.pack(pady=10)
        
        # Labels para información básica
        self.pokemon_name_label = ctk.CTkLabel(
            self.pokemon_info_frame,
            text="",
            font=("Roboto", 14, "bold")
        )
        self.pokemon_name_label.pack(pady=5)
        
        self.pokemon_type_label = ctk.CTkLabel(self.pokemon_info_frame, text="")
        self.pokemon_type_label.pack(pady=2)
        
        self.pokemon_metrics_label = ctk.CTkLabel(self.pokemon_info_frame, text="")
        self.pokemon_metrics_label.pack(pady=2)
        
        # Frame para el gráfico de estadísticas
        self.stats_frame = ctk.CTkFrame(self.details_frame)
        self.stats_frame.pack(fill="both", expand=True, padx=10, pady=5)

    def perform_search(self):
        query = self.search_entry.get().strip()
        if not query:
            return
        
        # Limpiar resultados anteriores
        for widget in self.results_scrollable.winfo_children():
            widget.destroy()
        
        # Realizar búsqueda
        results, message = self.pokemon_controller.search_pokemon(query, self.user_id)
        
        if not results:
            no_results = ctk.CTkLabel(
                self.results_scrollable,
                text="No se encontraron resultados",
                font=("Roboto", 12)
            )
            no_results.pack(pady=20)
            return
        
        # Mostrar resultados
        for pokemon in results:
            self.create_pokemon_card(pokemon)
        
        # Actualizar búsquedas recientes
        self.load_recent_searches()

    def create_pokemon_card(self, pokemon: Dict):
        # Frame para la tarjeta
        card = ctk.CTkFrame(self.results_scrollable)
        card.pack(fill="x", padx=10, pady=5)
        
        # Contenedor para la imagen y la información
        content = ctk.CTkFrame(card)
        content.pack(fill="x", padx=5, pady=5)
        
        # Cargar imagen
        if pokemon['sprite'] in self.image_cache:
            photo = self.image_cache[pokemon['sprite']]
        else:
            photo = self.load_pokemon_image(pokemon['sprite'])
            self.image_cache[pokemon['sprite']] = photo
        
        if photo:
            image_label = ctk.CTkLabel(content, image=photo, text="")
            image_label.pack(side="left", padx=5)
        
        # Información del Pokémon
        info_frame = ctk.CTkFrame(content)
        info_frame.pack(side="left", fill="x", expand=True, padx=5)
        
        name_label = ctk.CTkLabel(
            info_frame,
            text=pokemon['name'],
            font=("Roboto", 14, "bold")
        )
        name_label.pack(anchor="w")
        
        types_label = ctk.CTkLabel(
            info_frame,
            text=f"Tipo: {', '.join(pokemon['types'])}"
        )
        types_label.pack(anchor="w")
        
        # Botón para ver detalles
        details_button = ctk.CTkButton(
            content,
            text="Ver Detalles",
            command=lambda p=pokemon: self.show_pokemon_details(p['name'])
        )
        details_button.pack(side="right", padx=5)

    def show_pokemon_details(self, pokemon_name: str):
        # Obtener detalles completos del Pokémon
        pokemon_data, message = self.pokemon_controller.get_pokemon_details(pokemon_name)
        if not pokemon_data:
            return
        
        self.current_pokemon = pokemon_data
        
        # Actualizar imagen
        photo = self.load_pokemon_image(pokemon_data['sprites']['official_artwork'])
        if photo:
            self.pokemon_image_label.configure(image=photo)
            self.pokemon_image_label.image = photo
        
        # Actualizar información básica
        self.pokemon_name_label.configure(text=pokemon_data['name'])
        self.pokemon_type_label.configure(text=f"Tipo: {', '.join(pokemon_data['types'])}")
        self.pokemon_metrics_label.configure(
            text=f"Altura: {pokemon_data['height']}m | Peso: {pokemon_data['weight']}kg"
        )
        
        # Crear gráfico de estadísticas
        self.create_stats_radar(pokemon_data['stats'])

    def create_stats_radar(self, stats: Dict):
        # Limpiar frame de estadísticas
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        # Crear figura de matplotlib
        fig = plt.figure(figsize=(4, 4))
        ax = fig.add_subplot(111, projection='polar')
        
        # Preparar datos
        stats_names = ['HP', 'Ataque', 'Defensa', 'Atq. Esp.', 'Def. Esp.', 'Velocidad']
        stats_values = [
            stats['hp'], stats['attack'], stats['defense'],
            stats['sp_attack'], stats['sp_defense'], stats['speed']
        ]
        
        # Añadir el primer valor al final para cerrar el polígono
        values = stats_values + [stats_values[0]]
        
        # Calcular ángulos
        angles = np.linspace(0, 2*np.pi, len(stats_names), endpoint=False)
        angles = np.concatenate((angles, [angles[0]]))  # Completar el círculo
        
        # Crear el gráfico
        ax.plot(angles, values)
        ax.fill(angles, values, alpha=0.25)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(stats_names)
        
        # Ajustar límites
        ax.set_ylim(0, 150)
        
        # Crear canvas de Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.stats_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def load_pokemon_image(self, url: str) -> Optional[ImageTk.PhotoImage]:
        try:
            response = requests.get(url)
            image = Image.open(BytesIO(response.content))
            image = image.resize((100, 100), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Error loading image: {str(e)}")
            return None

    def load_recent_searches(self):
        # Limpiar búsquedas anteriores
        for widget in self.recent_scrollable.winfo_children():
            widget.destroy()
        
        # Cargar búsquedas recientes
        recent_searches = self.pokemon_controller.get_recent_searches(self.user_id)
        
        for search in recent_searches:
            search_frame = ctk.CTkFrame(self.recent_scrollable)
            search_frame.pack(fill="x", padx=5, pady=2)
            
            search_button = ctk.CTkButton(
                search_frame,
                text=search['search_term'],
                command=lambda term=search['search_term']: self.search_from_recent(term)
            )
            search_button.pack(fill="x", padx=5, pady=2)

    def search_from_recent(self, term: str):
        self.search_entry.delete(0, 'end')
        self.search_entry.insert(0, term)
        self.perform_search()