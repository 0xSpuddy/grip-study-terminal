import io
import os
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from PIL import Image
import ascii_magic
import dotenv

dotenv.load_dotenv()

# Initialize the Stable Diffusion client
# You'll need to get an API key from DreamStudio
stability_api = client.StabilityInference(
    key=os.getenv('STABILITY_KEY'),  # Get API key from environment variable
    verbose=True,
)

def generate_and_convert_to_ascii(prompt, width=120):
    """
    Generate an image from a prompt and convert it to ASCII art
    
    Args:
        prompt (str): The text prompt for Stable Diffusion
        negative_prompt (str): The negative prompt for things to avoid in the image
        width (int): Width of the ASCII art output (in characters)
    """
    # Generate image using Stable Diffusion
    answers = stability_api.generate(
        prompt=prompt,
        seed=0,  # Change this for different results
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
                ascii_art.to_terminal(columns=width)
                
                # Optionally save the ASCII art to a file
                ascii_art.to_html_file(f"ascii_art_{prompt[:30]}.html")
                
                # Save the original image
                img.save(f"original_{prompt[:30]}.png")

if __name__ == "__main__":
    # Example usage
    prompt = input("Enter your Stable Diffusion prompt: ")
    generate_and_convert_to_ascii(prompt)
