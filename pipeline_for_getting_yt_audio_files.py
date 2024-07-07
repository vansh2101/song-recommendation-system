from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import json
from pytube import YouTube as YT
from youtubesearchpython import VideosSearch
import os
from glob import glob

def get_metadata(record):
    track_details_for_search = {'name':record['SongData']['title'], 'artist':[i['name'] for i in record['SongData']['artists']]}
    if track_details_for_search['artist']:
        return track_details_for_search
    return None

def search_yt(query):
    res = VideosSearch(query=query, limit=1).result()['result']
    if res:
        return res[0]['link']
    return None

def download_audio(yt_link, outpath, song_name):
    try:
        audio = YT(url=yt_link).streams.filter(only_audio=True).first()
        audio.download(output_path=outpath, filename=f'{song_name}.mp3')
    except:
        print(f"Couldn't process {song_name}")

SCOPES = ['https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = 'drive-api-credentials.json'
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=creds)

def upload_to_drive(file_to_be_uploaded, drive_folder_id):
    metadata = {
        'name':os.path.basename(file_to_be_uploaded),
        'parents':[drive_folder_id]
    }
    media = MediaFileUpload(file_to_be_uploaded, mimetype='audio/mp3')
    file = drive_service.files().create(body=metadata, media_body=media, fields='id').execute()
    print(f"FILE ID : {file.get('id')}")

DRIVE_FOLDER_ID = "1KnqSDr72WKcQjj00IwTa_UFCHXIqFukw"

def main(data, output_path, start_idx, len=100):
    for i in range(start_idx, start_idx+len):
        track_details = get_metadata(data[i])
        query = f"{track_details['name']} {' '.join(track_details['artist'])}"
        youtube_link = search_yt(query=query)
        download_audio(youtube_link, output_path, track_details['name'])

    # The loop is done and all audio files are there in the folder.
    files = glob(f'{output_path}\*')
    for file in files:
        upload_to_drive(file, DRIVE_FOLDER_ID)

if __name__ == "__main__":
    with open(r'From AIMS/filtered_songdata.json', 'r') as file:
        raw_data = json.load(file)

    main(raw_data, r'song_files', 0, 100)