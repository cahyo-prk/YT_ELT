from airflow import DAG
import pendulum
from datetime import datetime, timedelta
from api.video_stats import get_playlists_id, get_video_ids, extract_video_data, save_data_to_json

#Define the local timezone
local_tz = pendulum.timezone("Asia/Jakarta")

#Default Args
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'email': "cahyoprakoso50@gmail.com",
    # 'retries': 1,
    # 'retry_delay': timedelta(minutes=5),
    'max_active_runs': 1,
    'dagrun_timeout': timedelta(minutes=60),
    'start_date': datetime(2026, 1, 1, tzinfo=local_tz),
    #'end_date': datetime(2030, 12, 31, tzinfo=local_tz),
}

with DAG(
    dag_id='produce_json',
    default_args=default_args,
    description='A DAG to produce JSON data from YouTube API',
    schedule='0 14 * * *',  # Run at 14:00 (2 PM) every day
    catchup=False,
) as dag:
    
    # Define the tasks in the DAG
    # Task 1: Get Playlist ID
    playlist_id = get_playlists_id()
    # Task 2: Get Video IDs from the Playlist
    video_ids = get_video_ids(playlist_id)
    # Task 3: Extract Video Data
    extracted_data = extract_video_data(video_ids)
    # Task 4: Save Data to JSON
    save_to_json_task = save_data_to_json(extracted_data)

    #Define the task dependencies
    playlist_id >> video_ids >> extracted_data >> save_to_json_task