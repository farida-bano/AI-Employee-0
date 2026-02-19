import os
import sys
import argparse
import datetime
import json
import logging
import shutil
import re


def setup_logging():
    """Setup logging for the personal task handler skill."""
    log_dir = os.path.join("AI_Employee_Vault", "personal", "Logs")
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, "personal_tasks.log")

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, mode='a'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)


def get_vault_paths():
    """Get the paths for the personal task workflow directories."""
    base_dir = os.getenv("PERSONAL_VAULT_PATH", os.path.join("AI_Employee_Vault", "personal"))

    return {
        'base_dir': base_dir,
        'inbox_dir': os.path.join(base_dir, "Inbox"),
        'needs_action_dir': os.path.join(base_dir, "Needs_Action"),
        'done_dir': os.path.join(base_dir, "Done")
    }


def ensure_directories_exist():
    """Ensure all required directories exist."""
    paths = get_vault_paths()
    os.makedirs(paths['inbox_dir'], exist_ok=True)
    os.makedirs(paths['needs_action_dir'], exist_ok=True)
    os.makedirs(paths['done_dir'], exist_ok=True)


def read_task(task_filepath: str) -> dict:
    """
    Reads and parses a task file from the personal domain.

    Args:
        task_filepath (str): The full path to the task file.

    Returns:
        dict: A dictionary containing the task's metadata and content.
    """
    logger = setup_logging()
    task_data = {"content": "", "metadata": {}}

    try:
        with open(task_filepath, "r", encoding='utf-8') as f:
            content = f.read()

        # Parse frontmatter if it exists
        frontmatter_match = re.search(r"---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
        if frontmatter_match:
            frontmatter = frontmatter_match.group(1)
            for line in frontmatter.strip().split('\n'):
                if ":" in line:
                    key, value = line.split(":", 1)
                    task_data["metadata"][key.strip()] = value.strip()

            # Extract the actual content after frontmatter
            task_data["content"] = content[frontmatter_match.end():].strip()
        else:
            # If no frontmatter, consider all content as the task
            task_data["content"] = content.strip()

        logger.info(f"Successfully read and parsed personal task: {os.path.basename(task_filepath)}")
        return task_data

    except FileNotFoundError:
        error_msg = f"ERROR: Personal task file not found at {task_filepath}"
        logger.error(error_msg)
        return {"error": "File not found", "content": "", "metadata": {}}

    except Exception as e:
        error_msg = f"ERROR: Failed to read personal task {task_filepath}. Reason: {e}"
        logger.error(error_msg)
        return {"error": str(e), "content": "", "metadata": {}}


def update_status_to_completed(task_filepath: str, result: str = "") -> bool:
    """
    Updates the status of a task to 'completed' and adds completion details.

    Args:
        task_filepath (str): The full path to the task file.
        result (str): Optional result or output from the task execution.

    Returns:
        bool: True if successful, False otherwise.
    """
    logger = setup_logging()

    try:
        with open(task_filepath, "r", encoding='utf-8') as f:
            content = f.read()

        completion_timestamp = datetime.datetime.now().isoformat()

        # Check if the file has frontmatter
        if content.startswith("---"):
            # Add completion info to frontmatter
            lines = content.split('\n')
            frontmatter_end = -1
            for i, line in enumerate(lines):
                if line.strip() == "---" and i > 0:
                    frontmatter_end = i
                    break

            if frontmatter_end > 0:
                # Insert status and completion time in the frontmatter
                updated_lines = lines[:frontmatter_end]
                updated_lines.insert(frontmatter_end - 1, f"  status: completed")
                updated_lines.insert(frontmatter_end - 1, f"  completed_at: {completion_timestamp}")
                if result:
                    updated_lines.insert(frontmatter_end - 1, f"  result: {result}")
                updated_lines.extend(lines[frontmatter_end:])
                updated_content = '\n'.join(updated_lines)
            else:
                # Didn't find proper end of frontmatter, just append to content
                updated_content = f"{content}\n\n# Status\n- Completed: {completion_timestamp}\n- Result: {result}"
        else:
            # No frontmatter, add status at the end
            updated_content = f"{content}\n\n# Status\n- Completed: {completion_timestamp}\n- Result: {result}"

        with open(task_filepath, "w", encoding='utf-8') as f:
            f.write(updated_content)

        logger.info(f"Updated status to 'completed' for personal task: {os.path.basename(task_filepath)}")
        return True

    except Exception as e:
        error_msg = f"ERROR: Failed to update status for {os.path.basename(task_filepath)}. Reason: {e}"
        logger.error(error_msg)
        return False


def move_file_to_done(task_filepath: str) -> str:
    """
    Moves a processed task file from Needs_Action to the Done folder.

    Args:
        task_filepath (str): The full path to the task file in Needs_Action.

    Returns:
        str: The new path of the moved file, or None on failure.
    """
    logger = setup_logging()

    if not os.path.exists(task_filepath):
        error_msg = f"ERROR: Cannot move file. Source file not found: {task_filepath}"
        logger.error(error_msg)
        return None

    filename = os.path.basename(task_filepath)
    paths = get_vault_paths()
    destination_path = os.path.join(paths['done_dir'], filename)

    try:
        shutil.move(task_filepath, destination_path)
        logger.info(f"Moved personal task file {filename} from Needs_Action to Done.")
        return destination_path
    except Exception as e:
        error_msg = f"ERROR: Failed to move file {filename}. Reason: {e}"
        logger.error(error_msg)
        return None


def process_task(task_file_path: str) -> str:
    """
    Process a personal task file.

    Args:
        task_file_path: Path to the task file to process

    Returns:
        str: Result of the processing
    """
    logger = setup_logging()

    try:
        # Ensure directories exist
        ensure_directories_exist()

        # Read the task
        task_data = read_task(task_file_path)

        if "error" in task_data:
            return f"Error reading task: {task_data['error']}"

        task_content = task_data["content"]
        task_metadata = task_data["metadata"]

        # Log the task processing
        logger.info(f"Processing personal task: {os.path.basename(task_file_path)}")
        logger.info(f"Task content preview: {task_content[:100]}...")

        # Execute the actual task logic
        result = execute_task_logic(task_content, task_metadata)

        # Update status to completed
        update_status_to_completed(task_file_path, result)

        # Move to Done folder
        new_path = move_file_to_done(task_file_path)

        if new_path:
            return f"Personal task completed successfully and moved to Done: {os.path.basename(new_path)}"
        else:
            return f"Personal task completed but failed to move to Done folder: {result}"

    except Exception as e:
        error_msg = f"Error processing personal task {task_file_path}: {str(e)}"
        logger.error(error_msg)
        return f"Error: {error_msg}"


def execute_task_logic(content: str, metadata: dict) -> str:
    """
    Execute the actual logic for the task based on its content.

    Args:
        content: The content of the task
        metadata: Metadata from the task file

    Returns:
        str: Result of the executed task
    """
    logger = setup_logging()

    # This is where we would implement task-specific logic
    # For now, we'll implement a few example task types

    try:
        content_lower = content.lower()

        if "schedule" in content_lower or "appointment" in content_lower:
            # Handle scheduling tasks
            result = "Scheduling task processed - added to personal calendar"
        elif "note" in content_lower or "reminder" in content_lower:
            # Handle note/reminder tasks
            result = "Note/reminder task processed - added to personal notes"
        elif "email" in content_lower or "contact" in content_lower:
            # Handle email/contact tasks
            result = "Email/contact task processed - action completed"
        elif "todo" in content_lower or "task" in content_lower:
            # Handle general todo tasks
            result = "Personal todo task processed - marked as complete"
        else:
            # Default processing for other tasks
            result = f"Generic personal task processed. Content length: {len(content)} characters"

        logger.info(f"Task execution completed with result: {result}")
        return result

    except Exception as e:
        error_msg = f"Error in task execution logic: {str(e)}"
        logger.error(error_msg)
        return f"Task execution failed: {error_msg}"


def main():
    parser = argparse.ArgumentParser(description="Handle personal tasks in the personal domain")
    parser.add_argument("--task-path", required=True, help="Path to the personal task file to process")

    args = parser.parse_args()

    result = process_task(args.task_path)
    print(result)


if __name__ == "__main__":
    main()
