import requests
import time
from typing import Optional, Dict
from utils.database import DatabaseHandler

class OAuth2Handler:
    def __init__(self, email: str, db_params: dict, service: str):
        self.db = DatabaseHandler(**db_params)
        self.user_data = self.db.load_user_credentials(email)

        if not self.user_data:
            raise ValueError(f"User with email '{email}' not found in database.")
        self.user_id = self.user_data["id"]
        self.account_id = self.user_data["account_id"]
        self.client_id = self.user_data["client_id"]
        self.client_secret = self.user_data["client_secret"]
        self.auth_url = self.user_data["auth_url"]
        self.token_url = self.user_data["token_url"]
        self.redirect_uri = self.user_data["redirect_uri"]
        self.service = service

    def load_token(self) -> Optional[Dict]:
        return self.db.load_token(self.service, self.user_id)

    def save_token(self, token_data: Dict) -> None:
        self.db.save_token(self.service, self.user_id, token_data)

    def handle_access_token(self, authorization_code: Optional[str] = None, refresh_token: Optional[str] = None, is_refresh: bool = False) -> Optional[Dict]:
        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }

        if is_refresh:
            if not refresh_token:
                print("Error: Refresh token is missing!")
                return None
            payload.update({'refresh_token': refresh_token, 'grant_type': 'refresh_token'})
            response = requests.post(self.token_url, data=payload)
        else:
            payload.update({'code': authorization_code, 'redirect_uri': self.redirect_uri, 'grant_type': 'authorization_code'})
            response = requests.post(self.token_url, data=payload)

        if response.status_code == 200:
            token_data = response.json()
            token_data['expires_at'] = int(time.time()) + token_data.get('expires_in', 3600)
            self.save_token(token_data)
            return token_data
        else:
            print(f"Failed to handle token. Status code: {response.status_code}")
            print(f"Response content: {response.content}")
            return None

    def get_or_refresh_token(self, scope: list) -> Optional[Dict]:
        token_data = self.load_token()
        if token_data and token_data.get('expires_at', 0) < int(time.time()):
            print("Token expired. Attempting to refresh...")
            refresh_token = token_data.get('refresh_token', token_data.get('access_token'))
            return self.handle_access_token(refresh_token=refresh_token, is_refresh=True)
        return token_data
