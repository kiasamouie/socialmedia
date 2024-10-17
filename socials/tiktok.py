import requests
import time
from utils.auth import OAuth2Handler

class TikTokAPI:
    def __init__(self, client_id, client_secret, account_id, auth_url, token_url, redirect_uri, token_file='instagram_token.json'):
        self.account_id = account_id
        self.oauth_handler = OAuth2Handler(client_id, client_secret, auth_url, token_url, redirect_uri, token_file)
        self.token_data = self.oauth_handler.get_or_refresh_token()
        self.access_token = self.token_data.get('access_token')
        self.base_url = ""