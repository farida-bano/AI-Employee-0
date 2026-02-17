import os
import sys
import datetime
import shutil

LOG_FILE = "logs/errors.log"
ERROR_VAULT_DIR = os.path.join("AI_Employee_Vault", "Errors")

def handle_error(original_file_path: str, error_message: str):
    """
    Handles an error by logging it, moving the problematic file to a quarantine
    directory, and signaling for a potential retry.

    Args:
        original_file_path: The path to the file that caused the error.
        error_message: A detailed message describing the error.
    """
    timestamp = datetime.datetime.now().isoformat()
    
    # Ensure logs directory exists
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    # 1. Log error to logs/errors.log
    log_entry = (
        f"[{timestamp}] ERROR: Processing '{original_file_path}' failed. "
        f"Message: {error_message}. Retry requested after 5 minutes.
"
    )
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)
    print(f"Error logged to {LOG_FILE}")

    # Ensure error vault directory exists
    os.makedirs(ERROR_VAULT_DIR, exist_ok=True)

    # 2. Move file to AI_Employee_Vault/Errors/
    if os.path.exists(original_file_path):
        file_name = os.path.basename(original_file_path)
        # Add timestamp to filename to prevent overwrites
        quarantined_file_name = f"{timestamp}_{file_name}"
        destination_path = os.path.join(ERROR_VAULT_DIR, quarantined_file_name)
        
        try:
            shutil.move(original_file_path, destination_path)
            print(f"Moved '{original_file_path}' to '{destination_path}'")
        except Exception as e:
            print(f"Error moving file '{original_file_path}' to '{destination_path}': {e}")
    else:
        print(f"Original file '{original_file_path}' not found, cannot move.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python handle_error.py <original_file_path> <error_message>")
        sys.exit(1)
    
    original_file_path = sys.argv[1]
    error_message = sys.argv[2]
    handle_error(original_file_path, error_message)
