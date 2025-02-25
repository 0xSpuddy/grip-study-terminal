import time
import asyncio
from grip_strength_terminal.data_handler import log_data, read_data
from grip_strength_terminal.blockchain_interaction import GripStrengthReporter, GripStrengthData
from grip_strength_terminal.leaderboard import display_leaderboard
from grip_strength_terminal.spirit_animal import select_spirit_animal
from grip_strength_terminal.art import display_welcome_screen
from grip_strength_terminal.discord_handler import send_to_discord
from telliot_core.apps.core import RPCEndpoint
from chained_accounts import ChainedAccount
from telliot_feeds.feeds import CATALOG_FEEDS
from telliot_feeds.datafeed import DataFeed
from telliot_feeds.queries.grip_dyno_challenge_query import EthDenverTester
from grip_strength_terminal.blockchain_interaction import GripStrengthDataSource
import os
from rich.console import Console
from rich.table import Table
from rich import box

# Get the directory of this file
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# Go up one level to the project root
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

async def async_main():
    while True:
        display_welcome_screen()
        choice = input("Choose an option (1: Enter Data, 2: View Leaderboard): ")
        
        if choice == '1' or choice == '':
            # Collect user data
            clear_terminal()
            print("""

▗▖  ▗▖▗▄▄▄▖▗▖  ▗▖ ▗▄▄▖     ▗▄▖ ▗▄▄▖     ▗▖ ▗▖ ▗▄▖ ▗▖  ▗▖▗▄▄▄▖▗▖  ▗▖ ▗▄▄▖
▐▛▚▞▜▌▐▌   ▐▛▚▖▐▌▐▌       ▐▌ ▐▌▐▌ ▐▌    ▐▌ ▐▌▐▌ ▐▌▐▛▚▞▜▌▐▌   ▐▛▚▖▐▌▐▌   
▐▌  ▐▌▐▛▀▀▘▐▌ ▝▜▌ ▝▀▚▖    ▐▌ ▐▌▐▛▀▚▖    ▐▌ ▐▌▐▌ ▐▌▐▌  ▐▌▐▛▀▀▘▐▌ ▝▜▌ ▝▀▚▖
▐▌  ▐▌▐▙▄▄▖▐▌  ▐▌▗▄▄▞▘    ▝▚▄▞▘▐▌ ▐▌    ▐▙█▟▌▝▚▄▞▘▐▌  ▐▌▐▙▄▄▖▐▌  ▐▌▗▄▄▞▘

                  """)
            data_set = input("Men's of Women's data set? (M/w): ").lower().strip()
            
            # Fuzzy matching for common variations
            male_options = ['m', 'male', 'man', '1', '']
            Womens_options = ['w', 'f', 'Womens', 'woman']
            
            while data_set not in male_options + Womens_options:
                print("Please enter 'M' for male or 'F' for Womens.")
                data_set = input("Enter M/f data set (M/f): ").lower().strip()
            
            data_set = data_set in male_options  # Convert to boolean (True for male, False for Womens)
            # 1
            # clear_terminal()
            print("""

▗▄▄▖ ▗▄▄▄▖ ▗▄▄▖▗▖ ▗▖▗▄▄▄▖    ▗▖ ▗▖ ▗▄▖ ▗▖  ▗▖▗▄▄▄     ▗▄▄▖ ▗▄▄▄▖ ▗▄▖ ▗▄▄▄ ▗▄▄▄▖▗▖  ▗▖ ▗▄▄▖
▐▌ ▐▌  █  ▐▌   ▐▌ ▐▌  █      ▐▌ ▐▌▐▌ ▐▌▐▛▚▖▐▌▐▌  █    ▐▌ ▐▌▐▌   ▐▌ ▐▌▐▌  █  █  ▐▛▚▖▐▌▐▌   
▐▛▀▚▖  █  ▐▌▝▜▌▐▛▀▜▌  █      ▐▛▀▜▌▐▛▀▜▌▐▌ ▝▜▌▐▌  █    ▐▛▀▚▖▐▛▀▀▘▐▛▀▜▌▐▌  █  █  ▐▌ ▝▜▌▐▌▝▜▌
▐▌ ▐▌▗▄█▄▖▝▚▄▞▘▐▌ ▐▌  █      ▐▌ ▐▌▐▌ ▐▌▐▌  ▐▌▐▙▄▄▀    ▐▌ ▐▌▐▙▄▄▖▐▌ ▐▌▐▙▄▄▀▗▄█▄▖▐▌  ▐▌▝▚▄▞▘
                                                                                          
            """)
            while True:
                try:
                    right_hand = float(input("Enter right hand strength (pounds): "))
                    if right_hand < 0:
                        print("Please enter a positive number.")
                        continue
                    break
                except ValueError:
                    print("Please enter a valid number.")
            print("""

▗▖   ▗▄▄▄▖▗▄▄▄▖▗▄▄▄▖    ▗▖ ▗▖ ▗▄▖ ▗▖  ▗▖▗▄▄▄     ▗▄▄▖ ▗▄▄▄▖ ▗▄▖ ▗▄▄▄ ▗▄▄▄▖▗▖  ▗▖ ▗▄▄▖
▐▌   ▐▌   ▐▌     █      ▐▌ ▐▌▐▌ ▐▌▐▛▚▖▐▌▐▌  █    ▐▌ ▐▌▐▌   ▐▌ ▐▌▐▌  █  █  ▐▛▚▖▐▌▐▌   
▐▌   ▐▛▀▀▘▐▛▀▀▘  █      ▐▛▀▜▌▐▛▀▜▌▐▌ ▝▜▌▐▌  █    ▐▛▀▚▖▐▛▀▀▘▐▛▀▜▌▐▌  █  █  ▐▌ ▝▜▌▐▌▝▜▌
▐▙▄▄▖▐▙▄▄▖▐▌     █      ▐▌ ▐▌▐▌ ▐▌▐▌  ▐▌▐▙▄▄▀    ▐▌ ▐▌▐▙▄▄▖▐▌ ▐▌▐▙▄▄▀▗▄█▄▖▝▚▄▄▖▐▌ ▐▌▐▌   
                                                                                     
            """)
            while True:
                try:
                    left_hand = float(input("Enter left hand strength (pounds): "))
                    if left_hand < 0:
                        print("Please enter a positive number.")
                        continue
                    break
                except ValueError:
                    print("Please enter a valid number.")
            print("""

 ▗▄▄▖ ▗▄▖  ▗▄▄▖▗▄▄▄▖ ▗▄▖ ▗▖    ▗▄▄▖    ▗▄▄▄▖ ▗▄▖ ▗▄▄▖      ▗▄▄▖▗▄▄▄▖▗▄▄▖ ▗▄▄▄▖▗▄▄▄▖▗▄▄▄▖     ▗▄▄▖▗▄▄▖ ▗▄▄▄▖▗▄▄▄ 
▐▌   ▐▌ ▐▌▐▌     █  ▐▌ ▐▌▐▌   ▐▌       ▐▌   ▐▌ ▐▌▐▌ ▐▌    ▐▌     █  ▐▌ ▐▌▐▌   ▐▌     █      ▐▌   ▐▌ ▐▌▐▌   ▐▌  █
 ▝▀▚▖▐▌ ▐▌▐▌     █  ▐▛▀▜▌▐▌    ▝▀▚▖    ▐▛▀▀▘▐▌ ▐▌▐▛▀▚▖     ▝▀▚▖  █  ▐▛▀▚▖▐▛▀▀▘▐▛▀▀▘  █      ▐▌   ▐▛▀▚▖▐▛▀▀▘▐▌  █
▗▄▄▞▘▝▚▄▞▘▝▚▄▄▖▗▄█▄▖▐▌ ▐▌▐▙▄▄▖▗▄▄▞▘    ▐▌   ▝▚▄▞▘▐▌ ▐▌    ▗▄▄▞▘  █  ▐▌ ▐▌▐▙▄▄▖▐▙▄▄▖  █      ▝▚▄▄▖▐▌ ▐▌▐▙▄▄▖▐▙▄▄▀
                                                                                     
            """)
            while True:
                x_handle = input("Social Media Handle 1 (X username?)): ").strip()
                if len(x_handle) > 100:
                    print("Handle must be less than 100 characters. Please try again.")
                    continue
                break

            while True:
                github_username = input("Social Media Handle 2 (GitHub username?)): ").strip()
                if len(github_username) > 100:
                    print("Handle must be less than 100 characters. Please try again.")
                    continue
                break
            print("""

 ▗▄▄▖▗▖   ▗▄▄▄▖▗▄▄▄▖▗▄▄▖     ▗▖ ▗▖ ▗▄▖ ▗▖  ▗▖▗▄▄▄ ▗▄▄▄▖ ▗▄▄▖ ▗▄▖ ▗▄▄▖ 
▐▌   ▐▌   ▐▌   ▐▌   ▐▌ ▐▌    ▐▌ ▐▌▐▌ ▐▌▐▛▚▖▐▌▐▌  █  █  ▐▌   ▐▌ ▐▌▐▌ ▐▌
 ▝▀▚▖▐▌   ▐▛▀▀▘▐▛▀▀▘▐▛▀▘     ▐▛▀▜▌▐▛▀▜▌▐▌ ▝▜▌▐▌  █  █  ▐▌   ▐▛▀▜▌▐▛▀▘ 
▗▄▄▞▘▐▙▄▄▖▐▙▄▄▖▐▙▄▄▖▐▌       ▐▌ ▐▌▐▌ ▐▌▐▌  ▐▌▐▙▄▄▀▗▄█▄▖▝▚▄▄▖▐▌ ▐▌▐▌   
                                                                                     
            """)
            while True:
                try:
                    hours_of_sleep = float(input("Enter hours of sleep (max 12 hours): "))
                    if hours_of_sleep < 0 or hours_of_sleep > 12:
                        print("Please enter a number between 0 and 12.")
                        continue
                    break
                except ValueError:
                    print("Please enter a valid number.")
            
            # Create GripStrengthData object
            grip_data_value = [
                bool(data_set),  # Ensure it's a proper boolean
                right_hand,
                left_hand,
                x_handle,
                github_username,
                hours_of_sleep
            ]

            # Clear terminal and show confirmation
            clear_terminal()
            console = Console()
            
            # Get terminal height and calculate padding
            terminal_height = os.get_terminal_size().lines
            padding_top = (terminal_height - 12) // 2  # 12 is approximate table height
            
            # Add vertical padding
            console.print("\n" * padding_top)
            
            table = Table(title="[green]🏋️ Confirm Your Data 🏋️[/green]", box=box.ROUNDED)
            table.add_column("Field", style="green")
            table.add_column("Value", style="green")
            
            table.add_row("Dataset Type", "Male" if data_set else "Womens")
            table.add_row("Right Hand", f"{right_hand} lbs")
            table.add_row("Left Hand", f"{left_hand} lbs")
            table.add_row("X (or other social media) Handle", x_handle)
            table.add_row("GitHub Username if applicable (can be anything)", github_username)
            table.add_row("Hours of Sleep", f"{hours_of_sleep}")
            
            console.print(table, justify="center")
            console.print("\n[green]Press Enter within 10 seconds to confirm and submit your data...[/green]", justify="center")
            
            # Wait for confirmation with timeout
            try:
                await asyncio.wait_for(asyncio.get_event_loop().run_in_executor(None, input), timeout=10.0)
                clear_terminal()
            except asyncio.TimeoutError:
                console.print("[red]Timeout reached. Cancelling submission...[/red]", justify="center")
                await asyncio.sleep(2)
                continue

            q = EthDenverTester(challengeType="grip_strength_dynamometer")
            encoded_value = q.value_type.encode(grip_data_value)
            # print(f"submitValue (bytes): 0x{encoded_value.hex()}")
            endpoint = RPCEndpoint(url="http://tellorlayer.com:1317", network="layertest-3")
            account = ChainedAccount("telliot_layer")
            account.unlock("asdf")
            datafeed = DataFeed(
                query=EthDenverTester(challengeType="grip_strength_dynamometer"),
                source=GripStrengthDataSource(encoded_value),
            )
            reporter = GripStrengthReporter([grip_data_value], endpoint, account)
            # Submit data to blockchain
            tip_tx = await reporter.tip_grip_query(datafeed=datafeed)
            # transaction_hash = tip_tx[0]['tx_response']['txhash']
            report_tx = await reporter.report_grip_query(datafeed=datafeed, grip_data=grip_data_value)
            report_tx_hash = report_tx[0]['tx_response']['txhash']
            if not report_tx_hash:
                print("Something went wrong with the report. Please try again.")
                await asyncio.sleep(15)
                continue
            # Log data using report transaction hash
            log_data(data_set, right_hand, left_hand, x_handle, github_username, hours_of_sleep, report_tx_hash)
            
            # Display spirit animal using tip transaction hash
            if report_tx_hash:
                spirit_animal = select_spirit_animal(report_tx_hash)
                html_path = os.path.join(PROJECT_ROOT, 'generated_art', 'html', f"{report_tx_hash[:10]}.html")
                print("\nTransaction successful!")
                print(f"Transaction hash: {report_tx_hash}")
                await send_to_discord(grip_data_value, report_tx_hash, spirit_animal, html_path)
            else:
                print("Something went wrong On-Chain. Please try again. Maybe find Spuddy.")

            await asyncio.sleep(15)
        
        elif choice == '2':
            display_leaderboard()
        
        else:
            print("Invalid choice. Please try again.")

def main():
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    main() 