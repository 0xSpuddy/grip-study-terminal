import time
import asyncio
from grip_strength_terminal.data_handler import log_data, read_data
from grip_strength_terminal.blockchain_interaction import GripStrengthReporter, GripStrengthData
from grip_strength_terminal.leaderboard import display_leaderboard
from grip_strength_terminal.spirit_animal import select_spirit_animal
from grip_strength_terminal.art import display_welcome_screen
from telliot_core.apps.core import RPCEndpoint
from chained_accounts import ChainedAccount
from telliot_feeds.feeds import CATALOG_FEEDS
from telliot_feeds.datafeed import DataFeed
from telliot_feeds.queries.grip_dyno_challenge_query import EthDenverTest
from grip_strength_terminal.blockchain_interaction import GripStrengthDataSource
import os
from rich.console import Console
from rich.table import Table
from rich import box

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

async def async_main():
    while True:
        display_welcome_screen()
        choice = input("Choose an option (1: Enter Data, 2: View Leaderboard): ")
        
        if choice == '1':
            # Collect user data
            data_set = input("Enter M/f data set (True/False): ")
            data_set = data_set.lower() if data_set else "true"  # Default to "true" if empty
            data_set = data_set == "true"  # Convert to boolean
            right_hand = int(input("Enter right hand strength (pounds): "))
            left_hand = int(input("Enter left hand strength (pounds): "))
            x_handle = input("Enter Twitter username: ")
            github_username = input("Enter GitHub username: ")
            hours_of_sleep = int(input("Enter hours of sleep: "))
            
            # Create GripStrengthData object
            grip_data_value = [
                data_set,
                right_hand,
                left_hand,
                x_handle,
                github_username,
                hours_of_sleep
            ]

            # Clear terminal and show confirmation
            clear_terminal()
            console = Console()
            
            table = Table(title="🏋️ Confirm Your Data 🏋️", box=box.ROUNDED)
            table.add_column("Field", style="cyan")
            table.add_column("Value", style="green")
            
            table.add_row("Dataset Type", "Male" if data_set else "Female")
            table.add_row("Right Hand", f"{right_hand} lbs")
            table.add_row("Left Hand", f"{left_hand} lbs")
            table.add_row("Twitter Handle", x_handle)
            table.add_row("GitHub Username", github_username)
            table.add_row("Hours of Sleep", f"{hours_of_sleep}")
            
            console.print(table)
            console.print("\n[yellow]Press Enter within 10 seconds to confirm and submit your data...[/yellow]")
            
            # Wait for confirmation with timeout
            try:
                await asyncio.wait_for(asyncio.get_event_loop().run_in_executor(None, input), timeout=10.0)
                clear_terminal()
            except asyncio.TimeoutError:
                console.print("[red]Timeout reached. Cancelling submission...[/red]")
                await asyncio.sleep(2)
                continue

            q = EthDenverTest(challengeType="grip_strength_dynamometer")
            encoded_value = q.value_type.encode(grip_data_value)
            # print(f"submitValue (bytes): 0x{encoded_value.hex()}")
            endpoint = RPCEndpoint(url="http://tellorlayer.com:1317", network="layertest-3")
            account = ChainedAccount("telliot_layer")
            account.unlock("asdf")
            datafeed = DataFeed(
                query=EthDenverTest(challengeType="grip_strength_dynamometer"),
                source=GripStrengthDataSource(encoded_value),
            )
            reporter = GripStrengthReporter([grip_data_value], endpoint, account)
            # Submit data to blockchain
            tip_tx = await reporter.tip_grip_query(datafeed=datafeed)
            # transaction_hash = tip_tx[0]['tx_response']['txhash']
            report_tx = await reporter.report_grip_query(datafeed=datafeed, grip_data=grip_data_value)
            report_tx_hash = report_tx[0]['tx_response']['txhash']
            # Log data using report transaction hash
            log_data(data_set, right_hand, left_hand, x_handle, github_username, hours_of_sleep, report_tx_hash)
            
            # Display spirit animal using tip transaction hash
            select_spirit_animal(report_tx_hash)
            print("looks like it worked")
            print(f"tip_tx: {tip_tx}")
            print(f"report_tx: {report_tx}")
            await asyncio.sleep(10)
        
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