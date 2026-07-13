from requests import exceptions
import requests
import json

import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = "NVIDIA"
maxResults  = 50

def get_playlists_id():
    try:       
        url = (
            f"https://youtube.googleapis.com/youtube/v3/channels"
            f"?part=contentDetails"
            f"&forHandle={CHANNEL_HANDLE}"
            f"&key={API_KEY}"
        )

        response = requests.get(url)

        response.raise_for_status()

        data = response.json()

        # print(json.dumps(data, indent=4))

        channel_items = data['items'][0]

        channel_playlistId = channel_items['contentDetails']['relatedPlaylists']['uploads']

        print(channel_playlistId)

        return channel_playlistId

    except requests.exceptions.RequestException as e:
        raise e


playlistId = get_playlists_id()

def get_video_ids(playlistId):

    videos_ids = []

    page_token = None

    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResults}&playlistId={playlistId}&key={}"

    try:
        while True:
            url = base

    except requests.exceptions.RequestException as e:
        raise e

if __name__ == "__main__":
     get_playlists_id()