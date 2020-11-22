from spotify import Spotify
from youtube import Youtube

def main():
    sp = Spotify()
    yt = Youtube()
    
    yt_playlist_id = input("Enter youtube playlist id: ")
    spotify_playlist_name = input("Enter a name for your spotify playlist: ")
    songs = yt.get_songs_from_playlist(yt_playlist_id)
    spotify_playlist_id = sp.create_playlist(spotify_playlist_name)

    for song in songs:
        song_uri = sp.get_song_uri(song.artist, song.title)
        was_added = sp.add_song_to_playlist(song_uri, spotify_playlist_id)
        if was_added:
            print(f'{song.artist} - {song.title} was added to playlist.')


if __name__ == "__main__":
    main()
