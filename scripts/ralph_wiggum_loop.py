import os
import sys
import subprocess
import json
import datetime
import re # For parsing task content
import shutil # For moving files in handle_error context

# --- Paths to other scripts/skills ---
# Note: These paths are relative to the project root, assuming ralph_wiggum_loop.py is in scripts/
HANDLE_ERROR_SCRIPT = os.path.join(".claude", "skills", "error-recovery", "scripts", "handle_error.py")
REQUEST_APPROVAL_SCRIPT = os.path.join(".claude", "skills", "human-approval", "scripts", "request_approval.py")
MOVE_TASK_SCRIPT = os.path.join(".claude", "skills", "vault-file-manager", "scripts", "move_task.py")

MAX_ITERATIONS = 5

def call_script(script_path, *args):
    """Helper function to call other Python scripts."""
    cmd = [sys.executable, script_path] + list(args)
    print(f"DEBUG: Calling script: {' '.join(cmd)}") # Debug print
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False) # check=False to handle script's own exit codes
        
        # Log stdout/stderr for debugging even if it's not a CalledProcessError
        if result.stdout:
            print(f"Script '{os.path.basename(script_path)}' stdout:\n{result.stdout.strip()}")
        if result.stderr:
            print(f"Script '{os.path.basename(script_path)}' stderr:\n{result.stderr.strip()}")

        if result.returncode != 0:
            print(f"Script '{os.path.basename(script_path)}' exited with non-zero status {result.returncode}")
            return False, result.stderr.strip()
            
        return True, result.stdout.strip()
    except FileNotFoundError:
        print(f"Error: Script '{script_path}' not found.")
        return False, f"Script '{script_path}' not found."
    except Exception as e:
        print(f"An unexpected error occurred while running '{script_path}': {e}")
        return False, str(e)


def generate_executable_plan(task_content):
    """
    Generates a simple executable plan from task content.
    This is a placeholder for more advanced LLM-driven planning.
    For now, it parses specific phrases.
    """
    plan = []

    # Example: "Create a new file named `test_ralph.txt` in the root directory of the project and write the string "Hello from Ralph" into it."
    create_file_match = re.search(
        r"Create a new file named `(?P<filename>[^`]+)`.*?write the string \"(?P<content>[^\"]+)\" into it",
        task_content,
        re.IGNORECASE | re.DOTALL
    )
    
    if create_file_match:
        filename = create_file_match.group("filename")
        content = create_file_match.group("content")
        plan.append({
            "action": "write_file",
            "file_path": os.path.join(os.getcwd(), filename), # Assume root directory for now
            "content": content,
            "description": f"Create file '{filename}' with content '{content}'"
        })
    
    # Placeholder for a risky operation example
    # If the task explicitly asks to delete something, prompt for approval
    if re.search(r"delete|remove", task_content, re.IGNORECASE):
        plan.insert(0, { # Insert at beginning to ensure approval before any potentially destructive action
            "action": "request_approval",
            "reason": f"Task involves potentially risky operation (delete/remove): {task_content[:100]}...",
            "description": "Request human approval for risky operation"
        })
    
    if not plan: # If no specific action was parsed, consider it an uninterpretable task
        plan.append({
            "action": "log_unplanned_task",
            "message": "Task content could not be converted into an executable plan.",
            "description": "Log an unplannable task for review"
        })


    return plan


