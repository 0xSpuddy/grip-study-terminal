import os
import aiohttp
from dotenv import load_dotenv
import json

load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

async def send_to_discord(grip_data, tx_hash, spirit_animal, html_path):
    """
    Send grip strength data and spirit animal to Discord.
    
    Args:
        grip_data: List containing [is_male, right_hand, left_hand, x_handle, github_handle, sleep_hours]
        tx_hash: Transaction hash from the blockchain
        spirit_animal: Spirit animal name
        html_path: Path to the spirit animal HTML file
    """
    if not DISCORD_WEBHOOK_URL:
        print("Discord webhook URL not found in environment variables")
        return

    # Extract data
    dataset_type = "Men's" if grip_data[0] else "Women's"
    right_hand = grip_data[1]
    left_hand = grip_data[2]
    x_handle = grip_data[3]
    github_handle = grip_data[4]
    sleep_hours = grip_data[5]

    # Create message
    message = {
        "embeds": [{
            "title": "🏋️ New Grip Strength Submission! 🏋️",
            "color": 0x00ff00,
            "fields": [
                {"name": "Dataset", "value": dataset_type, "inline": True},
                {"name": "Right Hand", "value": f"{right_hand} lbs", "inline": True},
                {"name": "Left Hand", "value": f"{left_hand} lbs", "inline": True},
                {"name": "X Handle", "value": x_handle, "inline": True},
                {"name": "GitHub Handle", "value": github_handle, "inline": True},
                {"name": "Hours of Sleep", "value": f"{sleep_hours}", "inline": True},
                {"name": "Spirit Animal", "value": spirit_animal, "inline": False},
                {"name": "Transaction Hash", "value": f"`{tx_hash}`", "inline": False},
            ],
            "footer": {
                "text": "ETHDenver 2024 Grip Strength Challenge"
            }
        }]
    }

    try:
        # Read the file content first
        with open(html_path, 'rb') as f:
            file_content = f.read()

        async with aiohttp.ClientSession() as session:
            # Create the form data with the file content
            file_data = aiohttp.FormData()
            file_data.add_field('file', file_content, filename='spirit_animal.html')
            file_data.add_field('payload_json', json.dumps(message))

            # Send both the message and file
            async with session.post(DISCORD_WEBHOOK_URL, data=file_data) as response:
                if response.status == 204:
                    print("Successfully sent data to Discord!")
                else:
                    print(f"Failed to send data to Discord. Status: {response.status}")
    except Exception as e:
        print(f"Error sending to Discord: {e}") 