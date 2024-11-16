# views/components/stats_chart.py
import customtkinter as ctk
import math

class StatsRadarChart(ctk.CTkCanvas):
    def __init__(self, master, stats, **kwargs):
        super().__init__(master, **kwargs)
        self.stats = stats
        self.configure(width=300, height=300)
        self.draw_chart()

    def draw_chart(self):
        # Limpiar canvas
        self.delete("all")
        
        # Configuración del gráfico
        center_x = 150
        center_y = 150
        max_radius = 120
        num_stats = 6
        angle_step = 2 * math.pi / num_stats
        
        # Dibujar líneas de fondo
        for i in range(5):
            radius = max_radius * (i + 1) / 5
            points = []
            for j in range(num_stats):
                angle = j * angle_step - math.pi / 2
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                points.extend([x, y])
            self.create_polygon(points, outline="gray70", fill="", smooth=True)
        
        # Dibujar líneas radiales
        for i in range(num_stats):
            angle = i * angle_step - math.pi / 2
            end_x = center_x + max_radius * math.cos(angle)
            end_y = center_y + max_radius * math.sin(angle)
            self.create_line(center_x, center_y, end_x, end_y, fill="gray70")
        
        # Dibujar estadísticas
        stats_values = [
            self.stats['hp'],
            self.stats['attack'],
            self.stats['defense'],
            self.stats['sp_attack'],
            self.stats['sp_defense'],
            self.stats['speed']
        ]
        
        # Normalizar valores (máximo 255 para stats de Pokémon)
        max_stat = 255
        points = []
        for i, stat in enumerate(stats_values):
            radius = (stat / max_stat) * max_radius
            angle = i * angle_step - math.pi / 2
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            points.extend([x, y])
        
        # Dibujar polígono de stats
        self.create_polygon(
            points,
            outline="#1f87ff",
            fill="#1f87ff50",
            width=2,
            smooth=True
        )
        
        # Añadir etiquetas
        stat_names = ['HP', 'Ataque', 'Defensa', 'Atq. Esp.', 'Def. Esp.', 'Velocidad']
        for i, name in enumerate(stat_names):
            angle = i * angle_step - math.pi / 2
            label_radius = max_radius + 20
            x = center_x + label_radius * math.cos(angle)
            y = center_y + label_radius * math.sin(angle)
            self.create_text(x, y, text=f"{name}\n{stats_values[i]}", anchor="center")