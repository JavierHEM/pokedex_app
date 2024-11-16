# Modelo de Entrenador
# models/trainer_model.py
from config.database import DatabaseConnection
from typing import List, Dict, Optional, Tuple

class TrainerModel:
    def __init__(self):
        self.db = DatabaseConnection()

    def create_trainer(self, user_id: int, name: str, age: int = None, region: str = None) -> Tuple[bool, str]:
        """
        Crea un nuevo entrenador para un usuario
        """
        try:
            # Verificar si el usuario ya tiene un entrenador
            check_query = "SELECT id FROM trainers WHERE user_id = %s"
            if self.db.fetch_one(check_query, (user_id,)):
                return False, "El usuario ya tiene un entrenador asignado"

            # Insertar nuevo entrenador
            query = """
                INSERT INTO trainers (user_id, name, age, region)
                VALUES (%s, %s, %s, %s)
            """
            self.db.execute_query(query, (user_id, name, age, region))
            return True, "Entrenador creado exitosamente"

        except Exception as e:
            print(f"Error creating trainer: {str(e)}")
            return False, "Error al crear el entrenador"

    def get_trainer_by_user_id(self, user_id: int) -> Optional[Dict]:
        """
        Obtiene los datos del entrenador de un usuario
        """
        query = """
            SELECT t.*, 
                   (SELECT COUNT(*) FROM team_pokemon WHERE trainer_id = t.id) as pokemon_count
            FROM trainers t
            WHERE t.user_id = %s
        """
        return self.db.fetch_one(query, (user_id,))

    def get_trainer_by_id(self, trainer_id: int) -> Optional[Dict]:
        """
        Obtiene los datos de un entrenador por su ID
        """
        query = """
            SELECT t.*, 
                   u.username as user_username,
                   (SELECT COUNT(*) FROM team_pokemon WHERE trainer_id = t.id) as pokemon_count
            FROM trainers t
            JOIN users u ON t.user_id = u.id
            WHERE t.id = %s
        """
        return self.db.fetch_one(query, (trainer_id,))

    def update_trainer(self, trainer_id: int, data: Dict) -> Tuple[bool, str]:
        """
        Actualiza la información de un entrenador
        """
        try:
            # Construir query de actualización
            updates = []
            params = []
            if 'name' in data:
                updates.append("name = %s")
                params.append(data['name'])
            if 'age' in data:
                updates.append("age = %s")
                params.append(data['age'])
            if 'region' in data:
                updates.append("region = %s")
                params.append(data['region'])

            if not updates:
                return False, "No hay datos para actualizar"

            params.append(trainer_id)
            query = f"""
                UPDATE trainers 
                SET {', '.join(updates)}
                WHERE id = %s
            """
            
            self.db.execute_query(query, tuple(params))
            return True, "Entrenador actualizado exitosamente"

        except Exception as e:
            print(f"Error updating trainer: {str(e)}")
            return False, "Error al actualizar el entrenador"

    def delete_trainer(self, trainer_id: int) -> Tuple[bool, str]:
        """
        Elimina un entrenador y sus pokémon
        """
        try:
            # Iniciar transacción
            self.db.execute_query("START TRANSACTION")

            # Eliminar pokémon del entrenador
            self.db.execute_query(
                "DELETE FROM team_pokemon WHERE trainer_id = %s",
                (trainer_id,)
            )

            # Eliminar entrenador
            self.db.execute_query(
                "DELETE FROM trainers WHERE id = %s",
                (trainer_id,)
            )

            # Confirmar transacción
            self.db.execute_query("COMMIT")
            return True, "Entrenador eliminado exitosamente"

        except Exception as e:
            # Revertir en caso de error
            self.db.execute_query("ROLLBACK")
            print(f"Error deleting trainer: {str(e)}")
            return False, "Error al eliminar el entrenador"

    def get_trainer_stats(self, trainer_id: int) -> Dict:
        """
        Obtiene estadísticas detalladas del entrenador
        """
        try:
            stats = {
                'total_pokemon': 0,
                'favorite_types': [],
                'strongest_pokemon': None,
                'newest_pokemon': None,
                'pokemon_by_type': {},
                'total_base_experience': 0,
                'avg_pokemon_stats': {
                    'hp': 0, 'attack': 0, 'defense': 0,
                    'sp_attack': 0, 'sp_defense': 0, 'speed': 0
                }
            }

            # Obtener pokémon del entrenador
            pokemon_query = """
                SELECT *
                FROM team_pokemon
                WHERE trainer_id = %s
                ORDER BY joined_at DESC
            """
            pokemon_list = self.db.fetch_all(pokemon_query, (trainer_id,))

            if not pokemon_list:
                return stats

            stats['total_pokemon'] = len(pokemon_list)
            total_stats = {stat: 0 for stat in stats['avg_pokemon_stats'].keys()}
            max_total_stats = 0
            type_count = {}

            for pokemon in pokemon_list:
                # Contar tipos
                types = pokemon['pokemon_type'].split(',')
                for type_name in types:
                    type_count[type_name] = type_count.get(type_name, 0) + 1

                # Sumar estadísticas
                total_stats['hp'] += pokemon['stats_hp']
                total_stats['attack'] += pokemon['stats_attack']
                total_stats['defense'] += pokemon['stats_defense']
                total_stats['sp_attack'] += pokemon['stats_sp_attack']
                total_stats['sp_defense'] += pokemon['stats_sp_defense']
                total_stats['speed'] += pokemon['stats_speed']

                # Calcular pokémon más fuerte
                total_pokemon_stats = (
                    pokemon['stats_hp'] + pokemon['stats_attack'] + 
                    pokemon['stats_defense'] + pokemon['stats_sp_attack'] + 
                    pokemon['stats_sp_defense'] + pokemon['stats_speed']
                )
                if total_pokemon_stats > max_total_stats:
                    max_total_stats = total_pokemon_stats
                    stats['strongest_pokemon'] = {
                        'name': pokemon['pokemon_name'],
                        'nickname': pokemon['nickname'],
                        'total_stats': total_pokemon_stats
                    }

                stats['total_base_experience'] += pokemon['base_experience']

            # Calcular promedios
            for stat in total_stats:
                stats['avg_pokemon_stats'][stat] = round(
                    total_stats[stat] / len(pokemon_list), 2
                )

            # Obtener tipos favoritos (top 3)
            stats['favorite_types'] = sorted(
                type_count.items(),
                key=lambda x: x[1],
                reverse=True
            )[:3]

            # Pokémon más reciente
            stats['newest_pokemon'] = {
                'name': pokemon_list[0]['pokemon_name'],
                'nickname': pokemon_list[0]['nickname'],
                'joined_at': pokemon_list[0]['joined_at']
            }

            # Distribución por tipo
            stats['pokemon_by_type'] = type_count

            return stats

        except Exception as e:
            print(f"Error getting trainer stats: {str(e)}")
            return {}

    def get_trainers_by_region(self, region: str) -> List[Dict]:
        """
        Obtiene todos los entrenadores de una región específica
        """
        query = """
            SELECT t.*, u.username as user_username,
                   (SELECT COUNT(*) FROM team_pokemon WHERE trainer_id = t.id) as pokemon_count
            FROM trainers t
            JOIN users u ON t.user_id = u.id
            WHERE t.region = %s
            ORDER BY t.name
        """
        return self.db.fetch_all(query, (region,))

    def get_all_regions(self) -> List[str]:
        """
        Obtiene todas las regiones registradas
        """
        query = """
            SELECT DISTINCT region 
            FROM trainers 
            WHERE region IS NOT NULL 
            ORDER BY region
        """
        results = self.db.fetch_all(query)
        return [result['region'] for result in results]