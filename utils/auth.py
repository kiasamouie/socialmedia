import inspect
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
        self.platform = self.detect_platform()
        self.access_token = None

    def load_token(self):
        if os.path.exists(self.token_file):
            with open(self.token_file, 'r') as f:
                return json.load(f)
        return None

    def save_token(self, token_data):
        with open(self.token_file, 'w') as f:
            json.dump(token_data, f)

    def is_token_expired(self, token_data):
        return token_data.get('expires_at') < int(time.time())
    
    def detect_platform(self):
        stack = inspect.stack()
        caller = stack[2].frame.f_locals.get('self', None).__class__.__name__.lower()
        for platform in [os.path.splitext(filename)[0] for filename in os.listdir('socials') if filename.endswith('.py') and filename != '__init__.py']:
            if platform in caller:
                return platform
        return 'unknown'

    def handle_access_token(self, authorization_code=None, refresh_token=None, is_refresh=False):
        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }

        if is_refresh:
            if self.platform == 'instagram':
                # Instagram long-lived token refresh
                refresh_url = f"https://graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token&access_token={refresh_token}"
                response = requests.get(refresh_url)
            else:
                # Standard refresh flow (TikTok, YouTube)
                if not refresh_token:
                    print("Error: Refresh token is missing!")
                    return None
                payload['refresh_token'] = refresh_token
                payload['grant_type'] = 'refresh_token'
                response = requests.post(self.token_url, data=payload)
        else:
            # Fetching new access token
            payload['code'] = authorization_code
            payload['redirect_uri'] = self.redirect_uri
            payload['grant_type'] = 'authorization_code'
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

    def get_or_refresh_token(self, scope):
        token_data = self.load_token()
        if token_data:
            if self.is_token_expired(token_data):
                print("Token expired. Attempting to refresh...")
                refresh_token = token_data.get('refresh_token', token_data.get('access_token'))
                return self.handle_access_token(refresh_token=refresh_token, is_refresh=True)
            return token_data
        return self.authorize(scope)

    def get_authorization_url(self, scope):
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'scope': ' '.join(scope),
        }
        if self.platform != 'instagram':
            params['access_type'] = 'offline'  # Request refresh token for non-Instagram platforms
            params['prompt'] = 'consent'
        return f"{self.auth_url}?{requests.compat.urlencode(params)}"

    def authorize(self, scope):
        auth_url = self.get_authorization_url(scope=scope)
        print(f"Go to this URL to authorize the app: {auth_url}")
        authorization_code = input("Enter the authorization code from the URL: ").strip()
        return self.handle_access_token(authorization_code=authorization_code)
