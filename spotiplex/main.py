import os
import sys

# Rich imports
from rich import print
# from cursesmenu import CursesMenu

# Spotiplex imports
from utils import logo_str, Menu
from layouts.main_menu import main
from config import Config
from platforms.spotify import checkPlaylistLink

# ==================== #

# Exit the program is the terminal height is less than 35
if os.get_terminal_size().lines < 27:
    print("[red]Terminal height is too small, please resize the terminal to be at least 35 lines tall[/red]")
    sys.exit()


my_config = Config("")

sel=main()
# sel = 0: Start
# sel = 1: Settings

if sel == 0:
    # Clear the console
    os.system("cls" if os.name == "nt" else "clear")

    platform_list = ["Spotify"]   #, "Deezer", "Youtube"]

    platform_select_menu = Menu("Select a platform", platform_list)
    import_platform = platform_list[platform_select_menu.get_selection()]
    # import_platform = platform_list[0]

    print("[bold yellow] Enter the playlist link: [/bold yellow]", end="")
    playlist_link = input()


    if import_platform == "Spotify":
        checkPlaylistLink(my_config, playlist_link)









