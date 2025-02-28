import os
import hashlib
from rich.console import Console
from rich import box
from rich.panel import Panel
import ascii_magic
from PIL import Image
from .animal_engine import generate_and_convert_to_ascii
from grip_strength_terminal.animals import ANIMALS

# Get the directory of this file
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# Go up one level to the project root
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
IMAGES_DIR = os.path.join(PROJECT_ROOT, 'images')

console = Console()

# Define the selection lists
# ANIMALS = ['crab', 'clam', 'tortoise', 'cockatoo', 'jellyfish', 'pondo']
ANIMALS_LIST = ANIMALS
SEEDS = list(range(25, 50))  # Creates a list of integers from 11 to 49
ANIMAL_BACKGROUNDS = ['cityscape', 'beach', 'sunset', 'mountains']

# Default ASCII art in case no files are found
DEFAULT_ANIMAL = """
             _.-````'-,_
   _,.,_ ,-'`           `'-.,_
 /)     (\                   '``-.
((      ) )                      `
 \)    (_/                        )
  |       /)           '    ,'    / 
  `\    ^'            '     (    /  ))
    |      _/\ ,     /    ,,`\   (  "`
     \Y,   |  \  \  | ````| / \_ 
       `)_/    \  \  )    ( >  ( >
                \( \(     |/   |/
    mic & dwb  /_(/_(    /_(  /_(
"""

# def ensure_images_dir_exists():
#     # Create images directory if it doesn't exist
#     if not os.path.exists(IMAGES_DIR):
#         os.makedirs(IMAGES_DIR)
#         # Optionally create a default animal file
#         with open(os.path.join(IMAGES_DIR, 'cat.txt'), 'w') as f:
#             f.write(DEFAULT_ANIMAL)

def image_to_ascii(image_path, columns=140):
    """Convert an image file to ASCII art"""
    output = ascii_magic.AsciiArt.from_image(image_path)
    ascii_str = output.to_ascii(columns=columns)
    # Escape the ASCII art to prevent Rich from interpreting backslashes
    return f"```\n{ascii_str}\n```"

def get_random_selections(transaction_hash):
    """Use transaction hash to generate three random selections"""
    # Create three different hashes from the transaction hash
    hash1 = hashlib.sha256(f"{transaction_hash}-1".encode()).digest()
    hash2 = hashlib.sha256(f"{transaction_hash}-2".encode()).digest()
    hash3 = hashlib.sha256(f"{transaction_hash}-3".encode()).digest()
    
    # Convert each hash to an integer and use modulo to select from lists
    animal_index = int.from_bytes(hash1[:8], 'big') % len(ANIMALS_LIST)
    seed_index = int.from_bytes(hash2[:8], 'big') % len(SEEDS)
    background_index = int.from_bytes(hash3[:8], 'big') % len(ANIMAL_BACKGROUNDS)
    
    return (
        ANIMALS_LIST[animal_index],
        SEEDS[seed_index],
        ANIMAL_BACKGROUNDS[background_index]
    )

def select_spirit_animal(transaction_hash):
    # Get random selections based on transaction hash
    animal, seed, background = get_random_selections(transaction_hash)
    
    # Generate the prompt for the AI
    prompt = f"futuristic Pixelart of a anthropomorphic cyberpunk {animal} with large squeezing fists with background {background}, Macabre at night, Hard Light"
    
    # Generate the ASCII art and pass the transaction hash
    ascii_art = generate_and_convert_to_ascii(prompt, transaction_hash)
    print(ascii_art)
    
    # Create a formatted description of the spirit animal
    description = f"Animal: {animal.title()}\nBackground: {background.title()}\nSeed: {seed}"
    
    console.print(Panel(
        f"[bold cyan]In Exchange for your Grip Strength, the oracle has revealed a new spirit animal!:[/bold cyan]\n\n{description}",
        title="🐾 Spirit Animal Revealed 🐾",
        border_style="cyan",
        box=box.DOUBLE
    ))

    return animal
