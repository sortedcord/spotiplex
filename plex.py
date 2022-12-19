from plexapi.myplex import MyPlexAccount
import sys
import pickle
from credentials import *
from rich import print

account = None
plex = None

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


def check_if_exist(song):
    track = song.name
    artist = song.artist

    music = plex.library.section('Music') # type: ignore
    
    # Search for Tracks
    # print(f"Query: {track}")
    init_track_results = music.searchTracks(title=track)
    flag = False
    for i in init_track_results:
        song.matching_tracks.append(i)


        if artist.lower() in i.artist().title.lower() or i.artist().title.lower() in artist.lower():
            # change the index to 1 of matching_tracks
            song.matching_tracks.pop()
            song.matching_tracks.insert(0,i)

            if i.title.lower() == track.lower():
                song.confirmed_matching_track = i
            flag = True

    if song.confirmed_matching_track:
        song.confirmed_matching_track_index = song.matching_tracks.index(song.confirmed_matching_track)

    
    if flag:
        return flag,len(song.matching_tracks)
    
    # Search for Tracks without remix or feat
    split_track_results = music.searchTracks(title=track.split("-")[0])
    flag = False
    for i in split_track_results:
        if i not in init_track_results:
            song.matching_tracks.append(i)

        if artist.lower() in i.artist().title.lower() or i.artist().title.lower() in artist.lower():
            # change the index to 1 of matching_tracks
            song.matching_tracks.pop()
            song.matching_tracks.insert(0,i)

            if i.title.lower() == track.lower():
                song.confirmed_matching_track = i
            flag = True

    if song.confirmed_matching_track:
        song.confirmed_matching_track_index = song.matching_tracks.index(song.confirmed_matching_track)

    # Pattern match without brackets
    if not flag:
        pattern_track_results = music.searchTracks(title=track.split("[")[0][:-1])
        for i in pattern_track_results:
            if i not in init_track_results and i not in split_track_results:
                song.matching_tracks.append(i)

            if artist.lower() in i.artist().title.lower() or i.artist().title.lower() in artist.lower():

                if i.title.lower() == track.lower():
                    song.confirmed_matching_track = i

                # change the index to 1 of matching_tracks
                song.matching_tracks.pop()
                song.matching_tracks.insert(0,i)
                flag = True

    if song.confirmed_matching_track:
        song.confirmed_matching_track_index = song.matching_tracks.index(song.confirmed_matching_track)

    if flag:
        return flag,len(song.matching_tracks)

    return False,len(song.matching_tracks)
    
