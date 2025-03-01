import os
import sys
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from socials.youtube import YouTubeAPI

load_dotenv()

youtube_api = YouTubeAPI(email="doestepp@gmail.com", db_params={
    "db_name": os.getenv("DB_NAME"),
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port": os.getenv("DB_PORT"),
})

video_file = r"D:\Videos\Shaad\Shaad Goal\Shaad Goal.mp4"
title = "Test Video Upload"
description = "This is a test video uploaded via YouTube API."
category_id = "22"
tags = ["test", "video", "upload"]

video_id = youtube_api.upload_video(video_file, title, description, category_id, tags)

if video_id:
    print(f"✅ Video uploaded successfully with ID: {video_id}")
else:
    print("❌ Failed to upload the video.")
