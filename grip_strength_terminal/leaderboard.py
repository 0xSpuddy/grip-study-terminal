import time
import os
from grip_strength_terminal.data_handler import read_data
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def clear_terminal():
    # Clear screen command for different operating systems
    os.system('cls' if os.name == 'nt' else 'clear')

def display_leaderboard():
    clear_terminal()
    
    data = read_data()
    # Convert string values to floats for sorting and display
    leaderboard = sorted(data, key=lambda x: float(x[1]) + float(x[2]), reverse=True)
    
    table = Table(title="🏆 Grip Strength Leaderboard 🏆")
    
    table.add_column("Rank", style="cyan", no_wrap=True)
    table.add_column("Twitter", style="green")
    table.add_column("GitHub", style="blue")
    table.add_column("Total Strength", justify="right", style="magenta")
    table.add_column("Right Hand", justify="right")
    table.add_column("Left Hand", justify="right")
    table.add_column("Gender", justify="center")
    
    for i, entry in enumerate(leaderboard, 1):
        data_set = "M" if entry[0].lower() == "true" else "F"
        # Convert Wei-like values back to human-readable floats
        right_hand = float(entry[1]) / (10 ** 18)
        left_hand = float(entry[2]) / (10 ** 18)
        total_strength = right_hand + left_hand
        
        table.add_row(
            f"#{i}",
            entry[3],  # Twitter
            entry[4],  # GitHub
            f"{total_strength:.2f}",  # Format to 2 decimal places
            f"{right_hand:.2f}",  # Format to 2 decimal places
            f"{left_hand:.2f}",  # Format to 2 decimal places
            data_set
        )
    
    console.print(table)
    time.sleep(10)  # Display for 10 seconds
    clear_terminal()  # Clear before returning to welcome screen 