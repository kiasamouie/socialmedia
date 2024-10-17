import os
from instagram import InstagramAPI
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv('INSTAGRAM_CLIENT_ID')
client_secret = os.getenv('INSTAGRAM_CLIENT_SECRET')
account_id = os.getenv('INSTAGRAM_ACCOUNT_ID')
auth_url = os.getenv('INSTAGRAM_AUTH_URL')
token_url = os.getenv('INSTAGRAM_TOKEN_URL')
redirect_uri = os.getenv('INSTAGRAM_REDIRECT_URI')

instagram_api = InstagramAPI(client_id, client_secret, account_id, auth_url, token_url, redirect_uri)

image_url = 'https://i1.sndcdn.com/avatars-Atwa0P5NDwgJpIcb-gkVkkg-t500x500.jpg'
caption = 'Automated Post'
success = instagram_api.upload_and_publish(image_url, caption)

if success:
    print("Image uploaded and published successfully.")
else:
    print("Failed to upload and publish the image.")
