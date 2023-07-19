from dotenv import load_dotenv
import os
import requests
import spotipy
import deezer
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
load_dotenv()


def getTracks():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ["SPOTIPY_CLIENT_ID"],
                                                   client_secret=os.environ["SPOTIPY_CLIENT_SECRET"],
                                                   redirect_uri=os.environ["SPOTIPY_REDIRECT_URI"],
                                                   scope="user-library-read"))
    data = []

    offset = 0
    limit = 50
    while True:
        results = sp.current_user_saved_tracks(limit=limit, offset=offset)
        if not results['items']:
            break
        for idx, item in enumerate(results['items']):
            track = item['track']
            data.append((track['name'],track['artists'][0]['name']))
            #print(f"{idx + offset + 1}. {track['name']} by {track['artists'][0]['name']}")
        offset += limit
    return data

def addMusic(track_id):
    url = f"http://api.deezer.com/playlist/{os.environ['DEEZER_PLAYLIST_ID']}/tracks?access_token={os.environ['API_TOKEN']}&request_method=post&songs={track_id}"
    response = requests.post(url)
    if response.json() != True:
        f = open(file="errors.txt", mode="a+")
        f.write(f"{track_id}\n")
        f.close()
    if response.status_code == 200:
        print(f"La musique avec l'ID {track_id} a été ajoutée à la playlist.")
    else:
        print("Erreur lors de l'ajout de la musique à la playlist.")

def findMusic(name :str, artist : str):
    client = deezer.Client()
    m = client.search(f"{name} {artist}")
    track = m[0]
    return track.id

def transferLikes():
    arr = getTracks()
    for item in arr:
        song = item[0]
        artist = item[1]
        try:
            trackid = findMusic(song, artist)
            addMusic(trackid)
        except:
            f = open(file="errors.txt", mode="a+", encoding='utf-8')
            try:
                f.write(f"{song}-{artist}")
            except:
                print(song, artist)
                f.write(f"{song}\n")
            f.close()


transferLikes()