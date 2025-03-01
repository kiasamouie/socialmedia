import psycopg2
import json
from psycopg2.extras import RealDictCursor

class DatabaseHandler:
    def __init__(self, db_name, host, user, password, port):
        self.conn = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host=host,
            port=port,
            cursor_factory=RealDictCursor
        )
        self.cursor = self.conn.cursor()

    def load_user_credentials(self, email: str):
        """Fetch OAuth credentials & account_id using email."""
        query = """
        SELECT * FROM private.users WHERE email = %s
        """
        self.cursor.execute(query, (email,))
        result = self.cursor.fetchone()
        return result if result else None  # Returns full user credentials

    def save_token(self, service: str, user_id: int, token_data: dict):
        """Stores OAuth token data as JSON for a given user_id."""
        query = """
        INSERT INTO private.tokens (service, user_id, token_data)
        VALUES (%s, %s, %s)
        ON CONFLICT (service, user_id) DO UPDATE 
        SET token_data = EXCLUDED.token_data
        """
        self.cursor.execute(query, (service, user_id, json.dumps(token_data)))
        self.conn.commit()

    def load_token(self, service: str, user_id: int):
        """Retrieves OAuth token data for a service and user_id."""
        query = "SELECT token_data FROM private.tokens WHERE service = %s AND user_id = %s"
        self.cursor.execute(query, (service, user_id))
        result = self.cursor.fetchone()
        
        return result['token_data'] if result else None  # ✅ No need for json.loads()

    def close(self):
        self.cursor.close()
        self.conn.close()
