from fetch import get_playlist_tracks
from plex import check_if_exist, setup_plex
import rich
from getkey import getkey, keys
import sys
from matching import build

from credentials import plex_email, plex_password, plex_server

con = rich.get_console()

setup_plex(plex_email,plex_password,plex_server)
tracks = get_playlist_tracks("37i9dQZF1ELZGwXK5139kh")


print("\n")
recognized = []
not_recognized = []

for track in tracks:
    track_name = track.name
    artist = track.artist

    stat, track_res = check_if_exist(track)

    if stat:
        con.print(f"Song {track_name} exists",style="bold chartreuse3",end=" ")
        con.print(f"by {artist}",style="bold chartreuse3", end=" ")
        con.print(f" {track_res} Tracks.",style="yellow")

        recognized.append(track)
    elif stat == False and track_res != 0:
        con.print(f"Multiple songs like {track_name} exist",style="bold green", end=" ")
        con.print(f" {track_res} Tracks.",style="yellow")
        recognized.append(track)
    
    else:
        con.print(f"Song {track_name} does not exist",style="bold red", end=" ")
        con.print(f"by {artist}",style="bold red")


        not_recognized.append(track)

print("\n")
con.print("Successfully recognized " + str(len(recognized)) + " songs, out of " + str(len(tracks)) + " songs",style="bold green")

con.print("Review Matches?",style="bold yellow",end=" ")
if input().lower() == "y":
        
    selection = 0
    selected_page = 0
    fetch_track = 0

    build(tracks, selection, fetch_track)

    confirmed = None
    while True:
        key = getkey()
        if key == keys.LEFT:
            selection -= 1
        elif key == keys.RIGHT:
            selection += 1
        elif key == keys.UP:
            selection -= 2
        elif key == keys.DOWN:
            selection += 2
        elif key == 'p':
            selection -= 4
        elif key == 'n':
            selection += 4
        elif key == keys.ESC:
            sys.exit()
        elif key == 'q':
            sys.exit()
        elif key == '=':
            fetch_track += 1
            selection = 0
            selected_page = 0
            confirmed = None
        elif key == '-':
            selection = 0
            selected_page = 0
            fetch_track -= 1
            confirmed = None
        # When enter key is presed
        elif key == keys.ENTER:
            confirmed = selection
        
        if fetch_track < 0:
            fetch_track = 0
        if fetch_track >= len(tracks):
            fetch_track = len(tracks) - 1

        if selection < 0:
            selection = 0
        if selection >= len(tracks[fetch_track].matching_tracks):
            selection = len(tracks[fetch_track].matching_tracks) - 1
        build(tracks, selection, fetch_track, confirmed)


else:
    pass