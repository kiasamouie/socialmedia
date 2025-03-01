from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from utils.auth import OAuth2Handler

class YouTubeAPI:
    def __init__(self, email: str, db_params: dict):
        self.oauth_handler = OAuth2Handler(email=email, db_params=db_params, service="youtube")

        # Fetch token (refresh if needed)
        self.token_data = self.oauth_handler.get_or_refresh_token(scope=['https://www.googleapis.com/auth/youtube.upload'])
        
        if not self.token_data:
            raise ValueError("Failed to retrieve valid OAuth token for YouTube.")

        self.access_token = self.token_data.get('access_token')
        self.refresh_token = self.token_data.get('refresh_token')
        self.service = self.get_authenticated_service()

    def get_authenticated_service(self):
        """Returns an authenticated YouTube API service instance."""
        credentials = Credentials(
            token=self.access_token,
            refresh_token=self.refresh_token,
            token_uri=self.oauth_handler.token_url,
            client_id=self.oauth_handler.client_id,
            client_secret=self.oauth_handler.client_secret
        )
        return build('youtube', 'v3', credentials=credentials)

    def upload_video(self, video_file: str, title: str, description: str, category_id: str, tags: list):
        """Uploads a video to YouTube and returns the video ID."""
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

        try:
            insert_request = self.service.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=MediaFileUpload(video_file, chunksize=-1, resumable=True)
            )
            response = insert_request.execute()
            return response.get('id')
        except Exception as e:
            print(f"Error uploading video: {e}")
            return None
