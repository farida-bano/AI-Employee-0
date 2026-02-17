import os
import argparse
import shutil

BASE_VAULT_PATH = "AI_Employee_Vault"
VALID_VAULT_DIRS = ["Inbox", "Needs_Action", "Done", "Need_Approval"] # Added Need_Approval for completeness

def move_task(filename, source_vault, destination_vault):
    if source_vault not in VALID_VAULT_DIRS or destination_vault not in VALID_VAULT_DIRS:
        print(f"Error: Invalid source or destination vault. Valid options are: {', '.join(VALID_VAULT_DIRS)}")
        return

    source_path = os.path.join(BASE_VAULT_PATH, source_vault, filename)
    destination_path = os.path.join(BASE_VAULT_PATH, destination_vault, filename)

    if not os.path.exists(source_path):
        print(f"Error: Source file '{source_path}' does not exist.")
        return

    try:
        shutil.move(source_path, destination_path)
        print(f"Success: Moved '{filename}' from '{source_vault}' to '{destination_vault}'.")
    except Exception as e:
        print(f"Error: Failed to move file. {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Move task files between vault directories.")
    parser.add_argument("--filename", required=True, help="The name of the file to move.")
    parser.add_argument("--source", required=True, help="The source vault directory (e.g., Inbox, Needs_Action).")
    parser.add_argument("--destination", required=True, help="The destination vault directory (e.g., Needs_Action, Done).")
    args = parser.parse_args()

    move_task(args.filename, args.source, args.destination)
