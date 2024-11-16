# Control de Autenticacion

# controllers/auth_controller.py
import re
from models.user_model import UserModel

class AuthController:
    def __init__(self):
        self.user_model = UserModel()

    def validate_password_strength(self, password: str) -> tuple[bool, str]:
        """
        Validates password meets requirements:
        - At least 8 characters
        - At least one special character
        """
        if len(password) < 8:
            return False, "La contraseña debe tener al menos 8 caracteres"
        
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False, "La contraseña debe contener al menos un carácter especial"
        
        return True, "Contraseña válida"

    def validate_email(self, email: str) -> tuple[bool, str]:
        """
        Validates email format
        """
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return False, "Formato de email inválido"
        return True, "Email válido"

    def register_user(self, username: str, password: str, email: str) -> tuple[bool, str]:
        """
        Registers a new user after validation
        """
        # Validate input fields
        if not all([username, password, email]):
            return False, "Todos los campos son obligatorios"

        # Validate password strength
        is_valid_password, password_message = self.validate_password_strength(password)
        if not is_valid_password:
            return False, password_message

        # Validate email format
        is_valid_email, email_message = self.validate_email(email)
        if not is_valid_email:
            return False, email_message

        # Check if username exists
        if self.user_model.username_exists(username):
            return False, "El nombre de usuario ya está en uso"

        # Check if email exists
        if self.user_model.email_exists(email):
            return False, "El email ya está registrado"

        # Create user
        if self.user_model.create_user(username, password, email):
            return True, "Usuario registrado exitosamente"
        return False, "Error al registrar el usuario"

    def login_user(self, username: str, password: str) -> tuple[bool, str, dict]:
        """
        Authenticates a user
        """
        if not all([username, password]):
            return False, "Todos los campos son obligatorios", {}

        user = self.user_model.validate_login(username, password)
        if user:
            return True, "Login exitoso", user
        return False, "Credenciales inválidas", {}