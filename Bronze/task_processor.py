import os
import sys

# Ensure the script can find the 'Bronze' directory modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import agent_skills as skills
except ImportError:
    print("Error: 'agent_skills.py' not found. Make sure it's in the same directory.")
    sys.exit(1)


def process_all_pending_tasks():
    """
    Scans the Needs_Action directory and processes all pending .md task files.
    """
    # Correctly resolve the path for Needs_Action relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    needs_action_dir = os.path.join(script_dir, "Needs_Action")

    if not os.path.exists(needs_action_dir):
        skills.log_activity(f"ERROR: Directory not found: {needs_action_dir}. Cannot process tasks.")
        return

    tasks_to_process = [f for f in os.listdir(needs_action_dir) if f.endswith('.md')]

    if not tasks_to_process:
        skills.log_activity("No tasks to process in Needs_Action directory.")
        return

    skills.log_activity(f"Found {len(tasks_to_process)} tasks. Starting processing...")
    processed_count = 0
    failed_count = 0

    for task_filename in tasks_to_process:
        task_path = os.path.join(needs_action_dir, task_filename)
        
        try:
            # 1. Read the task and check status
            task_data = skills.read_task(task_path)
            
            if task_data.get('status') != 'pending':
                skills.log_activity(f"Skipping task '{task_filename}' (status is not 'pending').")
                continue

            skills.log_activity(f"Processing task: {task_filename} for original file: {task_data.get('filename')}")

            # 2. Update status to completed (with timestamp)
            if not skills.update_status_to_completed(task_path):
                raise Exception("Failed to update status to completed.")

            # 3. Move the file to Done
            new_path = skills.move_file_to_done(task_path)
            if not new_path:
                 raise Exception("Failed to move file to Done directory.")

            # 4. Update the dashboard
            skills.update_dashboard(os.path.basename(new_path))
            
            skills.log_activity(f"Successfully processed task: {task_filename}")
            processed_count += 1

        except Exception as e:
            skills.log_activity(f"CRITICAL FAILURE processing task {task_filename}. Reason: {e}")
            failed_count += 1
            # Continue to the next task
            continue
            
    skills.log_activity(f"Task processing summary: {processed_count} succeeded, {failed_count} failed.")


if __name__ == '__main__':
    process_all_pending_tasks()
