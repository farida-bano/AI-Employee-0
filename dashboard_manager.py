#!/usr/bin/env python3

"""
Dashboard Management Script for AI Employee System
Implements claim-by-move and single-writer rules for Dashboard.md
"""

import os
import time
import datetime
import json
import fcntl
from pathlib import Path


class DashboardManager:
    def __init__(self, vault_path="AI_Employee_Vault"):
        self.vault_path = Path(vault_path)
        self.dashboard_path = self.vault_path / "Dashboard.md"
        self.dashboard_lock_path = self.vault_path / ".dashboard.lock"
        self.dashboard_claim_path = self.vault_path / ".dashboard_claim.json"

        # Ensure dashboard exists
        if not self.dashboard_path.exists():
            self.initialize_dashboard()

    def initialize_dashboard(self):
        """Initialize a new dashboard file"""
        initial_content = """# AI Employee Dashboard

## Tasks in Progress
- No active tasks

## Completed Tasks
- No completed tasks yet

## Pending Approvals
- No pending approvals

Last updated: """ + datetime.datetime.now().isoformat()

        self.dashboard_path.write_text(initial_content)
        print(f"Initialized dashboard at {self.dashboard_path}")

    def claim_by_move(self, task_path, destination_folder):
        """
        Implements claim-by-move rule: move a task to claim it
        This ensures only one instance processes a task
        """
        task_path = Path(task_path)
        destination_folder = self.vault_path / destination_folder

        if not task_path.exists():
            raise FileNotFoundError(f"Task file does not exist: {task_path}")

        if not destination_folder.exists():
            destination_folder.mkdir(parents=True, exist_ok=True)

        # Move the task file to claim it
        destination_path = destination_folder / task_path.name
        task_path.rename(destination_path)

        print(f"Claimed task by moving to {destination_path}")
        return destination_path

    def lock_dashboard(self, writer_id=None):
        """
        Acquire exclusive write lock on the dashboard
        Implements single-writer rule
        """
        if writer_id is None:
            writer_id = f"process_{os.getpid()}_{int(time.time())}"

        # Try to acquire file lock
        lock_file = open(self.dashboard_lock_path, 'w')
        try:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)

            # Record the claim
            claim_info = {
                "writer_id": writer_id,
                "timestamp": datetime.datetime.now().isoformat(),
                "pid": os.getpid()
            }
            self.dashboard_claim_path.write_text(json.dumps(claim_info))

            print(f"Dashboard locked for writer: {writer_id}")
            return lock_file
        except IOError:
            # Could not acquire lock
            lock_file.close()
            return None

    def unlock_dashboard(self, lock_file):
        """Release the dashboard lock"""
        if lock_file:
            try:
                fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
                lock_file.close()
                if self.dashboard_claim_path.exists():
                    self.dashboard_claim_path.unlink()
                print("Dashboard unlocked")
            except Exception as e:
                print(f"Error releasing dashboard lock: {e}")

    def update_dashboard(self, update_function, writer_id=None):
        """
        Safely update the dashboard using single-writer rule
        """
        lock_file = self.lock_dashboard(writer_id)
        if not lock_file:
            print("Could not acquire dashboard lock, another process is writing")
            return False

        try:
            # Read current dashboard content
            if self.dashboard_path.exists():
                current_content = self.dashboard_path.read_text()
            else:
                current_content = "# AI Employee Dashboard\n\n"

            # Apply update function
            new_content = update_function(current_content)

            # Write updated content
            self.dashboard_path.write_text(new_content)

            # Update timestamp
            timestamp_content = new_content + f"\n\nLast updated: {datetime.datetime.now().isoformat()}"
            self.dashboard_path.write_text(timestamp_content)

            print(f"Dashboard updated by {writer_id or 'unknown'}")
            return True

        except Exception as e:
            print(f"Error updating dashboard: {e}")
            return False
        finally:
            self.unlock_dashboard(lock_file)

    def get_dashboard_content(self):
        """Read dashboard content safely"""
        if self.dashboard_path.exists():
            return self.dashboard_path.read_text()
        else:
            return "# AI Employee Dashboard\n\nNo content available"

    def dashboard_status(self):
        """Check dashboard status and lock information"""
        status = {
            "dashboard_exists": self.dashboard_path.exists(),
            "lock_exists": self.dashboard_lock_path.exists(),
            "claim_exists": self.dashboard_claim_path.exists()
        }

        if self.dashboard_claim_path.exists():
            try:
                claim_info = json.loads(self.dashboard_claim_path.read_text())
                status["current_claim"] = claim_info
            except:
                status["current_claim"] = "Invalid claim file"

        return status


def example_dashboard_update(content):
    """Example update function that adds a new entry"""
    lines = content.split('\n')
    updated_lines = []
    added = False

    for line in lines:
        if line.strip() == "## Tasks in Progress" and not added:
            updated_lines.append(line)
            updated_lines.append("- Example task added by dashboard manager")
            added = True
        else:
            updated_lines.append(line)

    return '\n'.join(updated_lines)


if __name__ == "__main__":
    import sys

    manager = DashboardManager()

    if len(sys.argv) < 2:
        print("Usage: dashboard_manager.py {status|update|claim|lock_status}")
        sys.exit(1)

    command = sys.argv[1]

    if command == "status":
        print("Dashboard Status:")
        status = manager.dashboard_status()
        for key, value in status.items():
            print(f"  {key}: {value}")
        print("\nDashboard Content:")
        print(manager.get_dashboard_content())

    elif command == "update":
        writer_id = sys.argv[2] if len(sys.argv) > 2 else f"cli_{os.getpid()}"
        success = manager.update_dashboard(example_dashboard_update, writer_id)
        print(f"Update {'successful' if success else 'failed'}")

    elif command == "claim":
        if len(sys.argv) < 3:
            print("Usage: dashboard_manager.py claim <task_path> <destination_folder>")
            sys.exit(1)
        task_path = sys.argv[2]
        destination = sys.argv[3]
        try:
            result = manager.claim_by_move(task_path, destination)
            print(f"Task claimed successfully: {result}")
        except Exception as e:
            print(f"Failed to claim task: {e}")

    elif command == "lock_status":
        status = manager.dashboard_status()
        print(json.dumps(status, indent=2))

    else:
        print(f"Unknown command: {command}")
        print("Usage: dashboard_manager.py {status|update|claim|lock_status}")