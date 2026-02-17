import sys
import os
import time
import argparse
import datetime
import random # For simulating retry delays

# --- Configuration ---
VAULT_ROOT = os.path.join(os.getcwd(), 'AI_Employee_Vault')
LOGS_DIR = os.path.join(VAULT_ROOT, 'logs')
ACTIONS_LOG_FILE = os.path.join(LOGS_DIR, 'actions.log')
NEED_APPROVAL_DIR = os.path.join(VAULT_ROOT, 'Need_Approval')

# Ensure log and approval directories exist
os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(NEED_APPROVAL_DIR, exist_ok=True)

# --- Logging Function (reused from task_planner.py) ---
def log_action(message):
    timestamp = datetime.datetime.now().isoformat()
    with open(ACTIONS_LOG_FILE, 'a') as f:
        f.write(f"[{timestamp}] {message}
")
    print(message) # Also print to console for immediate feedback

# --- Retry Decorator ---
def retry(max_attempts=3, delay_seconds=2, catch_exceptions=(Exception,)):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except catch_exceptions as e:
                    log_action(f"WARNING: Attempt {attempt}/{max_attempts} failed for {func.__name__}: {e}")
                    if attempt < max_attempts:
                        time.sleep(delay_seconds + random.uniform(0, 1)) # Add some jitter
            log_action(f"ERROR: All {max_attempts} attempts failed for {func.__name__}.")
            raise
        return wrapper
    return decorator

# --- Human-in-the-Loop Approval ---
def check_approval(task_id):
    """
    Checks if a task has been approved by a human.
    Approval is indicated by an empty file named '<task_id>.approved' in the NEED_APPROVAL_DIR.
    """
    approval_file = os.path.join(NEED_APPROVAL_DIR, f"{task_id}.approved")
    if os.path.exists(approval_file):
        log_action(f"INFO: Approval found for task_id: {task_id}")
        return True
    else:
        log_action(f"INFO: No approval found for task_id: {task_id}. Please create '{approval_file}' to approve.")
        return False

# --- External Action Simulations ---

@retry()
def send_gmail(recipient, subject, body, task_id="N/A"):
    """
    Simulates sending an email using a 'gmail-send-skill'.
    """
    log_action(f"INFO: (Task ID: {task_id}) Simulating sending Gmail to '{recipient}' with subject '{subject}'...")
    # In a real scenario, this would involve calling the gmail-send-skill
    # Example: run_skill("gmail-send", recipient=recipient, subject=subject, body=body)
    # Simulate potential failure
    if random.random() < 0.1: # 10% chance of failure
        raise ConnectionError("Simulated Gmail service unavailable")
    log_action(f"SUCCESS: (Task ID: {task_id}) Gmail sent to '{recipient}'.")
    return True

@retry()
def post_linkedin_message(message, task_id="N/A"):
    """
    Simulates posting a message to LinkedIn using a 'linkedin-post-skill'.
    """
    log_action(f"INFO: (Task ID: {task_id}) Simulating posting LinkedIn message: '{message}'...")
    # In a real scenario, this would involve calling the linkedin-post-skill
    # Example: run_skill("linkedin-post", message=message)
    # Simulate potential failure
    if random.random() < 0.1: # 10% chance of failure
        raise ConnectionError("Simulated LinkedIn API error")
    log_action(f"SUCCESS: (Task ID: {task_id}) LinkedIn message posted.")
    return True

# --- Main Execution Block ---
def main():
    parser = argparse.ArgumentParser(description="MCP Executor Skill: Executes external actions based on AI workflow requests.")
    parser.add_argument('--task_id', type=str, default=f"task_{int(time.time())}",
                        help="Unique identifier for the task. Used for approval checks and logging.")
    parser.add_argument('--action', type=str, required=True, choices=['send_gmail', 'post_linkedin'],
                        help="The external action to perform.")
    
    # Arguments for send_gmail
    parser.add_argument('--recipient', type=str, help="Recipient email address for Gmail.")
    parser.add_argument('--subject', type=str, help="Subject for Gmail.")
    parser.add_argument('--body', type=str, help="Body for Gmail.")

    # Arguments for post_linkedin
    parser.add_argument('--message', type=str, help="Message content for LinkedIn post.")

    args = parser.parse_args()

    log_action(f"INFO: MCP Executor starting for Task ID: {args.task_id}, Action: {args.action}")

    # Check for human approval if required by the action or policy
    # For this simulation, we'll check approval for all external actions.
    if not check_approval(args.task_id):
        log_action(f"STATUS: Task {args.task_id} requires human approval before execution. Aborting for now.")
        sys.exit(0) # Exit gracefully, waiting for approval

    try:
        if args.action == 'send_gmail':
            if not all([args.recipient, args.subject, args.body]):
                log_action("ERROR: Missing arguments for send_gmail: --recipient, --subject, --body are required.")
                sys.exit(1)
            send_gmail(args.recipient, args.subject, args.body, args.task_id)
        elif args.action == 'post_linkedin':
            if not args.message:
                log_action("ERROR: Missing argument for post_linkedin: --message is required.")
                sys.exit(1)
            post_linkedin_message(args.message, args.task_id)
        else:
            log_action(f"ERROR: Unknown action: {args.action}")
            sys.exit(1)
    except Exception as e:
        log_action(f"CRITICAL ERROR: Failed to execute action '{args.action}' for task {args.task_id}: {e}")
        sys.exit(1)

    log_action(f"INFO: MCP Executor finished for Task ID: {args.task_id}")

if __name__ == "__main__":
    main()
