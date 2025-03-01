import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from socials.tiktok import TikTokAPI
load_dotenv()

client_id = os.getenv('TIKTOK_CLIENT_ID')
client_secret = os.getenv('TIKTOK_CLIENT_SECRET')
account_id = os.getenv('TIKTOK_ACCOUNT_ID')
auth_url = os.getenv('TIKTOK_AUTH_URL')
token_url = os.getenv('TIKTOK_TOKEN_URL')
redirect_uri = os.getenv('TIKTOK_REDIRECT_URI')

# tiktok_api = TikTokAPI(client_id, client_secret, account_id, auth_url, token_url, redirect_uri)

video_file = r"D:\Videos\kickingitback.mp4"
description = 'This is a test video uploaded via TikTok API.'

# if tiktok_api.upload_and_publish(video_file, description):
#     print("Video uploaded and published successfully.")
# else:
#     print("Failed to upload or publish the video.")

print("This is part of a pip package with tiktok api integrated!")
print("The goal is to autonomously upload to Tiktok, Instagram, YouTube")
print("")
print("Uploaded video to Tiktok!!")