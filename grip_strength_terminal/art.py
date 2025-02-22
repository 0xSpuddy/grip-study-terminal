import pyfiglet
from termcolor import colored
from rich.console import Console
from rich.panel import Panel
import os

console = Console()

def display_welcome_screen():
    # Clear the terminal screen
    os.system('cls' if os.name == 'nt' else 'clear')  # 'cls' for Windows, 'clear' for Unix/Linux/MacOS
    
    # Create a fancy title
    title = pyfiglet.figlet_format("TELLOR LONGEVITY CHALLENGE", font="standard")
    colored_title = '\n'.join([colored(line, "green", attrs=["bold"]) for line in title.split('\n')])
    title = """

  ______     ____              __                                      
 /_  __/__  / / /___  _____   / /   ____ ___  _____  _____             
  / / / _ \/ / / __ \/ ___/  / /   / __ `/ / / / _ \/ ___/             
 / / /  __/ / / /_/ / /     / /___/ /_/ / /_/ /  __/ /                 
/_/  \___/_/_/\____/_/     /_____/\__,_/\__, /\___/_/    __  __        
   ____ ______(_)___     _____/ /______/____/___  ____ _/ /_/ /_       
  / __ `/ ___/ / __ \   / ___/ __/ ___/ _ \/ __ \/ __ `/ __/ __ \      
 / /_/ / /  / / /_/ /  (__  ) /_/ /  /  __/ / / / /_/ / /_/ / / /      
 \__, /_/  /_/ .___/  /____/\__/_/   \___/_/ /_/\__, /\__/_/ /_/       
/____/      /_/         __     __              /____/  _             __
   (_)___  ____  __  __/ /_   / /____  _________ ___  (_)___  ____ _/ /
  / / __ \/ __ \/ / / / __/  / __/ _ \/ ___/ __ `__ \/ / __ \/ __ `/ / 
 / / / / / /_/ / /_/ / /_   / /_/  __/ /  / / / / / / / / / / /_/ / /  
/_/_/ /_/ .___/\__,_/\__/   \__/\___/_/  /_/ /_/ /_/_/_/ /_/\__,_/_/   
       /_/                                                             

    """

    colored_title = f"[bold green]{title}[/bold green]"

    # Create menu options with boxing
    menu = """
    INPUT YOUR GRIP STRENGTH RESULTS HERE! 
    ALL INPUTS ARE OPTIONAL.
    NO NEED TO GET OUT YOUR PHONE 😉

    [1] 💪 Report Your Grip Strength to Tellor Layer
    [2] 🏆 View the Leaderboard
    """
    
    colored_menu = f"[bold green]{menu}[/bold green]"

    console.print(Panel(colored_title, title="WELCOME TO THE", border_style="cyan"))
    console.print(Panel(colored_menu, title="OPTIONS", border_style="green"))
    
def display_loading_animation():
    with console.status("[bold green]Processing your submission...") as status:
        yield
        
def display_success_message(tx_hash):
    console.print(Panel(
        f"[bold green]Success![/bold green]\nTransaction Hash: {tx_hash}",
        title="Transaction Complete",
        border_style="green"
    )) 