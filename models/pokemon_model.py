# Modelo de Pokemon
# models/pokemon_model.py
from config.database import DatabaseConnection
from typing import List, Dict, Optional, Tuple

class PokemonModel:
    def __init__(self):
        self.db = DatabaseConnection()

    def save_pokemon(self, trainer_id: int, pokemon_data: Dict, nickname: str = None) -> Tuple[bool, str]:
        """
        Guarda un nuevo Pokémon en el equipo del entrenador
        """
        try:
            # Verificar si el entrenador existe
            trainer_query = "SELECT id FROM trainers WHERE id = %s"
            if not self.db.fetch_one(trainer_query, (trainer_id,)):
                return False, "Entrenador no encontrado"

            # Verificar límite de pokémon (máximo 10)
            count_query = """
                SELECT COUNT(*) as count 
                FROM team_pokemon 
                WHERE trainer_id = %s
            """
            result = self.db.fetch_one(count_query, (trainer_id,))
            if result['count'] >= 10:
                return False, "Ya tienes el máximo de 10 Pokémon en tu equipo"

            # Insertar el Pokémon
            query = """
                INSERT INTO team_pokemon (
                    trainer_id, pokemon_id, nickname, pokemon_name,
                    pokemon_type, height, weight, base_experience,
                    sprite_url, stats_hp, stats_attack, stats_defense,
                    stats_sp_attack, stats_sp_defense, stats_speed, moves
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """
            
            params = (
                trainer_id,
                pokemon_data['id'],
                nickname,
                pokemon_data['name'],
                ','.join(pokemon_data['types']),
                pokemon_data['height'],
                pokemon_data['weight'],
                pokemon_data.get('base_experience', 0),
                pokemon_data['sprites']['front_default'],
                pokemon_data['stats']['hp'],
                pokemon_data['stats']['attack'],
                pokemon_data['stats']['defense'],
                pokemon_data['stats']['sp_attack'],
                pokemon_data['stats']['sp_defense'],
                pokemon_data['stats']['speed'],
                ','.join(pokemon_data['moves'])
            )

            self.db.execute_query(query, params)
            return True, "Pokémon añadido exitosamente al equipo"

        except Exception as e:
            print(f"Error saving pokemon: {str(e)}")
            return False, "Error al guardar el Pokémon en la base de datos"

    def get_trainer_pokemon(self, trainer_id: int) -> List[Dict]:
        """
        Obtiene todos los Pokémon de un entrenador
        """
        query = """
            SELECT * FROM team_pokemon 
            WHERE trainer_id = %s 
            ORDER BY joined_at DESC
        """
        return self.db.fetch_all(query, (trainer_id,))

    def get_pokemon_by_id(self, pokemon_id: int) -> Optional[Dict]:
        """
        Obtiene un Pokémon específico por su ID
        """
        query = "SELECT * FROM team_pokemon WHERE id = %s"
        return self.db.fetch_one(query, (pokemon_id,))

    def update_nickname(self, pokemon_id: int, new_nickname: str) -> Tuple[bool, str]:
        """
        Actualiza el apodo de un Pokémon
        """
        try:
            if len(new_nickname) > 50:
                return False, "El apodo no puede tener más de 50 caracteres"

            query = "UPDATE team_pokemon SET nickname = %s WHERE id = %s"
            self.db.execute_query(query, (new_nickname, pokemon_id))
            return True, "Apodo actualizado exitosamente"

        except Exception as e:
            print(f"Error updating nickname: {str(e)}")
            return False, "Error al actualizar el apodo"

    def remove_pokemon(self, pokemon_id: int) -> Tuple[bool, str]:
        """
        Elimina un Pokémon del equipo
        """
        try:
            query = "DELETE FROM team_pokemon WHERE id = %s"
            self.db.execute_query(query, (pokemon_id,))
            return True, "Pokémon eliminado exitosamente"

        except Exception as e:
            print(f"Error removing pokemon: {str(e)}")
            return False, "Error al eliminar el Pokémon"

    def get_pokemon_stats(self, trainer_id: int) -> Dict:
        """
        Obtiene estadísticas de los Pokémon del entrenador
        """
        try:
            stats = {
                'total_pokemon': 0,
                'types': {},
                'average_stats': {
                    'hp': 0,
                    'attack': 0,
                    'defense': 0,
                    'sp_attack': 0,
                    'sp_defense': 0,
                    'speed': 0
                },
                'highest_stat_pokemon': {
                    'hp': None,
                    'attack': None,
                    'defense': None,
                    'sp_attack': None,
                    'sp_defense': None,
                    'speed': None
                }
            }

            pokemon_list = self.get_trainer_pokemon(trainer_id)
            if not pokemon_list:
                return stats

            stats['total_pokemon'] = len(pokemon_list)
            total_stats = {stat: 0 for stat in stats['average_stats'].keys()}

            for pokemon in pokemon_list:
                # Contar tipos
                for type_name in pokemon['pokemon_type'].split(','):
                    stats['types'][type_name] = stats['types'].get(type_name, 0) + 1

                # Sumar estadísticas
                total_stats['hp'] += pokemon['stats_hp']
                total_stats['attack'] += pokemon['stats_attack']
                total_stats['defense'] += pokemon['stats_defense']
                total_stats['sp_attack'] += pokemon['stats_sp_attack']
                total_stats['sp_defense'] += pokemon['stats_sp_defense']
                total_stats['speed'] += pokemon['stats_speed']

                # Actualizar pokémon con estadísticas más altas
                if not stats['highest_stat_pokemon']['hp'] or \
                   pokemon['stats_hp'] > stats['highest_stat_pokemon']['hp']['value']:
                    stats['highest_stat_pokemon']['hp'] = {
                        'name': pokemon['pokemon_name'],
                        'value': pokemon['stats_hp']
                    }
                # Repetir para otras estadísticas...

            # Calcular promedios
            for stat in total_stats:
                stats['average_stats'][stat] = round(
                    total_stats[stat] / len(pokemon_list), 2
                )

            return stats

        except Exception as e:
            print(f"Error getting pokemon stats: {str(e)}")
            return {}

    def search_pokemon_by_name(self, trainer_id: int, name: str) -> List[Dict]:
        """
        Busca Pokémon en el equipo por nombre
        """
        query = """
            SELECT * FROM team_pokemon 
            WHERE trainer_id = %s 
            AND (pokemon_name LIKE %s OR nickname LIKE %s)
            ORDER BY joined_at DESC
        """
        search_term = f"%{name}%"
        return self.db.fetch_all(query, (trainer_id, search_term, search_term))

    def get_pokemon_moves(self, pokemon_id: int) -> List[str]:
        """
        Obtiene los movimientos de un Pokémon
        """
        query = "SELECT moves FROM team_pokemon WHERE id = %s"
        result = self.db.fetch_one(query, (pokemon_id,))
        if result and result['moves']:
            return result['moves'].split(',')
        return []