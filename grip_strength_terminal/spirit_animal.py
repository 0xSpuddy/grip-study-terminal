import os
import hashlib
import json
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
ANIMAL_TRACKING_FILE = os.path.join(PROJECT_ROOT, 'data', 'revealed_animals.json')

console = Console()

# Define the selection lists
# ANIMALS = ['crab', 'clam', 'tortoise', 'cockatoo', 'jellyfish', 'pondo']
ANIMALS_LIST = ANIMALS
SEEDS = list(range(25, 50))  # Creates a list of integers from 11 to 49
ANIMAL_BACKGROUNDS = ['cityscape', 'sunset', 'mountains']


def image_to_ascii(image_path, columns=150):
    """Convert an image file to ASCII art"""
    output = ascii_magic.AsciiArt.from_image(image_path)
    ascii_str = output.to_ascii(columns=columns)
    # Escape the ASCII art to prevent Rich from interpreting backslashes
    return f"```\n{ascii_str}\n```"

def load_animal_tracking():
    """Load the animal tracking data from JSON file"""
    if not os.path.exists(ANIMAL_TRACKING_FILE):
        return {'revealed': {}, 'available': ANIMALS.copy()}
    
    with open(ANIMAL_TRACKING_FILE, 'r') as f:
        data = json.load(f)
        # If all animals have been revealed, reset the tracking
        if not data['available']:
            data = {'revealed': {}, 'available': ANIMALS.copy()}
    return data

def save_animal_tracking(data):
    """Save the animal tracking data to JSON file"""
    os.makedirs(os.path.dirname(ANIMAL_TRACKING_FILE), exist_ok=True)
    with open(ANIMAL_TRACKING_FILE, 'w') as f:
        json.dump(data, f)

def get_random_selections(transaction_hash):
    """Get random selections based on transaction hash"""
    tracking_data = load_animal_tracking()
    available_animals = tracking_data['available']
    
    # If no animals are available, reset the tracking
    if not available_animals:
        tracking_data = {'revealed': {}, 'available': ANIMALS.copy()}
        available_animals = tracking_data['available']
    
    # Use transaction hash to select a random animal
    hash_bytes = bytes.fromhex(transaction_hash[2:])  # Remove '0x' prefix
    hash_int = int.from_bytes(hash_bytes, byteorder='big')
    animal_index = hash_int % len(available_animals)
    animal = available_animals.pop(animal_index)
    
    # Mark the animal as revealed with its transaction hash
    tracking_data['revealed'][transaction_hash] = animal
    save_animal_tracking(tracking_data)
    
    # Generate other random selections
    seed = str(hash_int)[-8:]
    background_index = (hash_int // len(ANIMALS)) % len(ANIMAL_BACKGROUNDS)
    background = ANIMAL_BACKGROUNDS[background_index]
    
    return animal, seed, background

def select_spirit_animal(transaction_hash):
    """Select and display a spirit animal"""
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
