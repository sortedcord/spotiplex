from plexapi.myplex import MyPlexAccount
import sys
import pickle
from credentials import *

account = None
plex = None

def setup_plex(username, password, servername):
    global account
    try:
        account = MyPlexAccount(f'{username}', f'{password}')
    except:
        print("Error logging in")
        sys.exit(1)
    else:
        print("Logged IN")

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
            flag = True
    
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
            flag = True

    # Pattern match without brackets
    if not flag:
        pattern_track_results = music.searchTracks(title=track.split("[")[0][:-1])
        for i in pattern_track_results:
            if i not in init_track_results and i not in split_track_results:
                song.matching_tracks.append(i)

            if artist.lower() in i.artist().title.lower() or i.artist().title.lower() in artist.lower():
                # change the index to 1 of matching_tracks
                song.matching_tracks.pop()
                song.matching_tracks.insert(0,i)
                flag = True

    if flag:
        return flag,len(song.matching_tracks)

    return False,len(song.matching_tracks)
    
