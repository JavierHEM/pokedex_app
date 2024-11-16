# config/config_handler.py
import configparser
import os

class ConfigHandler:
    _instance = None
    _config = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigHandler, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        """
        Carga la configuración desde el archivo config.ini
        """
        self._config = configparser.ConfigParser()
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config.ini')
        
        if not os.path.exists(config_path):
            raise FileNotFoundError(
                "El archivo config.ini no se encuentra. "
                "Por favor, crea el archivo en el directorio raíz del proyecto."
            )
        
        self._config.read(config_path)

    @property
    def database(self):
        """
        Retorna la configuración de la base de datos
        """
        return {
            'host': self._config.get('DATABASE', 'host'),
            'user': self._config.get('DATABASE', 'user'),
            'password': self._config.get('DATABASE', 'password'),
            'database': self._config.get('DATABASE', 'database'),
            'port': self._config.getint('DATABASE', 'port')
        }

    @property
    def api(self):
        """
        Retorna la configuración de la API
        """
        return {
            'base_url': self._config.get('API', 'base_url'),
            'timeout': self._config.getint('API', 'timeout'),
            'max_retries': self._config.getint('API', 'max_retries')
        }

    @property
    def app(self):
        """
        Retorna la configuración general de la aplicación
        """
        return {
            'title': self._config.get('APP', 'title'),
            'theme': self._config.get('APP', 'theme'),
            'language': self._config.get('APP', 'language'),
            'max_team_size': self._config.getint('APP', 'max_team_size'),
            'debug': self._config.getboolean('APP', 'debug')
        }

    @property
    def logging(self):
        """
        Retorna la configuración de logging
        """
        return {
            'level': self._config.get('LOGGING', 'level'),
            'file': self._config.get('LOGGING', 'file'),
            'format': self._config.get('LOGGING', 'format')
        }

    @property
    def security(self):
        """
        Retorna la configuración de seguridad
        """
        return {
            'min_password_length': self._config.getint('SECURITY', 'min_password_length'),
            'require_special_char': self._config.getboolean('SECURITY', 'require_special_char'),
            'session_timeout': self._config.getint('SECURITY', 'session_timeout'),
            'max_login_attempts': self._config.getint('SECURITY', 'max_login_attempts')
        }

# Para usar en otros archivos:
config = ConfigHandler()