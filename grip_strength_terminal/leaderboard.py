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
    # Calculate total grip strength and sort
    leaderboard = sorted(data, key=lambda x: int(x[1]) + int(x[2]), reverse=True)
    
    table = Table(title="🏆 Grip Strength Leaderboard 🏆")
    
    table.add_column("Rank", style="cyan", no_wrap=True)
    table.add_column("Twitter", style="green")
    table.add_column("GitHub", style="blue")
    table.add_column("Total Strength", justify="right", style="magenta")
    table.add_column("Right Hand", justify="right")
    table.add_column("Left Hand", justify="right")
    table.add_column("Gender", justify="center")
    
    for i, entry in enumerate(leaderboard, 1):
        m_f = "M" if entry[0].lower() == "true" else "F"
        total_strength = int(entry[1]) + int(entry[2])
        
        table.add_row(
            f"#{i}",
            entry[3],  # Twitter
            entry[4],  # GitHub
            str(total_strength),
            entry[1],  # Right hand
            entry[2],  # Left hand
            m_f
        )
    
    console.print(table)
    time.sleep(10)  # Display for 10 seconds
    clear_terminal()  # Clear before returning to welcome screen 