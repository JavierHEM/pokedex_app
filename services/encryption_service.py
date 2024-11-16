# Servicio de Encriptacion

# services/encryption_service.py
import bcrypt

class EncryptionService:
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Encrypts a password using bcrypt
        """
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @staticmethod
    def check_password(password: str, hashed_password: str) -> bool:
        """
        Verifies if a password matches its hash
        """
        return bcrypt.checkpw(
            password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )