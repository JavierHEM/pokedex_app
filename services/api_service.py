# services/api_service.py
import requests
import time
from typing import Dict, List, Optional
from services.logging_service import logger

class PokeAPIService:
    def __init__(self):
        self.base_url = "https://pokeapi.co/api/v2"
        self.session = requests.Session()

    def get_pokemon_by_name_or_id(self, identifier: str) -> Optional[Dict]:
        """
        Obtiene información detallada de un Pokémon por nombre o ID
        """
        start_time = time.time()
        try:
            # Convertir el identificador a minúsculas si es string
            if isinstance(identifier, str):
                identifier = identifier.lower()

            endpoint = f"/pokemon/{identifier}"
            response = self.session.get(f"{self.base_url}{endpoint}")
            response_time = time.time() - start_time
            
            # Log de la llamada a la API
            logger.log_api_call(
                endpoint=endpoint,
                method="GET",
                status_code=response.status_code,
                response_time=response_time
            )

            response.raise_for_status()
            pokemon_data = response.json()

            # Obtener información de la especie
            species_start_time = time.time()
            species_url = pokemon_data['species']['url']
            species_response = self.session.get(species_url)
            species_time = time.time() - species_start_time

            logger.log_api_call(
                endpoint=f"species/{identifier}",
                method="GET",
                status_code=species_response.status_code,
                response_time=species_time
            )

            species_data = species_response.json()

            # Obtener cadena evolutiva
            evo_start_time = time.time()
            evolution_url = species_data['evolution_chain']['url']
            evolution_response = self.session.get(evolution_url)
            evo_time = time.time() - evo_start_time

            logger.log_api_call(
                endpoint=f"evolution-chain/{identifier}",
                method="GET",
                status_code=evolution_response.status_code,
                response_time=evo_time
            )

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
                'description': self._get_pokemon_description(species_data),
                'base_experience': pokemon_data.get('base_experience', 0)
            }

            logger.log_api_call(
                endpoint=f"pokemon/{identifier}/complete",
                method="GET",
                status_code=200,
                response_time=time.time() - start_time
            )

            return processed_data

        except requests.exceptions.RequestException as e:
            logger.log_error(
                f"Error fetching pokemon {identifier}: {str(e)}",
                exc_info=True
            )
            return None

    def search_pokemon(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Busca Pokémon que coincidan con el término de búsqueda
        """
        start_time = time.time()
        try:
            # Obtener lista completa de Pokémon
            endpoint = "/pokemon?limit=1000"
            response = self.session.get(f"{self.base_url}{endpoint}")
            response_time = time.time() - start_time

            logger.log_api_call(
                endpoint=endpoint,
                method="GET",
                status_code=response.status_code,
                response_time=response_time
            )

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

            logger.log_api_call(
                endpoint=f"pokemon/search/{query}",
                method="GET",
                status_code=200,
                response_time=time.time() - start_time
            )

            return detailed_matches

        except requests.exceptions.RequestException as e:
            logger.log_error(
                f"Error searching pokemon with query {query}: {str(e)}",
                exc_info=True
            )
            return []

    def get_pokemon_types(self) -> List[str]:
        """
        Obtiene la lista de todos los tipos de Pokémon
        """
        start_time = time.time()
        try:
            endpoint = "/type"
            response = self.session.get(f"{self.base_url}{endpoint}")
            response_time = time.time() - start_time

            logger.log_api_call(
                endpoint=endpoint,
                method="GET",
                status_code=response.status_code,
                response_time=response_time
            )

            response.raise_for_status()
            types_data = response.json()
            return [type_info['name'] for type_info in types_data['results']]

        except requests.exceptions.RequestException as e:
            logger.log_error(
                f"Error fetching pokemon types: {str(e)}",
                exc_info=True
            )
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

        try:
            extract_evolution_data(chain)
            return evolution_chain
        except Exception as e:
            logger.log_error(
                f"Error processing evolution chain: {str(e)}",
                exc_info=True
            )
            return []

    def _get_pokemon_description(self, species_data: Dict) -> str:
        """
        Obtiene la descripción en español del Pokémon
        """
        try:
            for entry in species_data['flavor_text_entries']:
                if entry['language']['name'] == 'es':
                    return entry['flavor_text'].replace('\n', ' ').replace('\f', ' ')
            return "Descripción no disponible en español."
        except Exception as e:
            logger.log_error(
                f"Error getting pokemon description: {str(e)}",
                exc_info=True
            )
            return "Error al obtener la descripción."

    def download_sprite(self, url: str) -> Optional[bytes]:
        """
        Descarga una imagen sprite de un Pokémon
        """
        start_time = time.time()
        try:
            response = self.session.get(url)
            response_time = time.time() - start_time

            logger.log_api_call(
                endpoint="sprite_download",
                method="GET",
                status_code=response.status_code,
                response_time=response_time
            )

            response.raise_for_status()
            return response.content

        except requests.exceptions.RequestException as e:
            logger.log_error(
                f"Error downloading sprite from {url}: {str(e)}",
                exc_info=True
            )
            return None