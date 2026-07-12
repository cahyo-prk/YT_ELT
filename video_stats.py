import requests
import json

import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = "NVIDIA"

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

if __name__ == "__main__":
     get_playlists_id()