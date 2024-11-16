# Control de Pokemon y API
# controllers/pokemon_controller.py
from services.api_service import PokeAPIService
from models.search_model import SearchModel
from typing import Dict, List, Optional
import logging

class PokemonController:
    def __init__(self):
        self.api_service = PokeAPIService()
        self.search_model = SearchModel()
        self.logger = logging.getLogger(__name__)

    def search_pokemon(self, query: str, user_id: int) -> tuple[List[Dict], str]:
        """
        Busca Pokémon y registra la búsqueda
        """
        try:
            # Realizar búsqueda
            results = self.api_service.search_pokemon(query)
            
            # Registrar búsqueda en el historial
            if results:
                self.search_model.add_search(user_id, query)
            
            if not results:
                return [], "No se encontraron Pokémon que coincidan con la búsqueda."
            
            return results, "Búsqueda exitosa"

        except Exception as e:
            self.logger.error(f"Error en búsqueda de Pokémon: {str(e)}")
            return [], "Error al realizar la búsqueda"

    def get_pokemon_details(self, identifier: str) -> tuple[Optional[Dict], str]:
        """
        Obtiene detalles completos de un Pokémon
        """
        try:
            pokemon_data = self.api_service.get_pokemon_by_name_or_id(identifier)
            
            if not pokemon_data:
                return None, "No se pudo encontrar el Pokémon especificado"
            
            return pokemon_data, "Datos obtenidos exitosamente"

        except Exception as e:
            self.logger.error(f"Error al obtener detalles del Pokémon: {str(e)}")
            return None, "Error al obtener detalles del Pokémon"

    def get_recent_searches(self, user_id: int, limit: int = 10) -> List[Dict]:
        """
        Obtiene las búsquedas recientes del usuario
        """
        try:
            return self.search_model.get_user_searches(user_id, limit)
        except Exception as e:
            self.logger.error(f"Error al obtener búsquedas recientes: {str(e)}")
            return []

    def get_popular_searches(self, limit: int = 10) -> List[Dict]:
        """
        Obtiene las búsquedas más populares
        """
        try:
            return self.search_model.get_popular_searches(limit)
        except Exception as e:
            self.logger.error(f"Error al obtener búsquedas populares: {str(e)}")
            return []