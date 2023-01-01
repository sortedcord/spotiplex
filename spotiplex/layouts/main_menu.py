from rich import print
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel

from utils import logo_str, gen_main_menu_str

from getkey import getkey, keys

import sys

def main_menu_layout(selected_item, expand_menu=False):
        layout = Layout(size=5)

        layout.split_column(
            Layout(name="logo"),
            Layout(name="layout_main")
        )

        layout['layout_main'].split_row(
            Layout(name="info", ratio=5),
            Layout(name="main_menu", ratio=1),
        )

        if expand_menu:
            layout['layout_main']['main_menu'].ratio = 20


        info_panel = Panel("Info Panel", title="Info")

        selected = selected_item

        main_menu_panel = Panel(gen_main_menu_str(selected), title="Main Menu")

        layout['layout_main']["info"].update(info_panel)
        layout['layout_main']["main_menu"].update(main_menu_panel)

        # Set the max size of layout to be 20% of the terminal
        layout.size = 20

        layout['logo'].update(Panel(logo_str))

        return layout
        

def main():

    # ----
    expand_menu = False


    selected_item = 0
    with Live(main_menu_layout(selected_item, expand_menu=expand_menu), refresh_per_second=2) as live:
        while True:
            key = getkey()
            if key == keys.UP:
                selected_item -= 1
            elif key == keys.DOWN:
                selected_item += 1
            elif key == keys.ESC:
                sys.exit()
            
            if selected_item < 0:
                selected_item = 0
            elif selected_item > 2:
                selected_item = 2

            if key == keys.ENTER:
                if selected_item == 0:
                    # Enter playlist
                    return selected_item
                elif selected_item == 1:
                    return selected_item
                    pass
                elif selected_item == 2:
                    sys.exit()

            live.update(main_menu_layout(selected_item, expand_menu=expand_menu))    