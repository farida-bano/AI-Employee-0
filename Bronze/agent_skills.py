import os
import datetime
import shutil
import re

# --- Configuration ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NEEDS_ACTION_DIR = os.path.join(BASE_DIR, "Needs_Action")
DONE_DIR = os.path.join(BASE_DIR, "Done")
DASHBOARD_FILE = os.path.join(BASE_DIR, "Dashboard.md")
LOG_FILE = os.path.join(BASE_DIR, "System_log.md")


# --- Skill 5: Logger ---
def log_activity(message: str):
    """
    Writes a timestamped log message to the system log file.
    Args:
        message (str): The message to log.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"- {timestamp}: {message}\n"
    try:
        with open(LOG_FILE, "a") as f:
            f.write(log_entry)
        print(f"Logged: {message}")
    except Exception as e:
        print(f"Error logging to {LOG_FILE}: {e}")


# --- Skill 1: Task Reader ---
def read_task(task_filepath: str) -> dict:
    """
    Reads and parses a task file from the Needs_Action directory.
    Args:
        task_filepath (str): The full path to the task file.
    Returns:
        dict: A dictionary containing the task's metadata.
    """
    task_data = {}
    try:
        with open(task_filepath, "r") as f:
            content = f.read()
            
        # Basic frontmatter parsing
        match = re.search(r"---(.*?)---", content, re.DOTALL)
        if match:
            frontmatter = match.group(1)
            for line in frontmatter.strip().split('\n'):
                if ":" in line:
                    key, value = line.split(":", 1)
                    task_data[key.strip()] = value.strip()
        
        log_activity(f"Successfully read and parsed task: {os.path.basename(task_filepath)}")
        return task_data
    except FileNotFoundError:
        log_activity(f"ERROR: Task file not found at {task_filepath}")
        return {"error": "File not found"}
    except Exception as e:
        log_activity(f"ERROR: Failed to read task {task_filepath}. Reason: {e}")
        return {"error": str(e)}


# --- Skill 2: Status Updater ---
def update_status_to_completed(task_filepath: str) -> bool:
    """
    Changes the status of a task to 'completed' and adds a completion timestamp.
    Args:
        task_filepath (str): The full path to the task file.
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        with open(task_filepath, "r") as f:
            content = f.read()

        if "status: pending" not in content:
            log_activity(f"WARNING: Task status in {os.path.basename(task_filepath)} is not 'pending'. No change made.")
            return False

        completion_timestamp = datetime.datetime.now().isoformat()
        
        # Replace status and add completion timestamp right after
        updated_content = content.replace(
            "status: pending",
            f"status: completed\ncompleted_at: {completion_timestamp}"
        )

        with open(task_filepath, "w") as f:
            f.write(updated_content)
            
        log_activity(f"Updated status to 'completed' for task: {os.path.basename(task_filepath)}")
        return True
    except Exception as e:
        log_activity(f"ERROR: Failed to update status for {os.path.basename(task_filepath)}. Reason: {e}")
        return False


# --- Skill 3: File Mover ---
def move_file_to_done(task_filepath: str) -> str or None:
    """
    Moves a processed task file from Needs_Action to the Done folder.
    Args:
        task_filepath (str): The full path to the task file in Needs_Action.
    Returns:
        str: The new path of the moved file, or None on failure.
    """
    if not os.path.exists(task_filepath):
        log_activity(f"ERROR: Cannot move file. Source file not found: {task_filepath}")
        return None
        
    filename = os.path.basename(task_filepath)
    destination_path = os.path.join(DONE_DIR, filename)

    try:
        os.makedirs(DONE_DIR, exist_ok=True)
        shutil.move(task_filepath, destination_path)
        log_activity(f"Moved task file {filename} from Needs_Action to Done.")
        return destination_path
    except Exception as e:
        log_activity(f"ERROR: Failed to move file {filename}. Reason: {e}")
        return None


# --- Skill 4: Dashboard Updater ---
def update_dashboard(task_filename: str):
    """
    Appends a completed task to the dashboard file.
    Args:
        task_filename (str): The filename of the completed task.
    """
    entry = f"\n- Completed: {task_filename}"
    try:
        # Ensure the "Completed Tasks" header exists
        if os.path.exists(DASHBOARD_FILE):
             with open(DASHBOARD_FILE, "r") as f:
                content = f.read()
        else:
            content = ""

        if "## Completed Tasks" not in content:
            with open(DASHBOARD_FILE, "a") as f:
                f.write("\n\n## Completed Tasks\n")

        with open(DASHBOARD_FILE, "a") as f:
            f.write(entry)
        log_activity(f"Updated dashboard with completed task: {task_filename}")
    except Exception as e:
        log_activity(f"ERROR: Could not update dashboard. Reason: {e}")

if __name__ == '__main__':
    print("Agent Skills module loaded. This file provides reusable functions for the AI Employee.")
    print("It is not meant to be executed directly, but its functions can be imported and used by other scripts.")
    # You can add test calls here for development, for example:
    # log_activity("Test log from agent_skills.py")
