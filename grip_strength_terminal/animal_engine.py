import io
import os
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from PIL import Image
import ascii_magic
import dotenv
import time

# Get the directory of this file
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# Go up one level to the project root
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

dotenv.load_dotenv()

# Initialize the Stable Diffusion client
# You'll need to get an API key from DreamStudio
stability_api = client.StabilityInference(
    key=os.getenv('STABILITY_KEY'),  # Get API key from environment variable
    verbose=True,
)

def generate_and_convert_to_ascii(prompt, tx_hash=None):
    """
    Generate an image from a prompt and convert it to ASCII art
    
    Args:
        prompt (str): The text prompt for Stable Diffusion
        tx_hash (str): Transaction hash to use for file naming
    """
    # Create output directories if they don't exist
    output_dir = os.path.join(PROJECT_ROOT, 'generated_art')
    html_dir = os.path.join(output_dir, 'html')
    png_dir = os.path.join(output_dir, 'png')
    
    for directory in [output_dir, html_dir, png_dir]:
        if not os.path.exists(directory):
            os.makedirs(directory)

    # Generate base filename from transaction hash or timestamp
    if tx_hash:
        base_filename = tx_hash[:10]  # First 10 characters of hash
    else:
        base_filename = str(int(time.time()))

    # Generate image using Stable Diffusion
    answers = stability_api.generate(
        prompt=prompt,
        seed=0,
        steps=30,
        cfg_scale=8.0,
        width=512,
        height=512,
        samples=1,
    )

    # Get the generated image
    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.type == generation.ARTIFACT_IMAGE:
                # Convert bytes to PIL Image
                img = Image.open(io.BytesIO(artifact.binary))
                
                # Convert to ASCII art
                ascii_art = ascii_magic.from_pillow_image(img)
                
                # Print the ASCII art
                ascii_art.to_terminal(columns=120)
                
                # Save the ASCII art to HTML file
                html_path = os.path.join(html_dir, f"{base_filename}.html")
                ascii_art.to_html_file(html_path)
                
                # Save the original image
                png_path = os.path.join(png_dir, f"{base_filename}.png")
                img.save(png_path)
                
                return ascii_art

if __name__ == "__main__":
    # Example usage
    prompt = input("Enter your Stable Diffusion prompt: ")
    generate_and_convert_to_ascii(prompt)
