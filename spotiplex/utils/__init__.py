import os

from rich import print
from rich.layout import Layout
from rich.panel import Panel


logo_str = """
                                                                                             
 ad88888ba                                     88               88                           
d8"     "8b                             ,d     ""               88                           
Y8,                                     88                      88                           
`Y8aaaaa,    8b,dPPYba,    ,adPPYba,  MM88MMM  88  8b,dPPYba,   88   ,adPPYba,  8b,     ,d8  
  `'''''8b,  88P'    "8a  a8"     "8a   88     88  88P'    "8a  88  a8P_____88   `Y8, ,8P'   
        `8b  88       d8  8b       d8   88     88  88       d8  88  8PP"""""""     )888(     
Y8a     a8P  88b,   ,a8"  "8a,   ,a8"   88,    88  88b,   ,a8"  88  "8b,   ,aa   ,d8" "8b,   
 "Y88888P"   88`YbbdP"'    `"YbbdP"'    "Y888  88  88`YbbdP"'   88   `"Ybbd8"'  8P'     `Y8  
             88                                    88                                        
             88                                    88                                        
"""

def gen_main_menu_str(selected):
	items = ["Import playlist", "Change config", "Exit"]

	main_menu_str = """"""

	for i in range(len(items)):
		if i == selected:
			main_menu_str += f"""[bold white on blue]{items[i]}[/bold white on blue]\n"""
		else:
			main_menu_str += f"""{items[i]}\n"""
		
	return main_menu_str


class Menu:
	def __init__(self, title, items, selected=0):
		self.title = title
		self.items = items
		self.selected = selected

	def build_menu_str(self):
		menu_str = """"""

		for i in range(len(self.items)):
			if i == self.selected:
				menu_str += f"""[bold white on blue]{self.items[i]}[/bold white on blue]\n"""
			else:
				menu_str += f"""[bold blue on white]{self.items[i]}[/bold blue on white]\n"""

		return menu_str

	def build():
		# BUILD MENU
		# clear the console
		os.system("cls" if os.name == "nt" else "clear")

		menu_layout = Layout()

		menu_panel = Panel(self.build_menu_str(), title=self.title)

		menu_layout.split_column(
			menu_panel
		)

		menu_layout.update(menu_panel)

		return menu_layout

	def get_selection(self):
		# generate a menu selector using rich layout and getkey
		# returns the index of the selected item

		# array: list of items to select from

		# BUILD MENU
		# clear the console
		os.system("cls" if os.name == "nt" else "clear")

		menu_layout = Layout()

		menu_panel = Panel(self.build_menu_str(), title=self.title)

		menu_layout.split_column(
			menu_panel
		)

		menu_layout["menu"].update(gen_main_menu_str(0))

		print(menu_layout)

		# GET INPUT
		# get input from user and update the menu
		# if the user presses enter, return the index of the selected item
		# if the user presses up/down, update the menu
		# if the user presses q, exit the program

		self.selected = 0

		while True:
			key = menu_layout.getkey()

			if key == "KEY_UP":
				selected -= 1
				if selected < 0:
					selected = len(self.items) - 1

				menu_layout["menu"].update(gen_main_menu_str(selected))

			elif key == "KEY_DOWN":
				selected += 1
				if selected > len(self.items) - 1:
					selected = 0

				menu_layout["menu"].update(gen_main_menu_str(selected))

			elif key == "KEY_ENTER":
				return selected

			elif key == "q":
				sys.exit()

			else:
				pass

			print(menu_layout)
