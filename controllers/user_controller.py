# Control de Usuarios

# controllers/profile_controller.py
from models.user_model import UserModel
import re
from typing import Dict, Tuple

class ProfileController:
    def __init__(self):
        self.user_model = UserModel()

    def get_user_profile(self, user_id: int) -> Dict:
        """
        Obtiene el perfil del usuario
        """
        return self.user_model.get_user_profile(user_id)

    def validate_profile_data(self, data: Dict) -> Tuple[bool, str]:
        """
        Valida los datos del perfil antes de actualizar
        """
        # Validar email
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, data.get('email', '')):
            return False, "Formato de email inválido"

        # Validar nombre del entrenador
        trainer_name = data.get('trainer_name', '')
        if not trainer_name or len(trainer_name) < 3:
            return False, "El nombre del entrenador debe tener al menos 3 caracteres"

        # Validar edad
        try:
            age = int(data.get('age', 0))
            if not (8 <= age <= 100):
                return False, "La edad debe estar entre 8 y 100 años"
        except ValueError:
            return False, "La edad debe ser un número válido"

        # Validar región
        region = data.get('region', '')
        if not region or len(region) < 2:
            return False, "Debe especificar una región válida"

        return True, "Datos válidos"

    def update_profile(self, user_id: int, data: Dict) -> Tuple[bool, str]:
        """
        Actualiza el perfil del usuario
        """
        # Validar datos
        is_valid, message = self.validate_profile_data(data)
        if not is_valid:
            return False, message

        # Actualizar perfil
        return self.user_model.update_user_profile(user_id, data)

    def validate_password(self, password: str) -> Tuple[bool, str]:
        """
        Valida los requisitos de la contraseña
        """
        if len(password) < 8:
            return False, "La contraseña debe tener al menos 8 caracteres"

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False, "La contraseña debe contener al menos un carácter especial"

        return True, "Contraseña válida"

    def change_password(self, user_id: int, current_password: str, new_password: str) -> Tuple[bool, str]:
        """
        Cambia la contraseña del usuario
        """
        # Validar nueva contraseña
        is_valid, message = self.validate_password(new_password)
        if not is_valid:
            return False, message

        return self.user_model.change_password(user_id, current_password, new_password)

    def delete_account(self, user_id: int, password: str) -> Tuple[bool, str]:
        """
        Elimina la cuenta del usuario
        """
        return self.user_model.delete_account(user_id, password)