import requests
import json

import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = "GadgetIn"
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


def get_video_ids(playlistId):
    
    video_ids = []

    page_token = None

    try:
        while True:
            
            url = (
                f"https://youtube.googleapis.com/youtube/v3/playlistItems"
                f"?part=contentDetails"
                f"&maxResults={maxResults}"
                f"&playlistId={playlistId}"
                f"&key={API_KEY}"
            )

            if page_token:
                url += f"&pageToken={page_token}"   

            response = requests.get(url)

            response.raise_for_status()

            data = response.json()

            for item in data.get('items', []):
                video_id = item['contentDetails']['videoId']
                video_ids.append(video_id)

            page_token = data.get('nextPageToken')

            if not page_token:
                break
        
        return video_ids

    except requests.exceptions.RequestException as e:
        raise e

def extract_video_data(video_ids):
    extracted_data = []
    
    def batch_list(video_lst, batch_size):
        for video_id in range(0, len(video_lst), batch_size):
            yield video_lst [video_id:video_id + batch_size]

    try:
        for batch in batch_list(video_ids, maxResults):
            video_ids_str = ",".join(batch)
            url = (
                f"https://youtube.googleapis.com/youtube/v3/videos"
                f"?part=contentDetails,snippet,statistics"
                f"&id={video_ids_str}"
                f"&key={API_KEY}"
            )

            response = requests.get(url)

            response.raise_for_status()

            data = response.json()

            for item in data.get('items', []):
                video_id = item['id']
                snippet = item['snippet']
                content_details = item['contentDetails']
                statistics = item['statistics']

                video_data = {
                    "video_id": video_id,
                    "title": snippet['title'],
                    "published_at": snippet['publishedAt'],
                    "duration": content_details['duration'],
                    "view_count": statistics.get('viewCount', None),
                    "like_count": statistics.get('likeCount', None),
                    "comment_count": statistics.get('commentCount', None),
                }

                extracted_data.append(video_data)

        return extracted_data

    except requests.exceptions.RequestException as e:
        raise e

if __name__ == "__main__":
    playlistId = get_playlists_id()
    video_ids = get_video_ids(playlistId)
    print(extract_video_data(video_ids))