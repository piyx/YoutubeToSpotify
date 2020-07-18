from yt import Youtube
from sptfy import Spotify


def main():
    # Playlist url
    playlist_url = input("Enter youtube playlist url: ")
    playlist_name = input("Enter playlist name: ")

    # Youtube instance
    yt = Youtube(playlist_url)
    song_titles = yt.get_songs_title()
    print(len(song_titles))
    songs_info = yt.get_songs_info(song_titles)
    print(len(songs_info))

    # Spotify instance
    sptfy = Spotify()
    playlst_id = sptfy.create_playlist(playlist_name)

    for song_name, artist in songs_info.items():
        uri = sptfy.get_spotify_uri(artist, song_name)
        status = sptfy.add_songs_to_playlist(playlst_id, {"uris": [uri]})
        if status:
            print(f"{artist}-{song_name} was added to playlist.")
        else:
            print(f"\nERROR!! {artist}-{song_name} could not be added.\n")


if __name__ == "__main__":
    main()
