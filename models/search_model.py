# Modelo de Busqueda
# models/search_model.py
from config.database import DatabaseConnection
from typing import List, Dict

class SearchModel:
    def __init__(self):
        self.db = DatabaseConnection()

    def add_search(self, user_id: int, search_term: str) -> bool:
        """
        Registra una nueva búsqueda en el historial
        """
        try:
            query = """
                INSERT INTO search_history (user_id, search_term)
                VALUES (%s, %s)
            """
            self.db.execute_query(query, (user_id, search_term))
            return True
        except Exception as e:
            print(f"Error al registrar búsqueda: {str(e)}")
            return False

    def get_user_searches(self, user_id: int, limit: int = 10) -> List[Dict]:
        """
        Obtiene las búsquedas recientes de un usuario
        """
        query = """
            SELECT search_term, search_date
            FROM search_history
            WHERE user_id = %s
            ORDER BY search_date DESC
            LIMIT %s
        """
        return self.db.fetch_all(query, (user_id, limit))

    def get_popular_searches(self, limit: int = 10) -> List[Dict]:
        """
        Obtiene las búsquedas más populares
        """
        query = """
            SELECT search_term, COUNT(*) as count
            FROM search_history
            GROUP BY search_term
            ORDER BY count DESC
            LIMIT %s
        """
        return self.db.fetch_all(query, (limit,))