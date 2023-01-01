from rich import print
from rich.console import Console
import logging



def checkPlaylistLink(config, playlist_link):
    print("[bold chartreuse3]Checking playlist...[/bold chartreuse3]")
    console2 = Console()

    with console2.status("[bold chartreuse3]Checking playlist...") as status:

        # Check if the user has input the entire playlist link or just the playlist id
        if "playlist" in playlist_link:
            try:
                playlist_id = playlist_link.split("playlist/")[1].split("?")[0]
                console2.log(f"[bold chartreuse3]Playlist ID: {playlist_id} extracted successfully[/bold chartreuse3]")
            except IndexError:
                console2.log("[bold red]Invalid playlist link format[/bold red]")
                
        else:
            playlist_id = playlist_link

        # Check id length
        # Spotify playlist id length is 22
        
        if len(playlist_id) != 22:
            console2.log("[bold red]Invalid playlist ID format[/bold red]")
            return False 

        # Check if the playlist exists using spotipy
        while True:
            try:
                playlist = config.spotify.conn.playlist(playlist_id)
            except AttributeError:
                console2.log("[bold red]Spotify API not setup[/bold red]")

                config.spotify.auth()

            except Exception as e:
                console2.log(f"[bold red]Could not get playlist using spotipy[/bold red]")
                console2.log(e)
                return False
            else:
                console2.log(f"[bold chartreuse3]Playlist {playlist['name']} found[/bold chartreuse3]")
                return True

            
if __name__ == "__main__":
    checkPlaylistLink(None, "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M?si=34c3c3b9e9f44d8b")
