from spotify import Spotify
from youtube import Youtube
import os
from dotenv import load_dotenv

def main():
    load_dotenv()
    sp = Spotify(os.environ.get('SPOTIFY_USER_ID'), os.environ.get('SPOTIFY_CLIENT_ID'), os.environ.get('SPOTIFY_CLIENT_SECRET'), os.environ.get('SPOTIFY_REDIRECT_URI'))
    yt = Youtube(os.environ.get('YOUTUBE_API_KEY'))
    
    yt_playlist_id = input("Enter youtube playlist id: ")
    spotify_playlist_name = input("Enter a name for your spotify playlist: ")
    spotify_playlist_id = sp.create_playlist(spotify_playlist_name)
    songs = yt.get_songs_from_playlist(yt_playlist_id)

    for song in songs:
        song_uri = sp.get_song_uri(song.artist, song.title)

        if not song_uri:
            print(f"{song.artist} - {song.title} was not found!")
            continue
        
        was_added = sp.add_song_to_playlist(song_uri, spotify_playlist_id)

        if was_added:
            print(f'{song.artist} - {song.title} was added to playlist.')

    total_songs_added = sp._num_playlist_songs(spotify_playlist_id)
    print(f'Added {total_songs_added} songs out of {len(songs)}')

if __name__ == "__main__":
    main()
