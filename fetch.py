import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from func import Song

from credentials import spotify_client_id, spotify_client_secret

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=spotify_client_id,
                                                           client_secret=spotify_client_secret))


def get_playlist_tracks(playlist_id):

    # get all the items in a playlist
    results = sp.playlist_items(f"spotify:playlist:{playlist_id}")

    songs = []

    # print all the artist - titles
    for item in results['items']: 
        track = item['track']
        track = Song(track['name'], track['artists'][0]['name'], track['id'], track['duration_ms'])
        track.cache_track()
        # add to dictionary with artist as key and title as value
        songs.append(track)


    
    # print the number of songs fetched
    print("Fetched " + str(len(songs)) + " songs")
    return songs

    