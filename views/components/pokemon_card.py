# views/components/pokemon_card.py
import customtkinter as ctk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import threading

class PokemonCard(ctk.CTkFrame):
    def __init__(self, master, pokemon_data, on_click=None, **kwargs):
        super().__init__(master, **kwargs)
        self.pokemon_data = pokemon_data
        self.on_click = on_click
        self.image_label = None
        self.sprite_image = None
        
        self.setup_ui()
        self.load_sprite()

    def setup_ui(self):
        # Configurar el frame
        self.configure(
            fg_color=("gray90", "gray16"),
            corner_radius=10,
            border_width=2,
            border_color=("gray70", "gray30")
        )

        # Contenedor para la imagen
        self.image_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.image_frame.pack(pady=10, padx=10)

        # Placeholder para la imagen
        self.image_label = ctk.CTkLabel(
            self.image_frame,
            text="Cargando...",
            width=96,
            height=96
        )
        self.image_label.pack()

        # Nombre del Pokémon
        self.name_label = ctk.CTkLabel(
            self,
            text=self.pokemon_data['name'],
            font=("Roboto", 16, "bold")
        )
        self.name_label.pack(pady=5)

        # Tipos
        types_frame = ctk.CTkFrame(self, fg_color="transparent")
        types_frame.pack(pady=5)

        for type_name in self.pokemon_data['types']:
            type_label = ctk.CTkLabel(
                types_frame,
                text=type_name.capitalize(),
                width=70,
                height=25,
                fg_color=self.get_type_color(type_name),
                corner_radius=12,
                text_color="white"
            )
            type_label.pack(side="left", padx=2)

        # Hacer clickeable la tarjeta
        if self.on_click:
            self.bind("<Button-1>", lambda e: self.on_click(self.pokemon_data))
            self.bind("<Enter>", self.on_enter)
            self.bind("<Leave>", self.on_leave)

    def load_sprite(self):
        def fetch_image():
            try:
                response = requests.get(self.pokemon_data['sprite'])
                image = Image.open(BytesIO(response.content))
                image = image.resize((96, 96), Image.Resampling.LANCZOS)
                self.sprite_image = ImageTk.PhotoImage(image)
                
                # Actualizar la UI en el hilo principal
                self.after(0, self.update_image)
            except Exception as e:
                print(f"Error loading sprite: {e}")

        # Iniciar la descarga en un hilo separado
        thread = threading.Thread(target=fetch_image)
        thread.start()

    def update_image(self):
        if self.sprite_image and self.image_label:
            self.image_label.configure(image=self.sprite_image, text="")

    def on_enter(self, event):
        self.configure(border_color=("blue", "light blue"))

    def on_leave(self, event):
        self.configure(border_color=("gray70", "gray30"))

    @staticmethod
    def get_type_color(type_name):
        colors = {
            'normal': '#A8A878',
            'fire': '#F08030',
            'water': '#6890F0',
            'electric': '#F8D030',
            'grass': '#78C850',
            'ice': '#98D8D8',
            'fighting': '#C03028',
            'poison': '#A040A0',
            'ground': '#E0C068',
            'flying': '#A890F0',
            'psychic': '#F85888',
            'bug': '#A8B820',
            'rock': '#B8A038',
            'ghost': '#705898',
            'dragon': '#7038F8',
            'dark': '#705848',
            'steel': '#B8B8D0',
            'fairy': '#EE99AC'
        }
        return colors.get(type_name.lower(), '#68A090')