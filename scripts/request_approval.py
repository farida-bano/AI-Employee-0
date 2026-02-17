import os
import time
import argparse
import logging
import logging.handlers

# --- Configuration ---
APPROVAL_FOLDER = "AI_Employee_Vault/Need_Approval"
LOG_FILE = "logs/action.log"
DEFAULT_TIMEOUT_SECONDS = 3600  # 1 hour
POLLING_INTERVAL_SECONDS = 5 # How often to check for updates in the approval file

# --- Logger Setup ---
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# File handler for logging to a file with rotation (e.g., 1MB, 5 backups)
file_handler = logging.handlers.RotatingFileHandler(
    LOG_FILE, maxBytes=1 * 1024 * 1024, backupCount=5
)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

# Console handler (optional, for real-time feedback)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
logger.addHandler(console_handler)

def process_approval_request(file_path, timeout):
    logger.info(f"Monitoring file for approval: {file_path} with timeout {timeout} seconds.")
    start_time = time.time()
    
    while (time.time() - start_time) < timeout:
        if not os.path.exists(file_path):
            logger.warning(f"File {file_path} disappeared during monitoring.")
            return

        with open(file_path, 'r') as f:
            content = f.read().strip().upper()

        if "APPROVED" in content:
            logger.info(f"File {file_path} APPROVED.")
            new_file_path = file_path + ".approved"
            os.rename(file_path, new_file_path)
            logger.info(f"Renamed {file_path} to {new_file_path}")
            return
        elif "REJECTED" in content:
            logger.info(f"File {file_path} REJECTED.")
            new_file_path = file_path + ".rejected"
            os.rename(file_path, new_file_path)
            logger.info(f"Renamed {file_path} to {new_file_path}")
            return
        
        time.sleep(POLLING_INTERVAL_SECONDS)
    
    # Timeout reached
    logger.warning(f"Timeout for file {file_path}. No approval/rejection found.")
    new_file_path = file_path + ".timeout"
    os.rename(file_path, new_file_path)
    logger.info(f"Renamed {file_path} to {new_file_path} due to timeout.")

def main():
    parser = argparse.ArgumentParser(description="Human Approval Agent")
    parser.add_argument("file_to_monitor", help="Path to the file to monitor for approval/rejection.")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SECONDS,
                        help=f"Timeout in seconds (default: {DEFAULT_TIMEOUT_SECONDS} seconds, 1 hour).")
    
    args = parser.parse_args()

    # Ensure the approval folder exists
    os.makedirs(APPROVAL_FOLDER, exist_ok=True)
    
    full_file_path = os.path.join(APPROVAL_FOLDER, os.path.basename(args.file_to_monitor))

    if not os.path.exists(full_file_path):
        logger.error(f"File {full_file_path} does not exist. Please create it in {APPROVAL_FOLDER} first.")
        return

    process_approval_request(full_file_path, args.timeout)

if __name__ == "__main__":
    main()
