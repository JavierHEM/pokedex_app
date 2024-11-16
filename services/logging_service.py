# services/logging_service.py
import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from config.config_handler import config

class LoggingService:
    _instance = None
    _loggers = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LoggingService, cls).__new__(cls)
            cls._instance._setup_logging()
        return cls._instance

    def _setup_logging(self):
        """
        Configura el sistema de logging base
        """
        # Crear directorio de logs si no existe
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Configurar formato base
        self.formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # Configurar diferentes tipos de logs
        self._setup_error_logging()
        self._setup_user_logging()
        self._setup_api_logging()
        self._setup_database_logging()
        self._setup_security_logging()

    def _setup_error_logging(self):
        """
        Configura el logger para errores generales
        """
        error_handler = RotatingFileHandler(
            'logs/error.log',
            maxBytes=5*1024*1024,  # 5MB
            backupCount=5
        )
        error_handler.setFormatter(self.formatter)
        error_handler.setLevel(logging.ERROR)

        logger = logging.getLogger('error')
        logger.setLevel(logging.ERROR)
        logger.addHandler(error_handler)
        self._loggers['error'] = logger

    def _setup_user_logging(self):
        """
        Configura el logger para actividades de usuario
        """
        user_handler = TimedRotatingFileHandler(
            'logs/user_activity.log',
            when='midnight',
            interval=1,
            backupCount=30
        )
        user_handler.setFormatter(self.formatter)
        user_handler.setLevel(logging.INFO)

        logger = logging.getLogger('user')
        logger.setLevel(logging.INFO)
        logger.addHandler(user_handler)
        self._loggers['user'] = logger

    def _setup_api_logging(self):
        """
        Configura el logger para llamadas a la API
        """
        api_handler = RotatingFileHandler(
            'logs/api.log',
            maxBytes=2*1024*1024,  # 2MB
            backupCount=3
        )
        api_handler.setFormatter(self.formatter)
        api_handler.setLevel(logging.INFO)

        logger = logging.getLogger('api')
        logger.setLevel(logging.INFO)
        logger.addHandler(api_handler)
        self._loggers['api'] = logger

    def _setup_database_logging(self):
        """
        Configura el logger para operaciones de base de datos
        """
        db_handler = RotatingFileHandler(
            'logs/database.log',
            maxBytes=3*1024*1024,  # 3MB
            backupCount=4
        )
        db_handler.setFormatter(self.formatter)
        db_handler.setLevel(logging.INFO)

        logger = logging.getLogger('database')
        logger.setLevel(logging.INFO)
        logger.addHandler(db_handler)
        self._loggers['database'] = logger

    def _setup_security_logging(self):
        """
        Configura el logger para eventos de seguridad
        """
        security_handler = RotatingFileHandler(
            'logs/security.log',
            maxBytes=1*1024*1024,  # 1MB
            backupCount=10
        )
        security_handler.setFormatter(self.formatter)
        security_handler.setLevel(logging.INFO)

        logger = logging.getLogger('security')
        logger.setLevel(logging.INFO)
        logger.addHandler(security_handler)
        self._loggers['security'] = logger

    def log_error(self, message: str, exc_info=None):
        """
        Registra un error
        """
        self._loggers['error'].error(message, exc_info=exc_info)

    def log_user_activity(self, user_id: int, action: str, details: str):
        """
        Registra actividad de usuario
        """
        message = f"User ID: {user_id} | Action: {action} | Details: {details}"
        self._loggers['user'].info(message)

    def log_api_call(self, endpoint: str, method: str, status_code: int, response_time: float):
        """
        Registra una llamada a la API
        """
        message = (f"Endpoint: {endpoint} | Method: {method} | "
                  f"Status: {status_code} | Time: {response_time:.2f}s")
        self._loggers['api'].info(message)

    def log_database_operation(self, operation: str, table: str, details: str):
        """
        Registra una operación de base de datos
        """
        message = f"Operation: {operation} | Table: {table} | Details: {details}"
        self._loggers['database'].info(message)

    def log_security_event(self, event_type: str, user_id: int = None, details: str = None):
        """
        Registra un evento de seguridad
        """
        message = f"Type: {event_type}"
        if user_id:
            message += f" | User ID: {user_id}"
        if details:
            message += f" | Details: {details}"
        self._loggers['security'].info(message)

# Crear instancia global del servicio
logger = LoggingService()