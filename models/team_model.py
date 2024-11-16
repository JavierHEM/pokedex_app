# Modelo de Equipo
# models/team_model.py
from config.database import DatabaseConnection
from typing import List, Dict, Optional

class TeamModel:
    def __init__(self):
        self.db = DatabaseConnection()

    def get_trainer_pokemon(self, trainer_id: int) -> List[Dict]:
        """
        Obtiene todos los Pokémon del entrenador
        """
        query = """
            SELECT *
            FROM team_pokemon
            WHERE trainer_id = %s
            ORDER BY joined_at DESC
        """
        return self.db.fetch_all(query, (trainer_id,))

    def add_pokemon(self, trainer_id: int, pokemon_data: Dict, nickname: str = None) -> bool:
        """
        Añade un nuevo Pokémon al equipo
        """
        try:
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
            
            # Preparar los tipos de Pokémon como string
            pokemon_types = ','.join(pokemon_data['types'])
            # Preparar los movimientos como string
            moves = ','.join(pokemon_data['moves'])
            
            params = (
                trainer_id,
                pokemon_data['id'],
                nickname,
                pokemon_data['name'],
                pokemon_types,
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
                moves
            )
            
            self.db.execute_query(query, params)
            return True
        except Exception as e:
            print(f"Error adding pokemon to team: {e}")
            return False

    def remove_pokemon(self, pokemon_id: int, trainer_id: int) -> bool:
        """
        Elimina un Pokémon del equipo
        """
        try:
            query = """
                DELETE FROM team_pokemon
                WHERE id = %s AND trainer_id = %s
            """
            self.db.execute_query(query, (pokemon_id, trainer_id))
            return True
        except Exception as e:
            print(f"Error removing pokemon from team: {e}")
            return False

    def update_nickname(self, pokemon_id: int, trainer_id: int, nickname: str) -> bool:
        """
        Actualiza el apodo de un Pokémon
        """
        try:
            query = """
                UPDATE team_pokemon
                SET nickname = %s
                WHERE id = %s AND trainer_id = %s
            """
            self.db.execute_query(query, (nickname, pokemon_id, trainer_id))
            return True
        except Exception as e:
            print(f"Error updating pokemon nickname: {e}")
            return False

    def get_team_count(self, trainer_id: int) -> int:
        """
        Obtiene el número total de Pokémon en el equipo
        """
        query = """
            SELECT COUNT(*) as count
            FROM team_pokemon
            WHERE trainer_id = %s
        """
        result = self.db.fetch_one(query, (trainer_id,))
        return result['count'] if result else 0

    def get_pokemon_by_id(self, pokemon_id: int, trainer_id: int) -> Optional[Dict]:
        """
        Obtiene un Pokémon específico del equipo
        """
        query = """
            SELECT *
            FROM team_pokemon
            WHERE id = %s AND trainer_id = %s
        """
        return self.db.fetch_one(query, (pokemon_id, trainer_id))