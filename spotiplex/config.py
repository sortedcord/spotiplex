import sys
import os
import datetime

from rich import print
from rich.console import Console

from plexapi import myplex, server
from deemix.utils.deezer import getAccessToken, getArlFromAccessToken
import deezer
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import pickle


class Config:
    class PlexConfig:
        def __init__(self, username, password):
            self.username = username
            self.password = password

            self.auth()

        def auth(self):
            console = Console()
            with console.status("[bold blue]Setting Up Plex Connection...") as status:
                try:
                    myplex_ = myplex.MyPlexAccount(self.username, self.password)
                    
                except Exception as e:
                    console.log(f"[bold red]Could not login as {self.username}[/bold red]")
                    console.log(e)
                else:
                    console.log(f"[bold green]Logged in as {self.username}[/bold green]")
                
                self.auth_token = myplex_.authenticationToken
                console.log("[bold green]Fetched auth token from Plex [/bold green]")
                
                try:
                    self.server = server.PlexServer(token=self.auth_token)
                except Exception as e:
                    console.log(f"[bold red]Could not find server {self.servername}[/bold red]")
                    console.log(e)
                else:
                    self.servername = self.server.friendlyName
                    console.log(f"[bold green]Found server {self.servername}[/bold green]")
                    console.log(f"[bold green]Connected to {self.servername}[/bold green]")
                    console.log(f"[bold green]Plex Connection Setup Complete[/bold green]")
    
    class SpotifyConfig:
        def __init__(self, client_id, client_secret):
            self.client_id = client_id
            self.client_secret = client_secret
        
            self.auth()

        def auth(self):
            console = Console()
            with console.status("[bold blue]Setting Up Spotify Connection...") as status:
                try:
                    self.conn = spotipy.Spotify(auth_manager=SpotifyClientCredentials(self.client_id, self.client_secret))
                except Exception as e:
                    console.log(f"[bold red]Could not setup spotify api[/bold red]")
                    console.log(e)
                else:
                    console.log(f"[bold green]Spotify API Setup Complete[/bold green]")
                    

    class DeezerConfig:
        def __init__(self, username, password):
            self.username = username
            self.password = password
            self.quality = 3 # 1 = 128, 3 = 320, 9 = FLAC

            self.auth()

        def auth(self):

            console = Console()
            with console.status("[bold blue]Setting Up Deezer Connection...") as status:
                try:
                    self.access_token = getAccessToken(username, password)
                except Exception as e:
                    console.log(f"[bold red]Could not login as {self.username}[/bold red]")
                    console.log(e)
                else:
                    console.log(f"[bold green]Logged in as {self.username}[/bold green]")
                
                try:
                    self.arl = getArlFromAccessToken(self.access_token)
                except Exception as e:
                    console.log(f"[bold red]Could not get ARL from access token[/bold red]")
                    console.log(e)
                else:
                    console.log(f"[bold green]Fetched ARL from access token[/bold green]")
                    console.log(f"[bold green]Deezer Connection Setup Complete[/bold green]")

    def __init__(self, path):
        self.path = path
        self.plex = None
        self.fallback_to_ytm = True
        self.default_browser = "firefox"
        self.ytm_premium = False

        if path == "":
            self.path = str(os.path.dirname(sys.argv[0]))

        # Check path
        if not os.path.exists(self.path):
            print(f"[bold red]Given path {self.path} does not exist[/bold red]")

            while True:
                print("[bold blue]Enter a valid path[/bold blue]")
                self.path = input()
                if os.path.exists(self.path):
                    break
                else:
                    print(f"[bold red]Given path {self.path} does not exist[/bold red]")
                    time.sleep(1)
        
        # Check if consif file exists
        if os.path.exists(self.path+"/spotiplex.confbin"):
            self.read_config()
        else:
            self.generate_config()


    def read_config(self):

        console = Console()
        with console.status("[bold blue]Reading config file...") as status:
            try:
                with open(self.path+"/spotiplex.confbin", "rb") as f:
                    data = pickle.load(f)
            except Exception as e:
                console.log(f"[bold red]Could not read config file[/bold red]")
                console.log(e)
            else:
                console.log(f"[bold green]Config file read successfully[/bold green]")
        
        # Check loaded object integrity
        # Check if all attributes are present  

        with console.status("[bold blue] Checking loaded config") as status:
            try:
                self.plex = data.plex
                self.spotify = data.spotify
                self.deezer = data.deezer
                self.fallback_to_ytm = data.fallback_to_ytm
                self.default_browser = data.default_browser
                self.ytm_premium = data.ytm_premium
                self.last_save = data.last_save

            except Exception as e:
                console.log(f"[bold red]Loaded config is not valid[/bold red]")
                console.log(e)
            else:
                console.log(f"[bold green]Loaded config is valid[/bold green]")                      
        

    def save_config(self):
        with open(self.path+"/spotiplex.confbin", "wb") as f:
            
            self.last_save = datetime.datetime.now()
            pickle.dump(self, f)

    def generate_config(self):
        print(f"[bold blue]Generating config file at [/bold blue] [bold purple]{self.path}[/bold purple]\n\n")

        print(f"[bold gold3]Setup Plex Connection[/bold gold3]\n")
        print(f"[blue]Enter your Plex Username/email: [/blue]", end=" ")
        plex_username = input()

        print(f"[blue]Enter your Plex Password: [/blue]", end=" ")
        plex_password = input()

        self.plex = self.PlexConfig(plex_username, plex_password)

        print(f"\n\n[bold gold3]Setup Spotify Connection[/bold gold3]\n")
        print(f"[blue]Enter your Spotify Client ID: [/blue]", end=" ")
        spotify_client_id = input()
        print(f"[blue]Enter your Spotify Client Secret: [/blue]", end=" ")
        spotify_client_secret = input()

        self.spotify = self.SpotifyConfig(spotify_client_id, spotify_client_secret)

        print(f"\n\n[bold gold3]Setup Deezer Connection[/bold gold3]\n")
        print(f"[blue]Enter your Deezer Username/email: [/blue]", end=" ")
        deezer_username = input()
        print(f"[blue]Enter your Deezer Password: [/blue]", end=" ")
        deezer_password = input()

        self.deezer = self.DeezerConfig(deezer_username, deezer_password)

        self.save_config()

