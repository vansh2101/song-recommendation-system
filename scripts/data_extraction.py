import requests
from urllib.parse import urlencode
from base64 import b64encode
from datetime import datetime

#* Global Functions
def post_data(url, data, headers=None):
    response = requests.post(url, data=data, headers=headers)

    return response.json()


def get_data(url, data, query=True, token=None):
    if query == False:
        url = url + '/' + data
    else:
        url = url + "?" + urlencode(data)

    if token:
        headers = {'Authorization': f"Bearer {token}"}
    else:
        headers = None

    response = requests.get(url, headers=headers)

    return response.json()


def age(date):
    try:
        date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        try:
            date = datetime.strptime(date, "%Y")
        except ValueError:
            return 0
    
    today = datetime.now()

    years = today.year - date.year

    try:
        if today.month - date.month < -2:
            years -= 1
    except:
        pass

    return years


#* SpotifyAPI Class
class SpotifyAPI:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = "https://accounts.spotify.com/api/token"
        self.api_url = "https://api.spotify.com/v1/"

    def get_access_token(self):
        auth = (self.client_id + ":" + self.client_secret).encode("ascii")
        auth_string = b64encode(auth).decode("ascii")

        token = post_data(self.token_url,
                  data = {"grant_type": "client_credentials"},
                  headers = {"Authorization": "Basic " + auth_string}
                  )

        self.access_token = token["access_token"]

        return {'msg': "Access Token Generated", 'validity': token["expires_in"]}
    
    def fetch_song(self, song_id):
        song = get_data(self.api_url+"tracks", song_id, query=False, token=self.access_token)

        song_data = {
            "album_type": song["album"]["album_type"],
            "album_name": song["album"]["name"],
            "album_artist": [artist['name'] for artist in song['album']['artists']],
            "popularity": song["popularity"],
            "age": age(song["album"]["release_date"]),
            "explicit": song["explicit"],
        }

        return song_data
    
    def fetch_artist(self, artist_id):
        artist = get_data(self.api_url+"artists", artist_id, query=False, token=self.access_token)

        artist_data = {
            "artist_genre": artist['genres'],
            "artist_popularity": artist['popularity'],
            "artist_followers": artist['followers']['total'],
        }

        return artist_data
    
    def fetch_audio_features(self, song_id):
        features = get_data(self.api_url+"audio-features", song_id, query=False, token=self.access_token)

        try:
            audio_features = {
                "acousticness": features["acousticness"],
                "danceability": features["danceability"],
                "energy": features["energy"],
                "instrumentalness": features["instrumentalness"],
                "key": features["key"],
                "liveness": features["liveness"],
                "loudness": features["loudness"],
                "mode": features["mode"],
                "speechiness": features["speechiness"],
                "tempo": features["tempo"],
                "valence": features["valence"],
            }
        except:
            audio_features = {}

        return audio_features
    
    def fetch_audio_analysis(self, song_id):
        analysis = get_data(self.api_url+"audio-analysis", song_id, query=False, token=self.access_token)

        try:
            audio_analysis = {
                "num_sections": len(analysis["sections"]),
                "num_segments": len(analysis["segments"]),
            }
        except:
            audio_analysis = {}

        return audio_analysis
    

#* LastFMAPI Class
class LastFMAPI:
    def __init__(self, key):
        self.key = key
        self.api_url = "http://ws.audioscrobbler.com/2.0"
    
    def fetch_song(self, song_name, artist_name):
        song = get_data(self.api_url, {
            "method": "track.getinfo",
            "api_key": self.key,
            "track": song_name,
            "artist": artist_name,
            "format": "json"
        })

        if 'error' in song.keys():
            print("\tLastFM Error: ", song['message'])
            return {}

        song = song["track"]

        try:
            ratio = int(song['listeners'])/int(song['playcount'])
        except:
            ratio = 0

        song_data = {
            "duration": int(song["duration"]),
            "listener_play_ratio": ratio,
            "genre": [tag['name'] for tag in song['toptags']['tag']],
            "song_url": song['url'],
        }

        return song_data