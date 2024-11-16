# Control de Administracion
# controllers/admin_controller.py
from models.admin_model import AdminModel
from typing import List, Dict, Tuple
import logging

class AdminController:
    def __init__(self):
        self.admin_model = AdminModel()
        self.logger = logging.getLogger(__name__)

    def get_users_list(self) -> List[Dict]:
        """
        Obtiene la lista de usuarios para el panel de administración
        """
        try:
            return self.admin_model.get_all_users()
        except Exception as e:
            self.logger.error(f"Error getting users list: {str(e)}")
            return []

    def get_user_details(self, user_id: int) -> Tuple[bool, Dict]:
        """
        Obtiene los detalles completos de un usuario
        """
        try:
            details = self.admin_model.get_user_details(user_id)
            if details:
                return True, details
            return False, {"error": "Usuario no encontrado"}
        except Exception as e:
            self.logger.error(f"Error getting user details: {str(e)}")
            return False, {"error": str(e)}

    def update_user_role(self, user_id: int, new_role: str) -> Tuple[bool, str]:
        """
        Actualiza el rol de un usuario
        """
        try:
            if new_role not in ['user', 'admin']:
                return False, "Rol inválido"

            success = self.admin_model.update_user_role(user_id, new_role)
            if success:
                return True, "Rol actualizado exitosamente"
            return False, "Error al actualizar el rol"
        except Exception as e:
            self.logger.error(f"Error updating user role: {str(e)}")
            return False, str(e)

    def delete_user(self, user_id: int) -> Tuple[bool, str]:
        """
        Elimina un usuario y sus datos relacionados
        """
        try:
            success = self.admin_model.delete_user(user_id)
            if success:
                return True, "Usuario eliminado exitosamente"
            return False, "Error al eliminar el usuario"
        except Exception as e:
            self.logger.error(f"Error deleting user: {str(e)}")
            return False, str(e)

    def get_dashboard_stats(self) -> Dict:
        """
        Obtiene estadísticas para el dashboard de administración
        """
        try:
            return self.admin_model.get_system_stats()
        except Exception as e:
            self.logger.error(f"Error getting dashboard stats: {str(e)}")
            return {}

    def get_recent_activity(self) -> List[Dict]:
        """
        Obtiene actividad reciente del sistema
        """
        try:
            return self.admin_model.get_activity_logs()
        except Exception as e:
            self.logger.error(f"Error getting recent activity: {str(e)}")
            return []

    def get_search_history(self, limit: int = 100) -> List[Dict]:
        """
        Obtiene historial de búsquedas
        """
        try:
            return self.admin_model.get_search_logs(limit)
        except Exception as e:
            self.logger.error(f"Error getting search history: {str(e)}")
            return []