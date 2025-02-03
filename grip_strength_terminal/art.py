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
    # title = pyfiglet.figlet_format("TELLOR LONGEVITY CHALLENGE", font="standard")
    # colored_title = '\n'.join([colored(line, "green", attrs=["bold"]) for line in title.split('\n')])
    title = """
    ______)                    _                               )   ___                            
   (, /     /) /)          ___/__)                ,           (__/_____) /)     /) /)             
     /   _ // // ____     (, /   ____  _   _ _ _   _/_          /       (/  _  // //  _ __  _   _ 
  ) /  _(/(/_(/_(_/ (_      /   (_)/ ((_/_(/_(/__(_(__(_/_     /        / )(_((/_(/__(/_/ ((_/_(/_
 (_/                       (_____    .-/             .-/      (______)                    .-/     
                                  ) (_/             (_/                                  (_/      
    """

    colored_title = '\n'.join([colored(line, "green", attrs=["bold"]) for line in title.split('\n')])

    # Create menu options with boxing
    menu = """
    INPUT YOUR GRIP STRENGTH RESULTS HERE! 
    ALL INPUTS ARE OPTIONAL.
    NO NEED TO GET OUT YOUR PHONE 😉

    [1] 💪 Enter Your Grip Strength
    [2] 🏆 View Leaderboard
    """
    
    colored_menu = '\n'.join([colored(line, "green", attrs=["bold"]) for line in menu.split('\n')])

    console.print(Panel(colored_title, title="Welcome!", border_style="cyan"))
    console.print(Panel(colored_menu, title="Menu Options", border_style="green"))
    
def display_loading_animation():
    with console.status("[bold green]Processing your submission...") as status:
        yield
        
def display_success_message(tx_hash):
    console.print(Panel(
        f"[bold green]Success![/bold green]\nTransaction Hash: {tx_hash}",
        title="Transaction Complete",
        border_style="green"
    )) 