from plexapi.myplex import MyPlexAccount
import sys
import pickle
from credentials import *
from rich import print
from difflib import SequenceMatcher


account = None
plex = None

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def parse_song(song):
    return {
        'title':song.title,
        'artist':song.artist().title,
        'album': song.parentTitle,
        'duration': song.duration,
        'id': song.guid
    }

def setup_plex(username, password, servername):
    global account
    try:
        account = MyPlexAccount(f'{username}', f'{password}')
    except:
        print("[bold red]Error logging in[/bold red]")
        sys.exit(1)
    else:
        print("[bold green]Successfully logged in[/bold green]")

    global plex
    try:
        with open('plex.pickle', 'rb') as f:
            plex = pickle.load(f)
            print("Loaded from pickle")
    except FileNotFoundError:
        plex = account.resource(f'{servername}').connect()  # returns a PlexServer instance

    # dump plex object using pickle
    with open('plex.pickle', 'wb') as f:
        pickle.dump(plex, f)


def add_track(local, fetch, confirm=False):
    fetch = parse_song(fetch)
    # Add if it doesn't exist
    if fetch not in local.matching_tracks:
        local.matching_tracks.append(fetch)

        if confirm:
            local.confirmed_matching_track = fetch
            local.matching_tracks.pop()
            local.matching_tracks.insert(0,fetch)
            local.confirmed_matching_track_index = 0

def check_if_exist(song):
    local_track_name = song.name.lower()
    local_artist_name = song.artist.lower()

    # Setup up plex API
    music = plex.library.section('Music') # type: ignore

    pattern_matches = [
        local_track_name,
        local_track_name.split("-")[0],
        local_track_name.split("(")[0][:-1],
        local_track_name.split("[")[0][:-1],
    ]

    for pattern_index in range(len(pattern_matches)):

        # Search for the track
        track_results = music.searchTracks(title=pattern_matches[pattern_index])

        for track in track_results:
            result_track_name = track.title.lower()
            result_artist_name = track.artist().title.lower()

            # IDEAL CASE: Track name and artist name match
            if result_track_name == local_track_name and result_artist_name == local_artist_name:
                add_track(song, track, confirm=True)

                # Return true and length of matching tracks
                return True, 1

            # SECOND BEST CASE: Track name is a substring of each other and artist matches
            elif local_track_name in result_track_name or result_track_name in local_track_name and result_artist_name == local_artist_name:
                add_track(song, track, confirm=True)

                return True, len(song.matching_tracks)
                
            
            # THIRD BEST CASE: Artist name is a substring of each other and track matches
            elif local_artist_name in result_artist_name or result_artist_name in local_artist_name and result_track_name == local_track_name:
                add_track(song, track, confirm=True)

            # Case 4: Track name is a substring and artist name is in the track name
            elif local_track_name in result_track_name or result_track_name in local_track_name and local_artist_name in result_track_name:
                add_track(song, track, confirm=True)
            
            # Case 4: Track name is a substring of each other and artist name is a substring of each other
            elif local_track_name in result_track_name or result_track_name in local_track_name and local_artist_name in result_artist_name or result_artist_name in local_artist_name:
                add_track(song, track)
            
            # Case 5: Track name is a substring but artist name is similar
            elif local_track_name in result_track_name or result_track_name in local_track_name and similar(local_artist_name, result_artist_name) > 0.8:
                add_track(song, track)
            
            # Case 6: Track name is a substring
            elif local_track_name in result_track_name or result_track_name in local_track_name:
                add_track(song, track)

        # If there are confirmed tracks then break
        if len(song.matching_tracks) > 0:
            break

    # Return false and length of matching tracks
    return False, len(song.matching_tracks)

    
