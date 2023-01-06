import base64
import json
from pprint import pprint

from dotenv import load_dotenv
from spotipy import util, SpotifyClientCredentials, SpotifyOAuth
import spotipy
import requests
import os

load_dotenv()
position = 0


class SpotifyClientManager:
    def __init__(self):
        self.scope = 'playlist-modify-private'
        self.user_id = os.getenv('SPOTIFY_USER_ID')
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')
        self.client_credentials_manager = SpotifyClientCredentials(client_id=self.client_id,
                                                                   client_secret=self.client_secret)
        self.sp = spotipy.Spotify(client_credentials_manager=self.client_credentials_manager)

    @property
    def token(self):
        '''
        Return the access token
        '''
        auth_string = self.client_id + ":" + self.client_secret
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')
        url = "https://accounts.spotify.com/api/token"

        headers = {
            "Authorization": "Basic " + auth_base64,
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = {'grant_type': "client_credentials"}
        result = requests.post(url, headers=headers, data=data)
        json_result = json.loads(result.content)
        token = json_result["access_token"]
        return token

    @property
    def auth(self):
        return spotipy.Spotify(auth_manager=SpotifyOAuth(
            scope=self.scope,
            redirect_uri=self.redirect_uri,
            client_secret=self.client_secret,
            client_id=self.client_id
        ))


class Spotify:
    def __init__(self):
        self.spotify = SpotifyClientManager()
        self.base_url = 'https://api.spotify.com/v1'

    def create_playlist(self, playlist_name: str) -> str:
        spotify_playlist = self.spotify.auth.user_playlist_create(
            self.spotify.user_id, playlist_name,
            description="youtube playlist",
            public=False
        )
        return spotify_playlist['id']

    def get_song_uri(self, song_name: str) -> 'str':
        q = f'{song_name}'
        query = f'https://api.spotify.com/v1/search?q={q}&type=track&limit=1'

        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.spotify.token}"
            }
        )
        if not response.ok:
            return None

        results = response.json()
        items = results['tracks']['items']

        if not items:
            return None

        return items[0]['uri']

    def add_song_to_playlist(self, song_uri: str, playlist_id: str) -> bool:
        try:
            self.spotify.auth.playlist_add_items(playlist_id=playlist_id, items=song_uri)
            return True
        except:
            return False

    def num_playlist_songs(self, playlist_id):
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.spotify.token}"
            }
        )

        if not response.ok:
            return print("Bad Response.")

        results = response.json()
        if 'total' in results:
            return results['total']

        return None


if __name__ == "__main__":
    sp = Spotify()
    pid = sp.create_playlist("loll")
    uri = sp.get_song_uri('flor', 'hold on')
    res = sp.add_song_to_playlist(uri, pid)
    print(sp.num_playlist_songs('7oVpkyA59PIMtE4Bd1Oi2n'))
