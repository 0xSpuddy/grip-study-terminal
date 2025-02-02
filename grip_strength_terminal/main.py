import time
from grip_strength_terminal.data_handler import log_data, read_data
from grip_strength_terminal.blockchain_interaction import submit_data
from grip_strength_terminal.leaderboard import display_leaderboard
from grip_strength_terminal.spirit_animal import select_spirit_animal
from grip_strength_terminal.ascii_art import display_welcome_screen

def main():
    while True:
        display_welcome_screen()
        choice = input("Choose an option (1: Enter Data, 2: View Leaderboard): ")
        
        if choice == '1':
            # Collect user data
            m_f = input("Enter m/f data set (True/False): ")
            right_hand = int(input("Enter right hand strength (pounds): "))
            left_hand = int(input("Enter left hand strength (pounds): "))
            twitter = input("Enter Twitter username: ")
            github = input("Enter GitHub username: ")
            sleep_hours = int(input("Enter hours of sleep: "))
            
            # Submit data to blockchain
            transaction_hash = submit_data(m_f, right_hand, left_hand, twitter, github, sleep_hours)
            
            # Log data
            log_data(m_f, right_hand, left_hand, twitter, github, sleep_hours, transaction_hash)
            
            # Display spirit animal
            select_spirit_animal(transaction_hash)
            time.sleep(10)
        
        elif choice == '2':
            display_leaderboard()
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 