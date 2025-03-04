import pyfiglet
from termcolor import colored
from rich.console import Console
from rich.panel import Panel
import os

console = Console()

def display_welcome_screen():
    # Clear the terminal screen
    # os.system('cls' if os.name == 'nt' else 'clear')  # 'cls' for Windows, 'clear' for Unix/Linux/MacOS
    
    # Create a fancy title
    title = pyfiglet.figlet_format("TELLOR LONGEVITY CHALLENGE", font="standard")
    colored_title = '\n'.join([colored(line, "green", attrs=["bold"]) for line in title.split('\n')])
    title = """

         ███████████          ████  ████                     
        ░█░░░███░░░█         ░░███ ░░███                     
        ░   ░███  ░   ██████  ░███  ░███   ██████  ████████   
            ░███     ███░░███ ░███  ░███  ███░░███░░███░░███   
            ░███    ░███████  ░███  ░███ ░███ ░███ ░███ ░░░   
            ░███    ░███░░░   ░███  ░███ ░███ ░███ ░███        
            █████   ░░██████  █████ █████░░██████  █████      
           ░░░░░     ░░░░░░  ░░░░░ ░░░░░  ░░░░░░  ░░░░░       
                                                        
           ____ ____  ___ ____    ____ _____ ____  _____ _   _  ____ _____ _   _  
          / ___|  _ \|_ _|  _ \  / ___|_   _|  _ \| ____| \ | |/ ___|_   _| | | | 
         | |  _| |_) || || |_) | \___ \ | | | |_) |  _| |  \| | |  _  | | | |_| | 
         | |_| |  _ < | ||  __/   ___) || | |  _ <| |___| |\  | |_| | | | |  _  | 
          \____|_| \_\___|_|     |____/ |_| |_| \_\_____|_| \_|\____| |_| |_| |_| 
                                                                          
          ___ _   _ ____  _   _ _____   _____ _____ ____  __  __ ___ _   _    _    _     
         |_ _| \ | |  _ \| | | |_   _| |_   _| ____|  _ \|  \/  |_ _| \ | |  / \  | |    
          | ||  \| | |_) | | | | | |     | | |  _| | |_) | |\/| || ||  \| | / _ \ | |    
          | || |\  |  __/| |_| | | |     | | | |___|  _ <| |  | || || |\  |/ ___ \| |___ 
         |___|_| \_|_|    \___/  |_|     |_| |_____|_| \_\_|  |_|___|_| \_/_/   \_\_____|                           

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