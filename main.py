from spotify import Spotify
from youtube import Youtube


def main():
    sp = Spotify()
    yt = Youtube()
    found_music = []
    added = 0

    yt_playlist_id = input("Enter youtube playlist id: ")
    spotify_playlist_name = input("Enter a name for your spotify playlist: ")
    spotify_playlist_id = sp.create_playlist(spotify_playlist_name)
    songs = yt.get_songs_from_playlist(yt_playlist_id)

    for song in songs:
        song_uri = sp.get_song_uri(f'{song.artist} {song.title}')

        if not song_uri:
            print(f"{song.artist} - {song.title} was not found!")
            continue
        else:
            added = added + 1
            print(f"The {added}° added!")
        found_music.append(song_uri)

    was_added = sp.add_song_to_playlist(found_music, spotify_playlist_id)

    total_songs_added = sp.num_playlist_songs(spotify_playlist_id)
    print(f'Added {total_songs_added} songs out of {len(songs)}')


if __name__ == "__main__":
    main()
