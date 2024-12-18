# Configuracion de MySQL

# config/database.py
import pymysql
from config.constants import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.connection = None
        return cls._instance

    def connect(self):
        if not self.connection:
            try:
                self.connection = pymysql.connect(
                    host=DB_HOST,
                    user=DB_USER,
                    password=DB_PASSWORD,
                    db=DB_NAME,
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor
                )
            except Exception as e:
                raise Exception(f"Error connecting to database: {str(e)}")
        return self.connection

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_query(self, query, params=None):
        conn = self.connect()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params or ())
                conn.commit()
                return cursor
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error executing query: {str(e)}")

    def fetch_one(self, query, params=None):
        conn = self.connect()
        with conn.cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchone()

    def fetch_all(self, query, params=None):
        conn = self.connect()
        with conn.cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchall()