from rich import print
from rich.layout import Layout
from rich.panel import Panel
import sys,os



def ms_to_min(ms):
        seconds = (ms / 1000) % 60
        seconds = int(seconds)
        minutes = (ms / (1000 * 60)) % 60
        minutes = int(minutes)
        if seconds < 10:
            seconds = f"0{seconds}"
        return f"{minutes}:{seconds}"

def build(tracks, selection, fetch_track, confirmed=None):
    os.system('cls' if os.name == 'nt' else 'clear')

    if confirmed is None:
        confirmed = tracks[fetch_track].confirmed_matching_track_index


    current_fetched_track = tracks[fetch_track]
    fetch_track_name = current_fetched_track.name
    fetch_track_artist = current_fetched_track.artist
    fetch_track_duration = current_fetched_track.duration
    fetch_track_spotify_id = current_fetched_track.spot_id

    if len(tracks) <= 4:
        total_pagination= 1
    else:
        total_pagination = (len(tracks[fetch_track].matching_tracks) // 4) + 1
    panel_pages= []

    build_item = 0
    for panel_page_index in range(total_pagination):
        page_layout = Layout()

        if not tracks[fetch_track].matching_tracks:
            page_layout.update(Panel(f"[bold red]No matching tracks found for {fetch_track_name}[/bold red]"))

            panel_page = Panel(page_layout, title=f"[bold green]Page 0 [/bold green] of 0")
            panel_pages.append(panel_page)

            break

        page_layout.split_column(
            Layout(name="col1"),
            Layout(name="col2"),
        )

        page_layout['col1'].split_row(
            Layout(name="item1x1"),
            Layout(name="item2x1"),
        )

        page_layout['col2'].split_row(
            Layout(name="item1x2"),
            Layout(name="item2x2"),
        )
        
        layout_match = {
            "1": 'item1x1',
            "2": 'item2x1',
            "3": 'item1x2',
            "4": 'item2x2'
        }

        try:
            i = 1
            for data in tracks[fetch_track].matching_tracks[int(panel_page_index*4):int((panel_page_index+1)*4)]:
                _panel_title = "[bold blue]Track Name:[/bold blue] [bold white]{}[/bold white]"
                
                panel_style = ""
                if build_item == selection and build_item != confirmed:
                    panel_title = _panel_title + " [bold gold3] [SELECTED][/bold gold3]"
                    panel_style = "bold gold3"
                elif  build_item == confirmed:
                    panel_title = _panel_title + " [bold chartreuse3] [CONFIRMED][/bold chartreuse3]"
                    panel_style = "bold chartreuse3"
                else:
                    panel_title = _panel_title

                panel = Panel(f"""[bold blue]Track Name:[/bold blue] [bold white]{data['title']}[/bold white] 
[bold blue]Artist[/bold blue]: [bold white]{data['artist']}[/bold white]
[bold blue]Duration[/bold blue]: [bold white]{ms_to_min(int(data['duration']))}[/bold white]
[bold blue]Album[/bold blue]: [bold white]{data['album']}[/bold white]""",title=panel_title.format(build_item+1),style=panel_style) # type: ignore 
                
                page_layout[layout_match[str(i)]].update(panel)
                build_item += 1
                i += 1
        except IndexError:
            pass
        
        # If on the last page and there are less than 4 items
        if panel_page_index == total_pagination - 1:
            if len(tracks[fetch_track].matching_tracks) % 4 == 3:
                page_layout['col2']['item2x2'].update(Panel(""))
            elif len(tracks[fetch_track].matching_tracks) % 4 == 2:
                page_layout['col2']['item2x2'].update(Panel(""))
                page_layout['col2']['item1x2'].update(Panel(""))
            elif len(tracks[fetch_track].matching_tracks) % 4 == 1:
                page_layout['col2']['item2x2'].update(Panel(""))
                page_layout['col2']['item1x2'].update(Panel(""))
                page_layout['col1']['item2x1'].update(Panel(""))


        panel_page = Panel(page_layout, title=f"[bold green]Page {panel_page_index+1}[/bold green] of {total_pagination}")

        panel_pages.append(panel_page)


    main_layout = Layout()



    main_layout.split_row(
        Layout(name="fetched",ratio=1),
        Layout(name="local",ratio=2)
    )

    #Split fetched layout
    main_layout['fetched'].split_column(
        Layout(name="fetched_top"),
        Layout(name="fetched_bottom", ratio=3)
    )

    h = ((os.get_terminal_size().lines//3)*2 +1)//2
    # exit()

    playlist_str= ""

    playlist_start = fetch_track-h if fetch_track- h > 0 else 0
    playlist_end = fetch_track+h if fetch_track+h < len(tracks) else len(tracks)

    offset = fetch_track - h
    if offset < 0:
        playlist_end += abs(offset)


    for track in tracks[playlist_start:playlist_end]:
        color = track.display_color
        if track == tracks[fetch_track]:
            playlist_str += f"[black on {color}]{tracks.index(track)+1}: {track.name} - {track.artist}[/black on {color}]\n"
        else:
            playlist_str += f"[{color}]{tracks.index(track)+1}: {track.name} - {track.artist}[/{color}]\n"

    playlist_panel = Panel(playlist_str,title="Playlist")

    main_layout['fetched']['fetched_bottom'].update(playlist_panel)

    fetched_layout_panel_content = f"""[bold blue]Track Name[/bold blue]: [bold white]{fetch_track_name}[/bold white]
[bold blue]Artist Name[/bold blue]: [bold white]{fetch_track_artist}[/bold white]
[bold blue]Duration[/bold blue]: [bold white]{ms_to_min(fetch_track_duration)}[/bold white]
[bold blue]Spotify ID[/bold blue]: [bold green_yellow]{fetch_track_spotify_id}[/bold green_yellow]
    """
    fetched_layout_panel = Panel(fetched_layout_panel_content, title=f"[green bold]Fetched Track {fetch_track+1} of {len(tracks)}[/green bold]")

    main_layout['fetched']['fetched_top'].update(fetched_layout_panel)

    current_page = selection // 4
    main_layout['local'].update(panel_pages[current_page])


    main_panel = Panel(main_layout, title="[bold red]Spotiplex Matching Utility",height=os.get_terminal_size().lines -6)
    print(main_panel)

    



