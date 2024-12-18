# config/constants.py

from config.config_handler import config

# Database constants
DB_HOST = config.database['host']
DB_USER = config.database['user']
DB_PASSWORD = config.database['password']
DB_NAME = config.database['database']
DB_PORT = config.database['port']

# API constants
API_BASE_URL = config.api['base_url']
API_TIMEOUT = config.api['timeout']
API_MAX_RETRIES = config.api['max_retries']

# App constants
APP_TITLE = config.app['title']
APP_THEME = config.app['theme']
APP_LANGUAGE = config.app['language']
MAX_TEAM_SIZE = config.app['max_team_size']
DEBUG_MODE = config.app['debug']

# Security constants
MIN_PASSWORD_LENGTH = config.security['min_password_length']
REQUIRE_SPECIAL_CHAR = config.security['require_special_char']
SESSION_TIMEOUT = config.security['session_timeout']
MAX_LOGIN_ATTEMPTS = config.security['max_login_attempts']

# Other constants
SUPPORTED_LANGUAGES = ['es', 'en']
POKEMON_TYPES = [
    'normal', 'fire', 'water', 'electric', 'grass', 'ice',
    'fighting', 'poison', 'ground', 'flying', 'psychic', 'bug',
    'rock', 'ghost', 'dragon', 'dark', 'steel', 'fairy'
]