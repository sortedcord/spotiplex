import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from func import Song
import os
from credentials import *

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=spotify_client_id,
                                                           client_secret=spotify_client_secret))
from deezer_python.client import Client
from deemix.utils.deezer import getAccessToken

from rich.live import Live

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
        "Downloaded": "bold deep_pink2"
    }

    main_str = ""

    main_str += f"[bold white]--------------------- [/bold white][bold chartreuse1] Downloading {len(master)} tracks [bold charteuse3] [bold white]---------------------[/bold white]\n"

    for track in master:
        if track['status'] in ('Found','Not Found'):
            main_str += (f"\n[{ref[track['status']]}][{track['status']}]{track['name']} by {track['artist']} [/{ref[track['status']]}]")
            # break
        elif track['status'] == "Searching" or track['status'] == "Analyzing":
            main_str += (f"\n[{ref[track['status']]}][{track['status']}]{track['name']} by {track['artist']} ")
            for query_pattern in track['query_patterns']:
                main_str += (f"Pattern {track['query_patterns'].index(query_pattern)}: [{ref[query_pattern['status']]}]{query_pattern['status']} ")

                # if it is the last query pattern then add a new line
                if track['query_patterns'].index(query_pattern) == len(track['query_patterns']) - 1:
                    main_str += "\n"
            break
    return main_str


def download_deezer(tracks, master):
    from deemix.utils.deezer import getAccessToken, getArlFromAccessToken

    from downloader import download

    # get the access token
    token = getAccessToken(deemix_username, deemix_password)
    arl = getArlFromAccessToken(token)

    with Live(show_download_progress(master), refresh_per_second=9) as live:
        for track in tracks:
            print("Downloading " + track.name + " by " + track.artist)
            downloader = download((f"https://www.deezer.com/en/track/{track.deezer['id']}",), 320, True, path=download_location, arl=arl)
            master[tracks.index(track)]['status'] = "Downloaded"
        live.update(show_download_progress(master))

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

    with Live(show_download_progress(master), refresh_per_second=9) as live:
        live.update(show_download_progress(master))
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

                live.update(show_download_progress(master))
                search_results = client.search(query_pattern)[:8]

                if len(search_results) == 0:
                    master[tracks.index(track)]['query_patterns'][query_patterns.index(query_pattern)]['status'] = "Not Found"
                    # live.update(show_download_progress(master))
                    continue
                
                for result in search_results:
                    result_title = result.title.lower()
                    track_name = track.name.lower()
                    track_artist = track.artist.lower()
                    result_artist_name = result.artist.name.lower()
                    
                    master[tracks.index(track)]['status'] = "Analyzing"
                    live.update(show_download_progress(master))


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
                        tracks[tracks.index(track)].deezer['id'] = result.id
                        live.update(show_download_progress(master))
                        _ = True
                        break
                if _:
                    break
            if not _:
                master[tracks.index(track)]['status'] = "Not Found"
                live.update(show_download_progress(master))

    # Download the tracks that have been found
    found_list = []
    for track in tracks:
        if track.deezer['id'] != None:
            found_list.append(track)
    
    download_deezer(found_list, master)


if __name__ == "__main__":
    from deemix.utils.deezer import getAccessToken, getArlFromAccessToken
    from deemix.__main__ import download

    token = getAccessToken(deemix_username, deemix_password)
    arl = getArlFromAccessToken(token)

    downloader = download((f"https://www.deezer.com/en/track/1733691157",), 320, None, None, arl)