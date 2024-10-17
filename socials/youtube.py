import os
import requests
import time
from utils.auth import OAuth2Handler
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

class YouTubeAPI:
    def __init__(self, client_id, client_secret, account_id, auth_url, token_url, redirect_uri, token_file=os.path.join('tokens','youtube.json')):
        self.account_id = account_id
        self.oauth_handler = OAuth2Handler(client_id, client_secret, auth_url, token_url, redirect_uri, token_file)
        self.token_data = self.oauth_handler.get_or_refresh_token(scope=['https://www.googleapis.com/auth/youtube.upload'])
        self.access_token = self.token_data.get('access_token')
        self.refresh_token = self.token_data.get('refresh_token')
        self.base_url = "https://www.googleapis.com/youtube/v3"
        self.service = self.get_authenticated_service()

    def get_authenticated_service(self):
        credentials = Credentials(
            token=self.access_token,
            refresh_token=self.refresh_token,
            token_uri=self.oauth_handler.token_url,
            client_id=self.oauth_handler.client_id,
            client_secret=self.oauth_handler.client_secret
        )
        return build('youtube', 'v3', credentials=credentials)

    def upload_video(self, video_file, title, description, category_id, tags):
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': category_id
            },
            'status': {
                'privacyStatus': 'public',
                'selfDeclaredMadeForKids': False
            }
        }

        insert_request = self.service.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=MediaFileUpload(video_file, chunksize=-1, resumable=True)
        )
        response = insert_request.execute()
        return response.get('id')
