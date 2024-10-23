import os
import sys
import requests
import magic  # python-magic for MIME type detection
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from socials.youtube import YouTubeAPI
from socials.instagram import InstagramAPI

load_dotenv()

# YouTube API Setup
youtube_client_id = os.getenv('YOUTUBE_CLIENT_ID')
youtube_client_secret = os.getenv('YOUTUBE_CLIENT_SECRET')
youtube_account_id = os.getenv('YOUTUBE_ACCOUNT_ID')
youtube_auth_url = os.getenv('YOUTUBE_AUTH_URL')
youtube_token_url = os.getenv('YOUTUBE_TOKEN_URL')
youtube_redirect_uri = os.getenv('YOUTUBE_REDIRECT_URI')

youtube_api = YouTubeAPI(
    youtube_client_id, youtube_client_secret, youtube_account_id, 
    youtube_auth_url, youtube_token_url, youtube_redirect_uri
)

# Instagram API Setup
instagram_client_id = os.getenv('INSTAGRAM_CLIENT_ID')
instagram_client_secret = os.getenv('INSTAGRAM_CLIENT_SECRET')
instagram_account_id = os.getenv('INSTAGRAM_ACCOUNT_ID')
instagram_auth_url = os.getenv('INSTAGRAM_AUTH_URL')
instagram_token_url = os.getenv('INSTAGRAM_TOKEN_URL')
instagram_redirect_uri = os.getenv('INSTAGRAM_REDIRECT_URI')

instagram_api = InstagramAPI(
    instagram_client_id, instagram_client_secret, instagram_account_id, 
    instagram_auth_url, instagram_token_url, instagram_redirect_uri
)

# Video details (URL for Instagram)
video_url = r"https://samui-music.com/videos/output.mp4"
local_video_file = "kickingback.mp4"  # Path to temporarily save video locally
title = 'This is a test video uploaded via YouTube API'
description = 'This is a test video uploaded via YouTube API.'
category_id = '22'  # YouTube category ID (e.g., 22 for 'People & Blogs')
tags = ['test', 'video', 'upload']

# Download the video from the URL to a local file for YouTube and detect its type
def download_and_detect_file(url, local_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        # Detect the media type using python-magic
        mime = magic.Magic(mime=True)
        content_type = mime.from_file(local_path)
        print(content_type)
        return content_type
    return None

# Detect the type and process
content_type = download_and_detect_file(video_url, local_video_file)

if content_type:
    if content_type.startswith('video'):
        # Upload video to YouTube using the local file path
        youtube_video_id = youtube_api.upload_video(local_video_file, title, description, category_id, tags)
        if youtube_video_id:
            print(f"Video uploaded successfully to YouTube with ID: {youtube_video_id}")
        else:
            print("Failed to upload the video to YouTube.")
        
        # Clean up the local file after uploading to YouTube
        os.remove(local_video_file)
        
        # Use video_url for Instagram since Instagram accepts remote URLs
        caption = 'This is a test video uploaded via Instagram API'
        instagram_success = instagram_api.upload_and_publish(video_url, caption, media_type="video")

        if instagram_success:
            print("Video uploaded and published successfully to Instagram.")
        else:
            print("Failed to upload and publish the video to Instagram.")
else:
    print("Failed to download or detect the media type.")
