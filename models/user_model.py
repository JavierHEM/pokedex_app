# models/user_model.py
from config.database import DatabaseConnection
from services.encryption_service import EncryptionService
from typing import Optional, Dict, Tuple

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

    def get_user_profile(self, user_id: int) -> Optional[Dict]:
        """
        Obtiene el perfil completo del usuario incluyendo datos del entrenador
        """
        query = """
            SELECT u.username, u.email, u.created_at,
                   t.name as trainer_name, t.age as trainer_age, 
                   t.region as trainer_region
            FROM users u
            LEFT JOIN trainers t ON u.id = t.user_id
            WHERE u.id = %s
        """
        return self.db.fetch_one(query, (user_id,))

    def update_user_profile(self, user_id: int, data: Dict) -> Tuple[bool, str]:
        """
        Actualiza la información del perfil del usuario
        """
        try:
            # Verificar si el email ya existe
            if 'email' in data:
                check_query = "SELECT id FROM users WHERE email = %s AND id != %s"
                if self.db.fetch_one(check_query, (data['email'], user_id)):
                    return False, "El email ya está en uso"

            # Actualizar usuario
            user_updates = []
            user_params = []
            if 'email' in data:
                user_updates.append("email = %s")
                user_params.append(data['email'])
            
            if 'password' in data and data['password']:
                user_updates.append("password = %s")
                user_params.append(self.encryption.hash_password(data['password']))

            if user_updates:
                user_params.append(user_id)
                user_query = f"""
                    UPDATE users 
                    SET {', '.join(user_updates)}
                    WHERE id = %s
                """
                self.db.execute_query(user_query, tuple(user_params))

            # Actualizar entrenador
            trainer_exists = self.db.fetch_one(
                "SELECT id FROM trainers WHERE user_id = %s", 
                (user_id,)
            )

            trainer_data = {
                'name': data.get('trainer_name'),
                'age': data.get('trainer_age'),
                'region': data.get('trainer_region')
            }

            if any(v is not None for v in trainer_data.values()):
                if trainer_exists:
                    # Actualizar entrenador existente
                    trainer_updates = [
                        f"{k} = %s" for k, v in trainer_data.items() 
                        if v is not None
                    ]
                    trainer_params = [
                        v for v in trainer_data.values() 
                        if v is not None
                    ]
                    trainer_params.append(user_id)

                    trainer_query = f"""
                        UPDATE trainers 
                        SET {', '.join(trainer_updates)}
                        WHERE user_id = %s
                    """
                else:
                    # Crear nuevo entrenador
                    trainer_fields = [
                        k for k, v in trainer_data.items() 
                        if v is not None
                    ]
                    trainer_values = [
                        v for v in trainer_data.values() 
                        if v is not None
                    ]
                    trainer_values.append(user_id)

                    trainer_query = f"""
                        INSERT INTO trainers 
                        (user_id, {', '.join(trainer_fields)})
                        VALUES (%s, {', '.join(['%s'] * len(trainer_fields))})
                    """

                self.db.execute_query(trainer_query, tuple(trainer_params))

            return True, "Perfil actualizado exitosamente"

        except Exception as e:
            print(f"Error updating profile: {str(e)}")
            return False, "Error al actualizar el perfil"

    def change_password(self, user_id: int, current_password: str, 
                       new_password: str) -> Tuple[bool, str]:
        """
        Cambia la contraseña del usuario
        """
        try:
            # Verificar contraseña actual
            user = self.db.fetch_one(
                "SELECT password FROM users WHERE id = %s",
                (user_id,)
            )
            
            if not user or not self.encryption.check_password(
                current_password, user['password']
            ):
                return False, "Contraseña actual incorrecta"

            # Actualizar contraseña
            hashed_password = self.encryption.hash_password(new_password)
            self.db.execute_query(
                "UPDATE users SET password = %s WHERE id = %s",
                (hashed_password, user_id)
            )

            return True, "Contraseña actualizada exitosamente"

        except Exception as e:
            print(f"Error changing password: {str(e)}")
            return False, "Error al cambiar la contraseña"

    def get_user_stats(self, user_id: int) -> Dict:
        """
        Obtiene estadísticas del usuario
        """
        try:
            stats = {
                'total_searches': 0,
                'total_pokemon': 0,
                'join_date': None,
                'last_search': None
            }

            # Obtener fecha de registro
            user_query = """
                SELECT created_at 
                FROM users 
                WHERE id = %s
            """
            user_data = self.db.fetch_one(user_query, (user_id,))
            if user_data:
                stats['join_date'] = user_data['created_at']

            # Obtener total de búsquedas y última búsqueda
            search_query = """
                SELECT COUNT(*) as total,
                       MAX(search_date) as last_search
                FROM search_history
                WHERE user_id = %s
            """
            search_data = self.db.fetch_one(search_query, (user_id,))
            if search_data:
                stats['total_searches'] = search_data['total']
                stats['last_search'] = search_data['last_search']

            # Obtener total de pokémon en el equipo
            pokemon_query = """
                SELECT COUNT(*) as total
                FROM team_pokemon tp
                JOIN trainers t ON tp.trainer_id = t.id
                WHERE t.user_id = %s
            """
            pokemon_data = self.db.fetch_one(pokemon_query, (user_id,))
            if pokemon_data:
                stats['total_pokemon'] = pokemon_data['total']

            return stats

        except Exception as e:
            print(f"Error getting user stats: {str(e)}")
            return {}