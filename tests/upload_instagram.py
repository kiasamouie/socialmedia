import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from socials.instagram import InstagramAPI
load_dotenv()

client_id = os.getenv('INSTAGRAM_CLIENT_ID')
client_secret = os.getenv('INSTAGRAM_CLIENT_SECRET')
account_id = os.getenv('INSTAGRAM_ACCOUNT_ID')
auth_url = os.getenv('INSTAGRAM_AUTH_URL')
token_url = os.getenv('INSTAGRAM_TOKEN_URL')
redirect_uri = os.getenv('INSTAGRAM_REDIRECT_URI')

instagram_api = InstagramAPI(client_id, client_secret, account_id, auth_url, token_url, redirect_uri)

image_url = 'https://i1.sndcdn.com/avatars-Atwa0P5NDwgJpIcb-gkVkkg-t500x500.jpg'
video_url = r"https://samui-music.com/videos/output.mp4"
caption = 'Back on TheKiaDoe vibes'

success = instagram_api.upload_and_publish(video_url, caption, media_type="video")
# success = instagram_api.upload_and_publish(image_url, caption)

if success:
    print("Image uploaded and published successfully.")
else:
    print("Failed to upload and publish the image.")
