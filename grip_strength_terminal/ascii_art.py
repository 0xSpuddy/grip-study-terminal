import pyfiglet
from termcolor import colored
from rich.console import Console
from rich.panel import Panel

console = Console()

def display_welcome_screen():
    # Create a fancy title
    title = pyfiglet.figlet_format("GRIP STRENGTH", font="big")
    colored_title = colored(title, "cyan", attrs=["bold"])
    
    # Create menu options with boxing
    menu = """
    [1] 💪 Enter Your Grip Strength
    [2] 🏆 View Leaderboard
    """
    
    console.print(Panel(colored_title, title="Welcome!", border_style="cyan"))
    console.print(Panel(menu, title="Menu Options", border_style="green"))
    
def display_loading_animation():
    with console.status("[bold green]Processing your submission...") as status:
        yield
        
def display_success_message(tx_hash):
    console.print(Panel(
        f"[bold green]Success![/bold green]\nTransaction Hash: {tx_hash}",
        title="Transaction Complete",
        border_style="green"
    )) 