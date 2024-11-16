# models/admin_model.py
from config.database import DatabaseConnection
from typing import List, Dict, Tuple, Optional
from datetime import datetime

class AdminModel:
    def __init__(self):
        self.db = DatabaseConnection()

    def get_all_users(self) -> List[Dict]:
        """
        Obtiene todos los usuarios con sus datos básicos
        """
        query = """
            SELECT 
                u.id, u.username, u.email, u.created_at,
                r.name as role_name,
                t.name as trainer_name,
                (SELECT COUNT(*) FROM search_history WHERE user_id = u.id) as total_searches,
                (SELECT COUNT(*) FROM team_pokemon tp 
                 JOIN trainers tr ON tp.trainer_id = tr.id 
                 WHERE tr.user_id = u.id) as total_pokemon
            FROM users u
            JOIN roles r ON u.role_id = r.id
            LEFT JOIN trainers t ON u.id = t.user_id
            ORDER BY u.created_at DESC
        """
        return self.db.fetch_all(query)

    def get_user_details(self, user_id: int) -> Optional[Dict]:
        """
        Obtiene detalles completos de un usuario específico
        """
        query = """
            SELECT 
                u.*, r.name as role_name,
                t.name as trainer_name, t.age as trainer_age, 
                t.region as trainer_region
            FROM users u
            JOIN roles r ON u.role_id = r.id
            LEFT JOIN trainers t ON u.id = t.user_id
            WHERE u.id = %s
        """
        return self.db.fetch_one(query, (user_id,))

    def update_user_role(self, user_id: int, new_role: str) -> bool:
        """
        Actualiza el rol de un usuario
        """
        try:
            query = """
                UPDATE users 
                SET role_id = (SELECT id FROM roles WHERE name = %s)
                WHERE id = %s
            """
            self.db.execute_query(query, (new_role, user_id))
            return True
        except Exception as e:
            print(f"Error updating user role: {str(e)}")
            return False

    def delete_user(self, user_id: int) -> bool:
        """
        Elimina un usuario y todos sus datos relacionados
        """
        try:
            # Iniciar transacción
            self.db.execute_query("START TRANSACTION")

            # Eliminar historial de búsquedas
            self.db.execute_query(
                "DELETE FROM search_history WHERE user_id = %s",
                (user_id,)
            )

            # Eliminar pokémon del equipo
            self.db.execute_query("""
                DELETE tp FROM team_pokemon tp
                JOIN trainers t ON tp.trainer_id = t.id
                WHERE t.user_id = %s
            """, (user_id,))

            # Eliminar entrenador
            self.db.execute_query(
                "DELETE FROM trainers WHERE user_id = %s",
                (user_id,)
            )

            # Eliminar usuario
            self.db.execute_query(
                "DELETE FROM users WHERE id = %s",
                (user_id,)
            )

            # Confirmar transacción
            self.db.execute_query("COMMIT")
            return True

        except Exception as e:
            # Revertir en caso de error
            self.db.execute_query("ROLLBACK")
            print(f"Error deleting user: {str(e)}")
            return False

    def get_system_stats(self) -> Dict:
        """
        Obtiene estadísticas generales del sistema
        """
        stats = {
            'total_users': 0,
            'total_searches': 0,
            'total_pokemon': 0,
            'users_by_role': {},
            'searches_last_7_days': [],
            'recent_registrations': [],
            'popular_pokemon': [],
            'popular_regions': []
        }

        try:
            # Total usuarios
            query = "SELECT COUNT(*) as total FROM users"
            result = self.db.fetch_one(query)
            stats['total_users'] = result['total']

            # Total búsquedas
            query = "SELECT COUNT(*) as total FROM search_history"
            result = self.db.fetch_one(query)
            stats['total_searches'] = result['total']

            # Total pokémon en equipos
            query = "SELECT COUNT(*) as total FROM team_pokemon"
            result = self.db.fetch_one(query)
            stats['total_pokemon'] = result['total']

            # Usuarios por rol
            query = """
                SELECT r.name, COUNT(*) as total
                FROM users u
                JOIN roles r ON u.role_id = r.id
                GROUP BY r.name
            """
            results = self.db.fetch_all(query)
            stats['users_by_role'] = {
                row['name']: row['total'] for row in results
            }

            # Búsquedas últimos 7 días
            query = """
                SELECT DATE(search_date) as date, COUNT(*) as total
                FROM search_history
                WHERE search_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
                GROUP BY DATE(search_date)
                ORDER BY date
            """
            stats['searches_last_7_days'] = self.db.fetch_all(query)

            # Registros recientes
            query = """
                SELECT id, username, created_at
                FROM users
                ORDER BY created_at DESC
                LIMIT 5
            """
            stats['recent_registrations'] = self.db.fetch_all(query)

            # Pokémon más populares
            query = """
                SELECT pokemon_name, COUNT(*) as total
                FROM team_pokemon
                GROUP BY pokemon_name
                ORDER BY total DESC
                LIMIT 5
            """
            stats['popular_pokemon'] = self.db.fetch_all(query)

            # Regiones más populares
            query = """
                SELECT region, COUNT(*) as total
                FROM trainers
                WHERE region IS NOT NULL
                GROUP BY region
                ORDER BY total DESC
                LIMIT 5
            """
            stats['popular_regions'] = self.db.fetch_all(query)

            return stats

        except Exception as e:
            print(f"Error getting system stats: {str(e)}")
            return stats

    def get_search_logs(self, limit: int = 100) -> List[Dict]:
        """
        Obtiene los registros de búsqueda más recientes
        """
        query = """
            SELECT 
                sh.id, sh.search_term, sh.search_date,
                u.username, u.email
            FROM search_history sh
            JOIN users u ON sh.user_id = u.id
            ORDER BY sh.search_date DESC
            LIMIT %s
        """
        return self.db.fetch_all(query, (limit,))

    def get_activity_logs(self, days: int = 7) -> List[Dict]:
        """
        Obtiene logs de actividad reciente
        """
        query = """
            (SELECT 
                'search' as type,
                u.username,
                sh.search_term as detail,
                sh.search_date as activity_date
            FROM search_history sh
            JOIN users u ON sh.user_id = u.id)
            UNION ALL
            (SELECT 
                'team_update' as type,
                u.username,
                CONCAT(
                    CASE 
                        WHEN tp.nickname IS NOT NULL 
                        THEN CONCAT(tp.pokemon_name, ' (', tp.nickname, ')')
                        ELSE tp.pokemon_name
                    END,
                    ' added to team'
                ) as detail,
                tp.joined_at as activity_date
            FROM team_pokemon tp
            JOIN trainers t ON tp.trainer_id = t.id
            JOIN users u ON t.user_id = u.id)
            ORDER BY activity_date DESC
            LIMIT 100
        """
        return self.db.fetch_all(query)