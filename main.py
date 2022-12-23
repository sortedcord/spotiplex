from fetch import get_playlist_tracks, search_deezer
from plex import check_if_exist, setup_plex
import rich
from getkey import getkey, keys
import sys
from matching import build
import os
from credentials import plex_email, plex_password, plex_server
from rich import print
from difflib import SequenceMatcher

from rich.live import Live

con = rich.get_console()

setup_plex(plex_email,plex_password,plex_server)
tracks = get_playlist_tracks("5Ux5UONLss471Zz4FAHESP")



print("\n")
recognized = []
not_recognized = []

for track in tracks:
    track_name = track.name
    artist = track.artist

    stat, track_res = check_if_exist(track)

    track.update_status()
   
    if stat or track.confirmed_matching_track_index is not None:
        track.display_color = "cyan1"
        print(f"[bold {track.display_color}] Track {track.name} - {track.artist} is found.[/bold {track.display_color}]", end="")
        recognized.append(track)
        if track_res > 1:
            print(f"[chartreuse1] Found {track_res} similar tracks.[/chartreuse1]")
        else:
            print()
    else:
        if track_res > 0:
            print(f"[bold gold1] Track {track.name} - {track.artist} is not found.[/bold gold1]", end="")
            print(f"[bold gold1] Found {track_res} similar track(s).[/bold gold1]")
            not_recognized.append(track)
        else:
            print(f"[bold red] Track {track.name} - {track.artist} is not found.[/bold red]")
            not_recognized.append(track)


print("\n")
con.print("Successfully recognized " + str(len(recognized)) + " songs, out of " + str(len(tracks)) + " songs",style="bold green")

con.print("Review Matches? (Y/N)",style="bold yellow",end=" ")

if input().lower() == "y":

    print("\n\n")
    selection = 0
    selected_page = 0
    fetch_track = 0

    # build(tracks, selection, fetch_track)

    with Live(build(tracks, selection, fetch_track), refresh_per_second=2) as live:

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
                break
            elif key == 'q':
                break
                
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

            elif key == '+':
                selection = 0
                selected_page = 0
                confirmed = None

                # Jump to next unconfirmed track
                for i in range(fetch_track+1,len(tracks)):
                    if tracks[i].confirmed_matching_track is None:
                        fetch_track = i
                        break


            elif key == '_':
                selection = 0
                selected_page = 0
                confirmed = None

                # Jump to previous unconfirmed track
                for i in range(fetch_track-1,-1,-1):
                    if tracks[i].display_color == 'red':
                        fetch_track = i
                        break
                

            # When enter key is presed
            elif key == keys.ENTER:
                if tracks[fetch_track].display_color != 'red':
                    confirmed = selection
                    tracks[fetch_track].confirmed_matching_track_index = selection
                    tracks[fetch_track].confirmed_matching_track = tracks[fetch_track].matching_tracks[selection]

            elif key=="r":
                pass

            elif key == 'm':
                print(f"[bold red]Are you sure you want to mark {tracks[fetch_track].name} as missing?[/bold red][red]\n This would mean that there are no local tracks that match this song.[/red] [bold red]Y/N[/bold red] ",end=" ")
                confirmation = input()
                if confirmation.lower() == "y":
                    tracks[fetch_track].confirmed_matching_track = None
                    tracks[fetch_track].confirmed_matching_track_index = None
                    tracks[fetch_track].matching_tracks = []

            elif key == 'j':
                print(f"[bold green]Jump to track number (1-{len(tracks)}):[/bold green] ",end="")
                jump_selection = input()
                if jump_selection.isnumeric():
                    jump_selection = int(jump_selection)
                    if jump_selection > 0 and jump_selection <= len(tracks):
                        fetch_track = jump_selection - 1
                        selection = 0
                        selected_page = 0
                        confirmed = None
                    else:
                        print(f"[bold red]Invalid track number.[/bold red]")


            if fetch_track < 0:
                fetch_track = 0
            if fetch_track >= len(tracks):
                fetch_track = len(tracks) - 1

            if selection < 0:
                selection = 0
            if selection >= len(tracks[fetch_track].matching_tracks):
                selection = len(tracks[fetch_track].matching_tracks) - 1

            tracks[fetch_track].update_status()
            live.update(build(tracks, selection, fetch_track, confirmed))
            # build(tracks, selection, fetch_track, confirmed)

    download_list = []

    for track in tracks:
        if track.display_color == 'red':
            download_list.append(track)
    
    print("[bold green]Tracks to be Downloaded:- [/bold green]")
    for i in download_list:
        print(f"{i.artist} - {i.name}")
    
    print("\n[yellow]Continue Downloading these tracks? (Y/N)[yellow]",end=" ")

    download_confirmation = input()

    if download_confirmation.lower() == "y":
        print("[bold green]Downloading tracks...[/bold green]")
        search_deezer(download_list)

    
