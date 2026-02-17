import os
import time
import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- Configuration ---
INBOX_DIR = os.path.join("Bronze", "Inbox")
NEEDS_ACTION_DIR = os.path.join("Bronze", "Needs_Action")
LOG_FILE = os.path.join("Bronze", "System_log.md")

# --- Utility Functions ---

def log_activity(message):
    """Appends a message to the system log file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"- {timestamp}: {message}\n"
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)
    print(log_entry, end="")

# --- Event Handler ---

class NewFileHandler(FileSystemEventHandler):
    """Handles events for new files created in the Inbox."""

    def on_created(self, event):
        """
        Called when a file or directory is created.
        """
        if event.is_directory:
            return

        original_filename = os.path.basename(event.src_path)
        log_activity(f"New file detected in Inbox: {original_filename}")

        # Create the corresponding task file
        self.create_task_file(original_filename)

    def create_task_file(self, original_filename):
        """
        Creates a task file in the Needs_Action directory.
        """
        # Ignore hidden or system files
        if original_filename.startswith('.') or original_filename == "Thumbs.db":
            log_activity(f"Ignoring system file: {original_filename}")
            return

        task_filename = f"task_review_{original_filename}.md"
        task_filepath = os.path.join(NEEDS_ACTION_DIR, task_filename)

        # Create content for the task file
        creation_timestamp = datetime.datetime.now().isoformat()
        task_content = f"""---
filename: {original_filename}
created_at: {creation_timestamp}
status: pending
---
"""

        # Write the task file
        try:
            with open(task_filepath, "w") as f:
                f.write(task_content)
            log_activity(f"Created task file: {task_filename} in {NEEDS_ACTION_DIR}")
        except Exception as e:
            log_activity(f"ERROR: Could not create task file for {original_filename}. Reason: {e}")


# --- Main Execution ---

if __name__ == "__main__":
    # Ensure directories exist
    os.makedirs(INBOX_DIR, exist_ok=True)
    os.makedirs(NEEDS_ACTION_DIR, exist_ok=True)

    log_activity("File watcher started. Monitoring 'Bronze/Inbox' for new files.")

    event_handler = NewFileHandler()
    observer = Observer()
    observer.schedule(event_handler, INBOX_DIR, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        log_activity("File watcher stopped by user.")
    observer.join()
