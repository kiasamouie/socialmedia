import os
import time
import requests
from utils.auth import OAuth2Handler

class InstagramAPI:
    def __init__(self, client_id, client_secret, account_id, auth_url, token_url, redirect_uri, token_file=os.path.join('tokens','instagram.json')):
        self.account_id = account_id
        self.oauth_handler = OAuth2Handler(client_id, client_secret, auth_url, token_url, redirect_uri, token_file)
        self.token_data = self.oauth_handler.get_or_refresh_token(scope=["instagram_basic","instagram_content_publish"])
        self.access_token = self.token_data.get('access_token')
        self.base_url = "https://graph.facebook.com/v18.0"

    def exchange_for_long_lived_token(self, short_lived_token):
        url = f"https://graph.facebook.com/v18.0/oauth/access_token"
        params = {
            'grant_type': 'fb_exchange_token',
            'client_id': self.oauth_handler.client_id,
            'client_secret': self.oauth_handler.client_secret,
            'redirect_uri': self.oauth_handler.redirect_uri,
            'fb_exchange_token': short_lived_token
        }

        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            token_data = response.json()
            token_data['expires_at'] = int(time.time()) + token_data.get('expires_in', 3600 * 60)
            self.oauth_handler.save_token(token_data)
            self.access_token = token_data.get('access_token')
            print("Long-lived token retrieved and saved.")
            return token_data['access_token']
        else:
            print("Failed to exchange for a long-lived token:", response.json())
            return None

    def upload_media(self, image_url, caption):
        upload_url = f"{self.base_url}/{self.account_id}/media"
        payload = {
            'image_url': image_url,
            'caption': caption,
            'access_token': self.access_token,
        }
        response = requests.post(upload_url, data=payload)

        # Debugging: print out full response details
        print("Upload Media Response Status Code:", response.status_code)
        print("Upload Media Response Content:", response.json())

        if response.status_code == 200:
            return response.json().get('id')
        else:
            print("Failed to upload media:", response.json())
            return None

    def publish_media(self, media_id):
        publish_url = f"{self.base_url}/{self.account_id}/media_publish"
        payload = {
            'creation_id': media_id,
            'access_token': self.access_token,
        }
        response = requests.post(publish_url, data=payload)

        # Debugging: print out full response details
        print("Publish Media Response Status Code:", response.status_code)
        print("Publish Media Response Content:", response.json())

        if response.status_code == 200:
            print("Media published successfully:", response.json())
            return True
        else:
            print("Failed to publish media:", response.json())
            return False

    def upload_and_publish(self, image_url, caption):
        media_id = self.upload_media(image_url, caption)
        if media_id:
            return self.publish_media(media_id)
        return False
