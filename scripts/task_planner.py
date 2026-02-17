import sys
import os
import shutil
import datetime
import hashlib

# --- Configuration ---
VAULT_ROOT = os.path.join(os.getcwd(), 'AI_Employee_Vault')
INBOX_DIR = os.path.join(VAULT_ROOT, 'Inbox')
NEEDS_ACTION_DIR = os.path.join(VAULT_ROOT, 'Needs_Action')
DONE_DIR = os.path.join(VAULT_ROOT, 'Done')
LOGS_DIR = os.path.join(VAULT_ROOT, 'logs')
ACTIONS_LOG_FILE = os.path.join(LOGS_DIR, 'actions.log')
PROCESSED_FILES_LOG = os.path.join(LOGS_DIR, 'processed_files.log')

# Ensure log directory exists
os.makedirs(LOGS_DIR, exist_ok=True)

# --- Logging Function ---
def log_action(message):
    timestamp = datetime.datetime.now().isoformat()
    with open(ACTIONS_LOG_FILE, 'a') as f:
        f.write(f"[{timestamp}] {message}
")
    print(message) # Also print to console for immediate feedback

# --- Idempotency Check ---
def get_file_hash(filepath):
    """Generates a SHA256 hash of a file's content."""
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while True:
            chunk = f.read(8192)  # Read in 8KB chunks
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()

def is_processed(filepath):
    """Checks if a file (by its hash) has already been processed."""
    file_hash = get_file_hash(filepath)
    if not os.path.exists(PROCESSED_FILES_LOG):
        return False
    with open(PROCESSED_FILES_LOG, 'r') as f:
        for line in f:
            if line.strip() == file_hash:
                return True
    return False

def mark_as_processed(filepath):
    """Marks a file (by its hash) as processed."""
    file_hash = get_file_hash(filepath)
    with open(PROCESSED_FILES_LOG, 'a') as f:
        f.write(f"{file_hash}
")

# --- Plan Generation (Simulated) ---
def generate_plan_from_content(content):
    """
    Simulates generating a step-by-step plan based on the input content.
    In a real scenario, this would involve calling an LLM.
    """
    plan = f"# Plan for Task

"
    plan += f"Generated on: {datetime.date.today().isoformat()}

"
    plan += f"--- Original Task Content ---
"
    plan += f"{content}
"
    plan += f"--- Step-by-Step Plan ---
"
    plan += f"1. Review the provided task content carefully.
"
    plan += f"2. Identify key objectives and deliverables.
"
    plan += f"3. Break down the task into smaller, manageable sub-tasks.
"
    plan += f"4. Assign priorities and estimated timelines to each sub-task.
"
    plan += f"5. Prepare any necessary resources or prerequisites.
"
    plan += f"6. Execute each sub-task systematically.
"
    plan += f"7. Verify completion and quality of each sub-task.
"
    plan += f"8. Assemble final deliverables.
"
    plan += f"9. Document the process and outcome.
"
    plan += f"10. Present the completed task.
"
    plan += f"
--- End of Plan ---
"
    return plan

# --- Main Processing Logic ---
def process_task_file(filepath):
    if not os.path.exists(filepath):
        log_action(f"ERROR: Input file not found: {filepath}")
        return

    if not filepath.endswith('.md'):
        log_action(f"WARNING: Skipping non-markdown file: {filepath}")
        return

    if is_processed(filepath):
        log_action(f"INFO: File already processed, skipping: {filepath}")
        return

    log_action(f"INFO: Processing new task file: {filepath}")

    try:
        # 1. Read content
        with open(filepath, 'r') as f:
            content = f.read()
        log_action(f"INFO: Read content from {os.path.basename(filepath)}")

        # 2. Generate plan
        plan_content = generate_plan_from_content(content)
        plan_filename = f"plan_{os.path.basename(filepath)}"
        plan_filepath = os.path.join(NEEDS_ACTION_DIR, plan_filename)
        
        with open(plan_filepath, 'w') as f:
            f.write(plan_content)
        log_action(f"INFO: Created plan file: {plan_filepath}")

        # 3. Move original file to Done
        shutil.move(filepath, os.path.join(DONE_DIR, os.path.basename(filepath)))
        log_action(f"INFO: Moved '{os.path.basename(filepath)}' to '{DONE_DIR}'")

        # 4. Mark as processed
        mark_as_processed(filepath)
        log_action(f"INFO: Marked '{os.path.basename(filepath)}' as processed.")

        log_action(f"SUCCESS: Successfully processed {filepath}")

    except Exception as e:
        log_action(f"ERROR: Failed to process {filepath} - {e}")

# --- Main Execution Block ---
if __name__ == "__main__":
    if len(sys.argv) < 2:
        log_action("ERROR: Usage: python task_planner.py <path_to_markdown_file>")
        sys.exit(1)

    input_md_file = sys.argv[1]
    process_task_file(input_md_file)
