from fetch import get_playlist_tracks
from plex import check_if_exist, setup_plex
import rich
from getkey import getkey, keys
import sys
from matching import build
import os
from credentials import plex_email, plex_password, plex_server
from rich import print

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
    if stat and track.confirmed_matching_track is None:
        con.print(f"Song {track_name} exists",style="bold chartreuse3",end=" ")
        con.print(f"by {artist}",style="bold chartreuse3", end=" ")
        con.print(f" {track_res} Tracks.",style="yellow")
        # track.display_color = "chartreuse3"
    elif stat and track.confirmed_matching_track is not None:
        con.print(f"Song {track_name} Confirmed",style="bold cyan2",end=" ")
        con.print(f"by {artist}",style="bold cyan2")
        recognized.append(track)
        # track.display_color = "cyan2"
    elif stat == False and track_res != 0:
        con.print(f"Multiple songs like {track_name} exist",style="bold gold1", end=" ")
        con.print(f" {track_res} Tracks.",style="yellow")
        recognized.append(track)
        # track.display_color = "gold1"
    else:
        con.print(f"Song {track_name} does not exist",style="bold red", end=" ")
        con.print(f"by {artist}",style="bold red")
        # track.display_color = "red"


        not_recognized.append(track)

print("\n")
con.print("Successfully recognized " + str(len(recognized)) + " songs, out of " + str(len(tracks)) + " songs",style="bold green")

con.print("Review Matches? (Y/N)",style="bold yellow",end=" ")

if input().lower() == "y":
        
    selection = 0
    selected_page = 0
    fetch_track = 0

    build(tracks, selection, fetch_track)

    confirmed = None
    while True:
        keymaps = {
        "+": "Next Track",
        "-": "Previous Track",
        "p": "Previous Page",
        "n": "Next Page",
        "Enter": "Confirm Selection",
        "q / ESC": "Quit",
        "Arrows": "Change Selection",
        "a": "Add local track",
        "r": "Reload UI",
        "m": "Mark as missing",
        "j": "Jump to track"
    }

        keymap_str = ""
        _ = 1
        for key, value in keymaps.items():
            if len(keymap_str.replace("[bold green]","").replace("[/bold green]","")) > os.get_terminal_size().columns*_:
                keymap_str += "\n"
                _ += 1
            elif len(str(keymap_str+f"[bold green]{key}[/bold green]: {value}" + "   ").replace("[bold green]","").replace("[/bold green]","")) > os.get_terminal_size().columns*_:
                keymap_str += "\n"
                _ += 1
            keymap_str += f"[bold green]{key}[/bold green]: {value}" + "   "

        print(keymap_str+"\n")

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
        build(tracks, selection, fetch_track, confirmed)
