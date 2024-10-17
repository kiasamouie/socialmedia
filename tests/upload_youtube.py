import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from socials.youtube import YouTubeAPI
load_dotenv()

client_id = os.getenv('YOUTUBE_CLIENT_ID')
client_secret = os.getenv('YOUTUBE_CLIENT_SECRET')
account_id = os.getenv('YOUTUBE_ACCOUNT_ID')
auth_url = os.getenv('YOUTUBE_AUTH_URL')
token_url = os.getenv('YOUTUBE_TOKEN_URL')
redirect_uri = os.getenv('YOUTUBE_REDIRECT_URI')

youtube_api = YouTubeAPI(client_id, client_secret, account_id, auth_url, token_url, redirect_uri)

video_file = r"D:\Videos\Shaad\Shaad Goal\Shaad Goal.mp4"
title = 'Test Video Upload'
description = 'This is a test video uploaded via YouTube API.'
category_id = '22' 
tags = ['test', 'video', 'upload']

video_id = youtube_api.upload_video(video_file, title, description, category_id, tags)
if video_id:
    print(f"Video uploaded successfully with ID: {video_id}")
else:
    print("Failed to upload the video.")