def process_task(task_file_full_path):
    print(f"Ralph Wiggum Loop: Processing task: {task_file_full_path}")
    
    # Extract just the filename and source vault
    source_vault = os.path.basename(os.path.dirname(task_file_full_path)) # e.g., "Needs_Action"
    file_name_only = os.path.basename(task_file_full_path)

    try:
        with open(task_file_full_path, 'r') as f:
            task_content = f.read()

        executable_plan = generate_executable_plan(task_content)
        
        # If the only step is 'log_unplanned_task', consider it a planning failure
        if len(executable_plan) == 1 and executable_plan[0]["action"] == "log_unplanned_task":
            print(f"Ralph Wiggum Loop: No executable plan generated for task: {file_name_only}. Logging and moving to Errors.")
            call_script(
                HANDLE_ERROR_SCRIPT, 
                task_file_full_path, 
                executable_plan[0]["message"]
            )
            # The original task file will be moved by handle_error.py
            return

        iterations = 0
        for step in executable_plan:
            iterations += 1
            if iterations > MAX_ITERATIONS:
                print(f"Ralph Wiggum Loop: Task '{file_name_only}' exceeded {MAX_ITERATIONS} iterations. Halting execution and moving to Errors.")
                call_script(
                    HANDLE_ERROR_SCRIPT, 
                    task_file_full_path, 
                    f"Task exceeded {MAX_ITERATIONS} iterations."
                )
                return # Exit processing this task

            print(f"Ralph Wiggum Loop: Executing step {iterations}: {step.get('description', step['action'])}")

            if step["action"] == "request_approval":
                print(f"Ralph Wiggum Loop: Requesting human approval for: {step['reason']}")
                success, response_message = call_script(REQUEST_APPROVAL_SCRIPT, file_name_only, step["reason"]) # Pass filename for context
                if not success or "approved" not in response_message.lower():
                    print(f"Ralph Wiggum Loop: Human approval denied or failed for '{file_name_only}'. Moving to Errors.")
                    # If approval is denied, consider it an error in processing this task, and move it to Errors
                    call_script(
                        HANDLE_ERROR_SCRIPT, 
                        task_file_full_path, 
                        f"Human approval denied for step: {step['reason']}. Response: {response_message}"
                    )
                    return # Exit processing this task

            elif step["action"] == "write_file":
                file_path_to_write = step["file_path"]
                content_to_write = step["content"]
                
                try:
                    # Ensure directory exists for the target file
                    os.makedirs(os.path.dirname(file_path_to_write), exist_ok=True)
                    with open(file_path_to_write, "w") as f:
                        f.write(content_to_write)
                    print(f"Ralph Wiggum Loop: Successfully wrote to {file_path_to_write}")
                except Exception as e:
                    print(f"Ralph Wiggum Loop: Failed to write file {file_path_to_write}: {e}")
                    call_script(
                        HANDLE_ERROR_SCRIPT, 
                        task_file_full_path, 
                        f"Failed to write file {file_path_to_write}: {e}"
                    )
                    return # Exit processing this task
            
            # Add other executable actions here as needed (e.g., "run_shell_command", "replace_text", etc.)
            else:
                print(f"Ralph Wiggum Loop: Unknown action: {step['action']}")
                call_script(
                    HANDLE_ERROR_SCRIPT, 
                    task_file_full_path, 
                    f"Unknown action in plan: {step['action']}"
                )
                return # Exit processing this task

        print(f"Ralph Wiggum Loop: Task '{file_name_only}' completed successfully. Moving to Done.")
        success, _ = call_script(MOVE_TASK_SCRIPT, file_name_only, source_vault, "Done")
        if not success:
            print(f"Ralph Wiggum Loop: Failed to move task {file_name_only} to Done. Keeping in Errors.")
            # handle_error.py would have already moved it if an error happened during execution.
            # If move_task fails here, it's an issue with the vault manager itself.
            call_script(
                HANDLE_ERROR_SCRIPT, 
                task_file_full_path, # This path might not exist if move_task already failed
                f"Failed to move task '{file_name_only}' to Done after successful execution."
            )
        
    except Exception as e:
        print(f"Ralph Wiggum Loop: An unhandled error occurred during task processing for '{file_name_only}': {e}")
        call_script(
            HANDLE_ERROR_SCRIPT, 
            task_file_full_path, 
            f"An unhandled exception occurred in ralph_wiggum_loop: {e}"
        )

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ralph_wiggum_loop.py <task_file_full_path>")
        sys.exit(1)
    
    task_file_path_arg = sys.argv[1]
    process_task(task_file_path_arg)
