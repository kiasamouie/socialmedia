import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor

class DatabaseHandler:
    def __init__(self, db_type='sqlite', db_name='socialmedia.db', host=None, user=None, password=None, port=None):
        self.db_type = db_type
        if db_type == 'sqlite':
            self.conn = sqlite3.connect(db_name)
        elif db_type == 'postgres':
            self.conn = psycopg2.connect(
                dbname=db_name, 
                user=user, 
                password=password, 
                host=host, 
                port=port,
                cursor_factory=RealDictCursor
            )
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS tokens (
            service TEXT PRIMARY KEY,
            access_token TEXT,
            refresh_token TEXT,
            expires_at INTEGER
        )
        """
        self.cursor.execute(query)
        self.conn.commit()

    def save_token(self, service, access_token, refresh_token, expires_at):
        query = """
        INSERT OR REPLACE INTO tokens (service, access_token, refresh_token, expires_at)
        VALUES (?, ?, ?, ?)""" if self.db_type == 'sqlite' else """
        INSERT INTO tokens (service, access_token, refresh_token, expires_at)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (service) DO UPDATE 
        SET access_token = EXCLUDED.access_token, 
            refresh_token = EXCLUDED.refresh_token, 
            expires_at = EXCLUDED.expires_at
        """
        self.cursor.execute(query, (service, access_token, refresh_token, expires_at))
        self.conn.commit()

    def load_token(self, service):
        query = "SELECT * FROM tokens WHERE service = ?" if self.db_type == 'sqlite' else "SELECT * FROM tokens WHERE service = %s"
        self.cursor.execute(query, (service,))
        return self.cursor.fetchone()

    def close(self):
        self.cursor.close()
        self.conn.close()
