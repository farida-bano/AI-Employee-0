import os
import argparse
import time

BASE_VAULT_PATH = "AI_Employee_Vault"
APPROVAL_DIR = os.path.join(BASE_VAULT_PATH, "Need_Approval")

def request_approval(action_details, approval_id):
    os.makedirs(APPROVAL_DIR, exist_ok=True)
    approval_file_path = os.path.join(APPROVAL_DIR, f"{approval_id}.md")

    # Create the approval request file
    with open(approval_file_path, "w") as f:
        f.write(f"Approval Request ID: {approval_id}
")
        f.write(f"Action Details:
{action_details}

")
        f.write("Status: PENDING
")
        f.write("Please update this file with 'APPROVED' or 'REJECTED' as the first line.
")

    print(f"Approval request created: {approval_file_path}")
    print("Waiting for human approval...")

    while True:
        if not os.path.exists(approval_file_path):
            print(f"Error: Approval file '{approval_file_path}' was deleted unexpectedly.")
            return

        with open(approval_file_path, "r") as f:
            content = f.read().strip().upper()

        if "APPROVED" in content.splitlines()[0]:
            print("Status: APPROVED")
            # Optionally, remove the file after approval, or move it to a 'Done' directory
            # os.remove(approval_file_path)
            break
        elif "REJECTED" in content.splitlines()[0]:
            print("Status: REJECTED")
            # os.remove(approval_file_path)
            break
        time.sleep(5) # Check every 5 seconds

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Request human approval for a sensitive action.")
    parser.add_argument("--action_details", required=True, help="Details of the action requiring approval.")
    parser.add_argument("--approval_id", required=True, help="Unique identifier for this approval request.")
    args = parser.parse_args()

    request_approval(args.action_details, args.approval_id)
