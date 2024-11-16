# controllers/auth_controller.py
from models.user_model import UserModel
from services.logging_service import logger
from typing import Tuple, Dict, Optional
import re
import time

class AuthController:
    def __init__(self):
        self.user_model = UserModel()
        self._login_attempts = {}  # Para controlar intentos de login
        self.MAX_LOGIN_ATTEMPTS = 3
        self.LOCKOUT_TIME = 300  # 5 minutos en segundos

    def validate_password_strength(self, password: str) -> Tuple[bool, str]:
        """
        Valida que la contraseña cumpla con los requisitos de seguridad
        """
        try:
            if len(password) < 8:
                logger.log_security_event(
                    event_type="PASSWORD_VALIDATION_FAILURE",
                    details="Password length less than 8 characters"
                )
                return False, "La contraseña debe tener al menos 8 caracteres"
            
            if not re.search(r"[A-Z]", password):
                logger.log_security_event(
                    event_type="PASSWORD_VALIDATION_FAILURE",
                    details="Password missing uppercase letter"
                )
                return False, "La contraseña debe contener al menos una mayúscula"

            if not re.search(r"[a-z]", password):
                logger.log_security_event(
                    event_type="PASSWORD_VALIDATION_FAILURE",
                    details="Password missing lowercase letter"
                )
                return False, "La contraseña debe contener al menos una minúscula"

            if not re.search(r"\d", password):
                logger.log_security_event(
                    event_type="PASSWORD_VALIDATION_FAILURE",
                    details="Password missing number"
                )
                return False, "La contraseña debe contener al menos un número"
            
            if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
                logger.log_security_event(
                    event_type="PASSWORD_VALIDATION_FAILURE",
                    details="Password missing special character"
                )
                return False, "La contraseña debe contener al menos un carácter especial"
            
            logger.log_security_event(
                event_type="PASSWORD_VALIDATION_SUCCESS",
                details="Password meets all requirements"
            )
            return True, "Contraseña válida"

        except Exception as e:
            logger.log_error(
                f"Error validating password strength: {str(e)}",
                exc_info=True
            )
            return False, "Error al validar la contraseña"

    def validate_email(self, email: str) -> Tuple[bool, str]:
        """
        Valida el formato del email
        """
        try:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email):
                logger.log_security_event(
                    event_type="EMAIL_VALIDATION_FAILURE",
                    details=f"Invalid email format: {email}"
                )
                return False, "Formato de email inválido"
            return True, "Email válido"
        except Exception as e:
            logger.log_error(
                f"Error validating email: {str(e)}",
                exc_info=True
            )
            return False, "Error al validar el email"

    def check_login_attempts(self, username: str) -> Tuple[bool, str]:
        """
        Verifica si un usuario puede intentar iniciar sesión
        """
        current_time = time.time()
        if username in self._login_attempts:
            attempts, lockout_time = self._login_attempts[username]
            
            # Verificar si el tiempo de bloqueo ha pasado
            if lockout_time and current_time < lockout_time:
                remaining_time = int(lockout_time - current_time)
                logger.log_security_event(
                    event_type="LOGIN_ATTEMPT_BLOCKED",
                    details=f"User {username} is locked out for {remaining_time} seconds"
                )
                return False, f"Cuenta bloqueada. Intente en {remaining_time} segundos"
            
            # Resetear intentos si el tiempo de bloqueo ha pasado
            if lockout_time and current_time >= lockout_time:
                self._login_attempts[username] = (0, None)
        
        return True, ""

    def register_user(self, username: str, password: str, email: str) -> Tuple[bool, str]:
        """
        Registra un nuevo usuario
        """
        try:
            # Validar campos obligatorios
            if not all([username, password, email]):
                return False, "Todos los campos son obligatorios"

            # Validar formato de username
            if not re.match(r'^[a-zA-Z0-9_]{4,20}$', username):
                logger.log_security_event(
                    event_type="REGISTRATION_FAILURE",
                    details=f"Invalid username format: {username}"
                )
                return False, "Nombre de usuario inválido. Use entre 4 y 20 caracteres alfanuméricos"

            # Validar password
            is_valid_password, password_message = self.validate_password_strength(password)
            if not is_valid_password:
                return False, password_message

            # Validar email
            is_valid_email, email_message = self.validate_email(email)
            if not is_valid_email:
                return False, email_message

            # Verificar si el username existe
            if self.user_model.username_exists(username):
                logger.log_security_event(
                    event_type="REGISTRATION_FAILURE",
                    details=f"Username already exists: {username}"
                )
                return False, "El nombre de usuario ya está en uso"

            # Verificar si el email existe
            if self.user_model.email_exists(email):
                logger.log_security_event(
                    event_type="REGISTRATION_FAILURE",
                    details=f"Email already exists: {email}"
                )
                return False, "El email ya está registrado"

            # Crear usuario
            success = self.user_model.create_user(username, password, email)
            
            if success:
                logger.log_security_event(
                    event_type="REGISTRATION_SUCCESS",
                    details=f"New user registered: {username}"
                )
                return True, "Usuario registrado exitosamente"
            else:
                logger.log_security_event(
                    event_type="REGISTRATION_FAILURE",
                    details=f"Failed to create user: {username}"
                )
                return False, "Error al registrar el usuario"

        except Exception as e:
            logger.log_error(
                f"Error during user registration: {str(e)}",
                exc_info=True
            )
            return False, "Error en el proceso de registro"

    def login_user(self, username: str, password: str) -> Tuple[bool, str, Optional[Dict]]:
        """
        Autentica un usuario
        """
        try:
            # Verificar campos obligatorios
            if not all([username, password]):
                return False, "Todos los campos son obligatorios", None

            # Verificar intentos de login
            can_try, message = self.check_login_attempts(username)
            if not can_try:
                return False, message, None

            # Intentar login
            user = self.user_model.validate_login(username, password)
            
            if user:
                # Resetear intentos de login
                if username in self._login_attempts:
                    del self._login_attempts[username]

                logger.log_security_event(
                    event_type="LOGIN_SUCCESS",
                    user_id=user['id'],
                    details=f"User {username} logged in successfully"
                )
                return True, "Login exitoso", user
            else:
                # Registrar intento fallido
                attempts, _ = self._login_attempts.get(username, (0, None))
                attempts += 1
                
                if attempts >= self.MAX_LOGIN_ATTEMPTS:
                    lockout_time = time.time() + self.LOCKOUT_TIME
                    self._login_attempts[username] = (attempts, lockout_time)
                    
                    logger.log_security_event(
                        event_type="ACCOUNT_LOCKED",
                        details=f"Account locked for user {username} due to too many failed attempts"
                    )
                    return False, f"Demasiados intentos fallidos. Cuenta bloqueada por {self.LOCKOUT_TIME/60} minutos", None
                else:
                    self._login_attempts[username] = (attempts, None)
                    
                    logger.log_security_event(
                        event_type="LOGIN_FAILURE",
                        details=f"Failed login attempt {attempts} for user {username}"
                    )
                    return False, f"Credenciales inválidas. Intentos restantes: {self.MAX_LOGIN_ATTEMPTS - attempts}", None

        except Exception as e:
            logger.log_error(
                f"Error during login process: {str(e)}",
                exc_info=True
            )
            return False, "Error en el proceso de login", None

    def change_password(self, user_id: int, current_password: str, 
                       new_password: str) -> Tuple[bool, str]:
        """
        Cambia la contraseña de un usuario
        """
        try:
            # Validar nueva contraseña
            is_valid, message = self.validate_password_strength(new_password)
            if not is_valid:
                return False, message

            # Cambiar contraseña
            success = self.user_model.change_password(
                user_id, current_password, new_password
            )
            
            if success:
                logger.log_security_event(
                    event_type="PASSWORD_CHANGE_SUCCESS",
                    user_id=user_id,
                    details="Password changed successfully"
                )
                return True, "Contraseña actualizada exitosamente"
            else:
                logger.log_security_event(
                    event_type="PASSWORD_CHANGE_FAILURE",
                    user_id=user_id,
                    details="Failed to change password"
                )
                return False, "Error al cambiar la contraseña"

        except Exception as e:
            logger.log_error(
                f"Error during password change: {str(e)}",
                exc_info=True
            )
            return False, "Error al cambiar la contraseña"

    def logout_user(self, user_id: int) -> None:
        """
        Registra el logout de un usuario
        """
        try:
            logger.log_security_event(
                event_type="LOGOUT",
                user_id=user_id,
                details="User logged out successfully"
            )
        except Exception as e:
            logger.log_error(
                f"Error logging logout event: {str(e)}",
                exc_info=True
            )