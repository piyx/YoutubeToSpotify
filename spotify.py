from pprint import pprint
from spotipy import util
import requests
import os


class SpotifyClientManager:
    def __init__(self):
        self.scope = 'playlist-modify-private'
        self.user_id = os.getenv('SPOTIFY_USER_ID')
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')

    @property
    def token(self):
        '''
        Return the access token
        '''
        return util.prompt_for_user_token(
            self.user_id,
            scope=self.scope,
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri
        )


class Spotify:
    def __init__(self):
        self.spotify = SpotifyClientManager()

    def create_playlist(self, playlist_name: str) -> str:
        request_body = {
            "name": playlist_name,
            "description": "youtube playlist",
            "public": False
        }

        query = f"https://api.spotify.com/v1/users/{self.spotify.user_id}/playlists"

        response = requests.post(
            query,
            json=request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.spotify.token}"
            }
        )

        playlist = response.json()
        return playlist['id']

    def get_song_uri(self, artist: str, song_name: str) -> 'str':
        q = f'artist:{artist} track:{song_name}'
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
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        response = requests.post(
            url,
            json={"uris": [song_uri]},
            headers={
                "Authorization": f"Bearer {self.spotify.token}",
                "Content-Type": "application/json"
            }
        )
        return response.ok


if __name__ == "__main__":
    sp = Spotify()
    pid = sp.create_playlist("loll")
    uri = sp.get_song_uri('flor', 'hold on')
    res = sp.add_song_to_playlist(uri, pid)
    print(res)
