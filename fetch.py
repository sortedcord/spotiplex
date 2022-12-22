import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from func import Song
import os
from credentials import spotify_client_id, spotify_client_secret, deemix_username, deemix_password

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=spotify_client_id,
                                                           client_secret=spotify_client_secret))
from deezer.client import Client
from deemix.utils.deezer import getAccessToken

from rich import print
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def get_playlist_tracks(playlist_id):

    # get all the items in a playlist
    results = sp.playlist_items(f"spotify:playlist:{playlist_id}")

    songs = []

    # print all the artist - titles
    for item in results['items']:  # type: ignore
        track = item['track']
        track = Song(track['name'], track['artists'][0]['name'], track['id'], track['duration_ms'])
        track.cache_track()
        # add to dictionary with artist as key and title as value
        songs.append(track)


    
    # print the number of songs fetched
    print("Fetched " + str(len(songs)) + " songs")
    return songs

def show_download_progress(master):
    # clear console
    os.system('cls' if os.name == 'nt' else 'clear')

    ref = {
        "Searching": "bold blue",
        "Inactive": "gray",
        "Found": "bold green",
        "Analyzing": "bold yellow",
        "Not Found": "bold red",
    }

    main_str = ""

    for track in master:
        if track['status'] in ('Found','Inactive','Not Found'):
            main_str += (f"\n[{ref[track['status']]}][{track['status']}]{track['name']} by {track['artist']}")
        elif track['status'] == "Searching" or track['status'] == "Analyzing":
            main_str += (f"\n[{ref[track['status']]}][{track['status']}]{track['name']} by {track['artist']} ")
            for query_pattern in track['query_patterns']:
                main_str += (f"Pattern {track['query_patterns'].index(query_pattern)}: [{ref[query_pattern['status']]}]{query_pattern['status']} ")
    print(main_str,end="\r")




def search_deezer(tracks):
    access_token = getAccessToken(deemix_username, deemix_password)

    deemix_track_ids = []

    client = Client(access_token=access_token)

    master = []
    for track in tracks:
        master.append({'name':track.name,
                        'artist':track.artist,
                        'status':'Inactive'
        })


    show_download_progress(master)
    for track in tracks:

        query_patterns = [
            f"{track.name} {track.artist}",
            f"{track.name}",
            f"{track.name.split('[')[0]}",
            f"{track.name.split('(')[0]}",
        ]

        _ = False

        for query_pattern in query_patterns:
            master[tracks.index(track)]['status'] = "Searching"
            master[tracks.index(track)]['query_patterns'] = [{'status':'Inactive'},{'status':'Inactive'},{'status':'Inactive'},{'status':'Inactive'}]
            master[tracks.index(track)]['query_patterns'][query_patterns.index(query_pattern)]['status'] = "Searching"

            show_download_progress(master)
            search_results = client.search(query_pattern)[:8]

            if len(search_results) == 0:
                master[tracks.index(track)]['query_patterns'][query_patterns.index(query_pattern)]['status'] = "Not Found"
                show_download_progress(master)
                continue
            
            for result in search_results:
                result_title = result.title.lower()
                track_name = track.name.lower()
                track_artist = track.artist.lower()
                result_artist_name = result.artist.name.lower()
                
                master[tracks.index(track)]['status'] = "Analyzing"
                show_download_progress(master)


                if result_title in track_name or track_name in result_title:
                    if result_artist_name != track_artist:
                        if similar(result_artist_name, track_artist) > 0.7:
                            print(f"[bold yellow]Is {track_name} - {track.artist} the same as {result_title} - {result_artist_name}? (Y/N)")
                            if input().lower() == "y":
                                pass
                            else:
                                continue
                        else:
                            continue
                    track.matching_tracks.append(result)
                    track.update_status()
                    master[tracks.index(track)]['query_patterns'][query_patterns.index(query_pattern)]['status'] = "Found"
                    master[tracks.index(track)]['status'] = "Found"
                    show_download_progress(master)
                    _ = True
                    break
            if _:
                break
        if not _:
            master[tracks.index(track)]['status'] = "Not Found"
            show_download_progress(master)
