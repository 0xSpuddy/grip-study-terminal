import csv
import os
import time

# Get the directory of this file
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# Go up one level to the project root
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
# Define path to data directory and log files
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
LOG_FILE = os.path.join(DATA_DIR, 'logs.csv')
ERROR_LOG_FILE = os.path.join(DATA_DIR, 'error_logs.txt')

def ensure_data_dir_exists():
    # Create data directory if it doesn't exist
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    # Create CSV file with headers if it doesn't exist
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Data Set', 'Right Hand', 'Left Hand', 'Twitter', 'GitHub', 'Sleep Hours', 'Transaction Hash'])

def log_error(error_message, tx_data=None):
    """Log errors with timestamp and context"""
    ensure_data_dir_exists()
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    
    with open(ERROR_LOG_FILE, 'a') as file:
        file.write(f"\n[{timestamp}] ERROR:\n")
        file.write(f"Message: {error_message}\n")
        if tx_data:
            file.write(f"Transaction Data: {tx_data}\n")
        file.write("-" * 50 + "\n")

def log_data(m_f, right_hand, left_hand, twitter, github, sleep_hours, transaction_hash):
    ensure_data_dir_exists()
    # Convert to Wei-like precision before storing
    right_hand_wei = int(float(right_hand) * (10 ** 18))
    left_hand_wei = int(float(left_hand) * (10 ** 18))
    
    with open(LOG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([m_f, right_hand_wei, left_hand_wei, twitter, github, sleep_hours, transaction_hash])

def read_data():
    ensure_data_dir_exists()
    with open(LOG_FILE, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        return list(reader)
