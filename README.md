# YoutubeToSpotify

A simple script to add all songs from youtube playlist to spotify playlist.

## Example

![](imgs/examplerun.gif)

## What's different in version 2?

```
Faster: Uses Youtube API to get song info instead of selenium.
Convenient: No need to refresh token after every hour.
Reliable: Adds 85-95% of the songs from popular youtube playlists.
```

## Note

`Works only for public youtube playlists.`

## Stats

`Added 142 songs to spotify playlist out of 150 songs from youtube playlist`

## Setup

1.Create an app: https://developer.spotify.com/dashboard/applications

![](imgs/setup.png)

2.Copy the Client id and client secret

![](imgs/copy.png)

3.Set redirect uri to http://localhost:8888/callback
![](imgs/redirecturi.png)

### Get youtube API key

[CLICK HERE TO SEE HOW TO CREATE YOUTUBE API KEY](getkey.md)

### Setting Environment Variables Mac and Linux

1. Rename the file `.env.sample` to `.env`

2. Edit the file by adding your credentials

   1. SPOTIFY_USER_ID: open spotify, go to your profile, three dots, share profile. Take the link that should be like that "https://open.spotify.com/user/your_userId?si=41l9b3cfbc124e1d", your userId is the part that comes after "user/" and before "?si=".

   2. SPOTIFY_CLIENT_ID: In README

   3. SPOTIFY_CLIENT_SECRET: In README

   4. SPOTIFY_REDIRECT_URI: Go to edit settings of app in spotify developer dashboard, than add "http://localhost:8888/callback" to Redirect URIs and click "ADD"

   5. YOUTUBE_API_KEY: In README

   6. GOOGLE_APPLICATION_CREDENTIALS: link to credentials "https://console.cloud.google.com/iam-admin/serviceaccounts". Example to path "credentials.json"

      

3. Put the credentials.json from GOOGLE in the folder YoutubeToSpotify

### Setting Environment Variables (Windows)

```
set SPOTIFY_USER_ID <your_user_id>
set SPOTIFY_CLIENT_ID <your_client_id>
set SPOTIFY_CLIENT_SECRET <your_client_secret>
set SPOTIFY_REDIRECT_URI 'http://localhost:8888/callback'
set YOUTUBE_API_KEY <your_youtube_api_key>
```

## Set requirements

`$ python -m venv venv`

`$ pip install -r .\requirements.txt`

## Usage

`$ python main.py`

## Output

```
Enter youtube playlist id: PLgzTt0k8mXzEpH7-dOCHqRZOsakqXmzmG
Enter a name for your spotify playlist: youtube_chill_songs

The Chainsmokers - Takeaway was added to playlist.
KIRBY-Don't Leave Your Girl was not found!
Lauv - There's No Way was added to playlist.
.
.
.
Usher - Crash was added to playlist.
```

## Example

![](imgs/playlist.png)

## Result

<img src="imgs/playlistphone.jpg" width="49.5%"> <img src="imgs/playlistsongs.jpg" width="49.5%">
