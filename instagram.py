import requests
from base import OAuth2Handler

class InstagramAPI:
    def __init__(self, client_id, client_secret, account_id, auth_url, token_url, redirect_uri, token_file='instagram_token.json'):
        self.account_id = account_id
        self.oauth_handler = OAuth2Handler(client_id, client_secret, auth_url, token_url, redirect_uri, token_file)
        self.token_data = self.oauth_handler.get_or_refresh_token()
        self.access_token = self.token_data.get('access_token')
        self.base_url = "https://graph.facebook.com/v18.0"

    def upload_media(self, image_url, caption):
        upload_url = f"{self.base_url}/{self.account_id}/media"
        payload = {
            'image_url': image_url,
            'caption': caption,
            'access_token': self.access_token,
        }
        response = requests.post(upload_url, data=payload)
        if response.status_code == 200:
            return response.json().get('id')
        return None

    def publish_media(self, media_id):
        publish_url = f"{self.base_url}/{self.account_id}/media_publish"
        payload = {
            'creation_id': media_id,
            'access_token': self.access_token,
        }
        response = requests.post(publish_url, data=payload)
        return response.status_code == 200

    def upload_and_publish(self, image_url, caption):
        media_id = self.upload_media(image_url, caption)
        if media_id:
            return self.publish_media(media_id)
        return False