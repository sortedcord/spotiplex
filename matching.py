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

def build(tracks, selection, fetch_track):
    os.system('cls' if os.name == 'nt' else 'clear')


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

                panel = Panel(f"""[bold blue]Track Name:[/bold blue] [bold white]{data.title}[/bold white] 
[bold blue]Artist[/bold blue]: [bold white]{data.artist().title}[/bold white]
[bold blue]Duration[/bold blue]: [bold white]{ms_to_min(data.duration)}[/bold white]""",title="[yellow bold]Track {}[/yellow bold]".format(build_item+1)+f"{'[bold green] [SELECTED][/bold green]' if build_item == selection else ''}",style="bold green" if build_item == selection else "") # type: ignore 
                page_layout[layout_match[str(i)]].update(panel)
                build_item += 1
                i += 1
        except IndexError:
            pass

        panel_page = Panel(page_layout, title="[bold green]Page {}[/bold green]".format(panel_page_index+1))

        panel_pages.append(panel_page)




    # print(main_layout)


    main_layout = Layout()
    # Set the height of the layout as 120


    main_layout.split_column(
        Layout(name="matching",ratio=3),
        Layout(name="track_control",size=7,ratio=1)
    )

    main_layout['matching'].split_row(
        Layout(name="fetched",ratio=1),
        Layout(name="local",ratio=2)
    )

    fetched_layout_panel_content = f"""[bold blue]Track Name[/bold blue]: [bold white]{fetch_track_name}[/bold white]
[bold blue]Artist Name[/bold blue]: [bold white]{fetch_track_artist}[/bold white]
[bold blue]Duration[/bold blue]: [bold white]{ms_to_min(fetch_track_duration)}[/bold white]
[bold blue]Spotify ID[/bold blue]: [bold green_yellow]{fetch_track_spotify_id}[/bold green_yellow]
    """
    fetched_layout_panel = Panel(fetched_layout_panel_content, title="[green bold]Fetched Track")

    main_layout['matching']['fetched'].update(fetched_layout_panel)

    current_page = selection // 4
    main_layout['matching']['local'].update(panel_pages[current_page])

    main_layout['track_control'].split_row(
        Layout(name="previous"),
        Layout(name="next")
    )

    previous_panel = Panel("[bold blue]Previous Track[/bold blue]")
    next_panel = Panel("[bold blue]Next Track[/bold blue]")

    main_layout['track_control']['previous'].update(previous_panel)
    main_layout['track_control']['next'].update(next_panel)


    main_panel = Panel(main_layout, title="[bold red]Spotiplex Matching Utility",height=os.get_terminal_size().lines -6)
    print(main_panel)

    keymaps = {
        "r": "Next Track",
        "e": "Previous Track",
        "p": "Previous Page",
        "n": "Next Page",
        "Enter": "Confirm Selection",
        "q / ESC": "Quit",
        "Arrows": "Change Selection",
        "a": "Add local track"
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



