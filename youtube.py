from dataclasses import dataclass
from pprint import pprint
import re
import os

from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from youtube_title_parse import get_artist_title

load_dotenv()


@dataclass
class Song:
    artist: str
    title: str


def clean_song_info(song: Song) -> Song:
    artist, title = song.artist, song.title
    title = re.sub('\(.*', '', title)  # Remove everything after '(' including '('
    title = re.sub('ft.*', '', title)  # Remove everything after 'ft' including 'ft'
    title = re.sub(',.*', '', title)  # Remove everything after ',' including ','
    artist = re.sub('\sx\s.*', '', artist)  # Remove everything after ' x ' including ' x '
    artist = re.sub('\(.*', '', artist)  # Remove everything after '(' including '('
    artist = re.sub('ft.*', '', artist)  # Remove everything after 'ft' including 'ft'
    artist = re.sub(',.*', '', artist)  # Remove everything after ',' including ','
    return Song(artist.strip(), title.strip())  # Remove whitespaces from start and end


class Youtube:
    DEVELOPER_KEY = os.getenv('YOUTUBE_API_KEY')
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    credentials = service_account.Credentials.from_service_account_file(GOOGLE_APPLICATION_CREDENTIALS)

    def __init__(self):
        self.songs = []
        self.youtube = build(
            Youtube.YOUTUBE_API_SERVICE_NAME,
            Youtube.YOUTUBE_API_VERSION,
            developerKey=Youtube.DEVELOPER_KEY
        )

    def __fetch_songs(self, youtube, playlist_id, page_token=None):
        result = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults="300",
            pageToken=page_token
        ).execute()

        for item in result['items']:
            song = item['snippet']['title']
            try:
                artist, title = get_artist_title(song)
                self.songs.append(clean_song_info(Song(artist, title)))
            except:
                print(f'Error parsing {song}')

        return result

    def get_songs_from_playlist(self, playlist_id: str):
        youtube = self.youtube
        result = self.__fetch_songs(youtube, playlist_id)
        while 'nextPageToken' in result:
            page_token = result['nextPageToken']
            result = self.__fetch_songs(youtube, playlist_id, page_token)
        return self.songs


if __name__ == "__main__":
    yt = Youtube()
    print(clean_song_info(Song('Mr. x Probz', 'Waves(Robin Schulz Remix Radio Edit')))
    pprint(yt.get_songs_from_playlist('PLgzTt0k8mXzEpH7-dOCHqRZOsakqXmzmG'))
