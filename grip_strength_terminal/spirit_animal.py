import os
import hashlib
from rich.console import Console
from rich import box
from rich.panel import Panel

# Get the directory of this file
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# Go up one level to the project root
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
IMAGES_DIR = os.path.join(PROJECT_ROOT, 'images')

console = Console()

# Default ASCII art in case no files are found
DEFAULT_ANIMAL = """
             _.-````'-,_
   _,.,_ ,-'`           `'-.,_
 /)     (\                   '``-.
((      ) )                      `\
 \)    (_/                        )\
  |       /)           '    ,'    / \
  `\    ^'            '     (    /  ))
    |      _/\ ,     /    ,,`\   (  "`
     \Y,   |  \  \  | ````| / \_ \
       `)_/    \  \  )    ( >  ( >
                \( \(     |/   |/
    mic & dwb  /_(/_(    /_(  /_(
"""

def ensure_images_dir_exists():
    # Create images directory if it doesn't exist
    if not os.path.exists(IMAGES_DIR):
        os.makedirs(IMAGES_DIR)
        # Optionally create a default animal file
        with open(os.path.join(IMAGES_DIR, 'cat.txt'), 'w') as f:
            f.write(DEFAULT_ANIMAL)

def select_spirit_animal(transaction_hash):
    ensure_images_dir_exists()
    
    # Get list of available animal files
    animal_files = [f for f in os.listdir(IMAGES_DIR) if f.endswith('.txt')]
    
    # If no animal files found, use default
    if not animal_files:
        console.print(Panel(
            f"[bold cyan]Your Spirit Animal is: Cat[/bold cyan]\n\n{DEFAULT_ANIMAL}",
            title="🐾 Spirit Animal Revealed 🐾",
            border_style="cyan",
            box=box.DOUBLE
        ))
        return "Bufficorn (error lmao)"
    
    # Use the first 8 bytes of the transaction hash to select an animal
    hash_bytes = hashlib.sha256(transaction_hash.encode()).digest()
    index = int.from_bytes(hash_bytes[:8], 'big') % len(animal_files)
    chosen_animal = animal_files[index]
    
    # Get animal name from filename (assuming format: "animal_name.txt")
    animal_name = chosen_animal.replace('.txt', '').replace('_', ' ').title()
    
    # Read and display the ASCII art
    with open(os.path.join(IMAGES_DIR, chosen_animal), 'r') as file:
        art = file.read()
        
    console.print(Panel(
        f"[bold cyan]Your Spirit Animal is: {animal_name}[/bold cyan]\n\n{art}",
        title="🐾 Spirit Animal Revealed 🐾",
        border_style="cyan",
        box=box.DOUBLE
    ))
    
    return animal_name
