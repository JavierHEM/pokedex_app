# Control de Equipo
# controllers/team_controller.py
from models.team_model import TeamModel
from services.api_service import PokeAPIService
from typing import Dict, List, Tuple
import logging

class TeamController:
    def __init__(self):
        self.team_model = TeamModel()
        self.api_service = PokeAPIService()
        self.logger = logging.getLogger(__name__)
        self.MAX_TEAM_SIZE = 10

    def get_trainer_pokemon(self, trainer_id: int) -> List[Dict]:
        """
        Obtiene la lista de Pokémon del entrenador
        """
        try:
            pokemon_list = self.team_model.get_trainer_pokemon(trainer_id)
            
            # Procesar los datos para la visualización
            for pokemon in pokemon_list:
                pokemon['types'] = pokemon['pokemon_type'].split(',')
                pokemon['moves'] = pokemon['moves'].split(',')
                
            return pokemon_list
        except Exception as e:
            self.logger.error(f"Error getting trainer's pokemon: {e}")
            return []

    def add_pokemon_to_team(self, trainer_id: int, pokemon_name: str, nickname: str = None) -> Tuple[bool, str]:
        """
        Añade un nuevo Pokémon al equipo
        """
        try:
            # Verificar límite del equipo
            current_count = self.team_model.get_team_count(trainer_id)
            if current_count >= self.MAX_TEAM_SIZE:
                return False, f"No puedes tener más de {self.MAX_TEAM_SIZE} Pokémon en tu equipo"

            # Obtener datos del Pokémon
            pokemon_data, message = self.api_service.get_pokemon_by_name_or_id(pokemon_name)
            if not pokemon_data:
                return False, "No se pudo obtener la información del Pokémon"

            # Añadir al equipo
            if self.team_model.add_pokemon(trainer_id, pokemon_data, nickname):
                return True, "Pokémon añadido exitosamente al equipo"
            return False, "Error al añadir el Pokémon al equipo"

        except Exception as e:
            self.logger.error(f"Error adding pokemon to team: {e}")
            return False, "Error al añadir el Pokémon al equipo"

    def remove_pokemon_from_team(self, pokemon_id: int, trainer_id: int) -> Tuple[bool, str]:
        """
        Elimina un Pokémon del equipo
        """
        try:
            # Verificar que el Pokémon existe y pertenece al entrenador
            pokemon = self.team_model.get_pokemon_by_id(pokemon_id, trainer_id)
            if not pokemon:
                return False, "Pokémon no encontrado en tu equipo"

            # Verificar que no es el último Pokémon
            current_count = self.team_model.get_team_count(trainer_id)
            if current_count <= 1:
                return False, "No puedes eliminar tu último Pokémon"

            if self.team_model.remove_pokemon(pokemon_id, trainer_id):
                return True, "Pokémon eliminado exitosamente del equipo"
            return False, "Error al eliminar el Pokémon del equipo"

        except Exception as e:
            self.logger.error(f"Error removing pokemon from team: {e}")
            return False, "Error al eliminar el Pokémon del equipo"

    def update_pokemon_nickname(self, pokemon_id: int, trainer_id: int, nickname: str) -> Tuple[bool, str]:
        """
        Actualiza el apodo de un Pokémon
        """
        try:
            # Verificar que el Pokémon existe y pertenece al entrenador
            pokemon = self.team_model.get_pokemon_by_id(pokemon_id, trainer_id)
            if not pokemon:
                return False, "Pokémon no encontrado en tu equipo"

            if not nickname:
                return False, "El apodo no puede estar vacío"

            if self.team_model.update_nickname(pokemon_id, trainer_id, nickname):
                return True, "Apodo actualizado exitosamente"
            return False, "Error al actualizar el apodo"

        except Exception as e:
            self.logger.error(f"Error updating pokemon nickname: {e}")
            return False, "Error al actualizar el apodo"

    def get_team_stats(self, trainer_id: int) -> Dict:
        """
        Obtiene estadísticas del equipo
        """
        try:
            pokemon_list = self.get_trainer_pokemon(trainer_id)
            
            stats = {
                'total_pokemon': len(pokemon_list),
                'types': {},
                'average_stats': {
                    'hp': 0,
                    'attack': 0,
                    'defense': 0,
                    'sp_attack': 0,
                    'sp_defense': 0,
                    'speed': 0
                },
                'strongest_pokemon': None,
                'fastest_pokemon': None
            }
            
            if not pokemon_list:
                return stats

            # Calcular estadísticas
            for pokemon in pokemon_list:
                # Contar tipos
                for type_name in pokemon['types']:
                    stats['types'][type_name] = stats['types'].get(type_name, 0) + 1
                
                # Sumar stats
                for stat in stats['average_stats'].keys():
                    stats['average_stats'][stat] += pokemon[f'stats_{stat}']
                
                # Encontrar el más fuerte y el más rápido
                if not stats['strongest_pokemon'] or pokemon['stats_attack'] > stats['strongest_pokemon']['stats_attack']:
                    stats['strongest_pokemon'] = pokemon
                    
                if not stats['fastest_pokemon'] or pokemon['stats_speed'] > stats['fastest_pokemon']['stats_speed']:
                    stats['fastest_pokemon'] = pokemon

            # Calcular promedios
            for stat in stats['average_stats'].keys():
                stats['average_stats'][stat] = round(stats['average_stats'][stat] / len(pokemon_list), 2)

            return stats

        except Exception as e:
            self.logger.error(f"Error calculating team stats: {e}")
            return {}