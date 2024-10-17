import os
import json
import requests
import time

class OAuth2Handler:
    def __init__(self, client_id, client_secret, auth_url, token_url, redirect_uri, token_file):
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_url = auth_url
        self.token_url = token_url
        self.redirect_uri = redirect_uri
        self.token_file = token_file
        self.access_token = None

    def load_token(self):
        print(os.path.exists(self.token_file))
        if os.path.exists(self.token_file):
            with open(self.token_file, 'r') as f:
                return json.load(f)
        return None

    def save_token(self, token_data):
        with open(self.token_file, 'w') as f:
            json.dump(token_data, f)

    def is_token_expired(self, token_data):
        return token_data.get('expires_at') < int(time.time())

    def refresh_access_token(self, refresh_token_url, refresh_token):
        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token'
        }
        response = requests.post(refresh_token_url, data=payload)
        if response.status_code == 200:
            token_data = response.json()
            token_data['expires_at'] = int(time.time()) + token_data.get('expires_in', 3600)
            self.save_token(token_data)
            return token_data
        return None

    def fetch_access_token(self, authorization_code):
        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri,
            'code': authorization_code,
            'grant_type': 'authorization_code'
        }
        response = requests.post(self.token_url, data=payload)
        if response.status_code == 200:
            token_data = response.json()
            token_data['expires_at'] = int(time.time()) + token_data.get('expires_in', 3600)
            self.save_token(token_data)
            return token_data
        return None

    def get_authorization_url(self, scope):
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'scope': ' '.join(scope)
        }
        return f"{self.auth_url}?{requests.compat.urlencode(params)}"

    def get_or_refresh_token(self, scope):
        token_data = self.load_token()
        if token_data:
            if self.is_token_expired(token_data):
                return self.refresh_access_token(f"{self.token_url}/refresh", token_data['refresh_token'])
            return token_data
        return self.authorize(scope)

    def authorize(self, scope):
        auth_url = self.get_authorization_url(scope=scope)
        print(f"Go to this URL to authorize the app: {auth_url}")
        authorization_code = input("Enter the authorization code from the URL: ").strip()
        return self.fetch_access_token(authorization_code)
