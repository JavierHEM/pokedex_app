# Servicio de PokeAPI
# services/api_service.py
import requests
from typing import Dict, List, Optional
import logging

class PokeAPIService:
    def __init__(self):
        self.base_url = "https://pokeapi.co/api/v2"
        self.session = requests.Session()
        
        # Configurar logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def get_pokemon_by_name_or_id(self, identifier: str) -> Optional[Dict]:
        """
        Obtiene información detallada de un Pokémon por nombre o ID
        """
        try:
            # Convertir el identificador a minúsculas si es string
            if isinstance(identifier, str):
                identifier = identifier.lower()

            response = self.session.get(f"{self.base_url}/pokemon/{identifier}")
            response.raise_for_status()
            pokemon_data = response.json()

            # Obtener información de la especie para evoluciones y descripción
            species_url = pokemon_data['species']['url']
            species_response = self.session.get(species_url)
            species_data = species_response.json()

            # Obtener cadena evolutiva
            evolution_url = species_data['evolution_chain']['url']
            evolution_response = self.session.get(evolution_url)
            evolution_data = evolution_response.json()

            # Procesar y estructurar la información
            processed_data = {
                'id': pokemon_data['id'],
                'name': pokemon_data['name'].capitalize(),
                'height': pokemon_data['height'] / 10,  # Convertir a metros
                'weight': pokemon_data['weight'] / 10,  # Convertir a kilogramos
                'types': [t['type']['name'] for t in pokemon_data['types']],
                'stats': {
                    'hp': pokemon_data['stats'][0]['base_stat'],
                    'attack': pokemon_data['stats'][1]['base_stat'],
                    'defense': pokemon_data['stats'][2]['base_stat'],
                    'sp_attack': pokemon_data['stats'][3]['base_stat'],
                    'sp_defense': pokemon_data['stats'][4]['base_stat'],
                    'speed': pokemon_data['stats'][5]['base_stat']
                },
                'sprites': {
                    'front_default': pokemon_data['sprites']['front_default'],
                    'back_default': pokemon_data['sprites']['back_default'],
                    'official_artwork': pokemon_data['sprites']['other']['official-artwork']['front_default']
                },
                'moves': [move['move']['name'].replace('-', ' ').title() 
                         for move in pokemon_data['moves'][:4]],  # Limitamos a 4 movimientos
                'evolution_chain': self._process_evolution_chain(evolution_data['chain']),
                'description': self._get_pokemon_description(species_data)
            }

            return processed_data

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error al obtener datos del Pokémon {identifier}: {str(e)}")
            return None

    def search_pokemon(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Busca Pokémon que coincidan con el término de búsqueda
        """
        try:
            # Obtener lista completa de Pokémon
            response = self.session.get(f"{self.base_url}/pokemon?limit=1000")
            response.raise_for_status()
            all_pokemon = response.json()['results']

            # Filtrar por término de búsqueda
            matches = [
                pokemon for pokemon in all_pokemon
                if query.lower() in pokemon['name'].lower()
            ][:limit]

            # Obtener información detallada de cada coincidencia
            detailed_matches = []
            for match in matches:
                pokemon_data = self.get_pokemon_by_name_or_id(match['name'])
                if pokemon_data:
                    detailed_matches.append({
                        'id': pokemon_data['id'],
                        'name': pokemon_data['name'],
                        'types': pokemon_data['types'],
                        'sprite': pokemon_data['sprites']['front_default']
                    })

            return detailed_matches

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error en la búsqueda de Pokémon: {str(e)}")
            return []

    def _process_evolution_chain(self, chain: Dict) -> List[str]:
        """
        Procesa la cadena evolutiva de un Pokémon
        """
        evolution_chain = []
        
        def extract_evolution_data(evolution_data):
            evolution_chain.append(evolution_data['species']['name'].capitalize())
            for evolution in evolution_data.get('evolves_to', []):
                extract_evolution_data(evolution)

        extract_evolution_data(chain)
        return evolution_chain

    def _get_pokemon_description(self, species_data: Dict) -> str:
        """
        Obtiene la descripción en español del Pokémon
        """
        for entry in species_data['flavor_text_entries']:
            if entry['language']['name'] == 'es':
                return entry['flavor_text'].replace('\n', ' ').replace('\f', ' ')
        return "Descripción no disponible en español."

    def get_pokemon_types(self) -> List[str]:
        """
        Obtiene la lista de todos los tipos de Pokémon
        """
        try:
            response = self.session.get(f"{self.base_url}/type")
            response.raise_for_status()
            types_data = response.json()
            return [type_info['name'] for type_info in types_data['results']]
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error al obtener tipos de Pokémon: {str(e)}")
            return []

    def download_sprite(self, url: str) -> Optional[bytes]:
        """
        Descarga una imagen sprite de un Pokémon
        """
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error al descargar sprite: {str(e)}")
            return None