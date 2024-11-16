# Modelo de Usuario

# models/user_model.py
from config.database import DatabaseConnection
from services.encryption_service import EncryptionService
from typing import Optional, Dict

class UserModel:
    def __init__(self):
        self.db = DatabaseConnection()
        self.encryption = EncryptionService()

    def create_user(self, username: str, password: str, email: str) -> bool:
        """
        Creates a new user with encrypted password
        """
        try:
            hashed_password = self.encryption.hash_password(password)
            query = """
                INSERT INTO users (username, password, email, role_id)
                VALUES (%s, %s, %s, (SELECT id FROM roles WHERE name = 'user'))
            """
            self.db.execute_query(query, (username, hashed_password, email))
            return True
        except Exception as e:
            print(f"Error creating user: {str(e)}")
            return False

    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """
        Retrieves a user by username
        """
        query = """
            SELECT u.*, r.name as role_name 
            FROM users u 
            JOIN roles r ON u.role_id = r.id 
            WHERE username = %s
        """
        return self.db.fetch_one(query, (username,))

    def validate_login(self, username: str, password: str) -> Optional[Dict]:
        """
        Validates user login credentials
        """
        user = self.get_user_by_username(username)
        if user and self.encryption.check_password(password, user['password']):
            return user
        return None

    def username_exists(self, username: str) -> bool:
        """
        Checks if username already exists
        """
        query = "SELECT id FROM users WHERE username = %s"
        return bool(self.db.fetch_one(query, (username,)))

    def email_exists(self, email: str) -> bool:
        """
        Checks if email already exists
        """
        query = "SELECT id FROM users WHERE email = %s"
        return bool(self.db.fetch_one(query, (email,)))