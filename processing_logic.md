# AI Employee Vault - Processing Logic and Example Workflow

## Overview
This document describes the processing logic and workflow for the AI Employee vault system with Git-based synchronization.

## Folder Structure

```
AI_Employee_Vault/
├── Needs_Action/
│   ├── email/
│   └── social/
├── Pending_Approval/
│   ├── email/
│   └── social/
├── Approved/
├── In_Progress/
│   ├── cloud/
│   └── local/
├── Done/
├── Errors/
├── Inbox/
├── logs/
└── Reports/
```

### Directory Descriptions

- **Inbox/**: New tasks arrive here from external sources
- **Needs_Action/**: Tasks ready for processing, sorted by type (email/social)
- **Pending_Approval/**: Tasks requiring approval, sorted by type
- **Approved/**: Tasks that have received approval and are queueing for execution
- **In_Progress/**: Active tasks, separated by processing origin (cloud/local)
- **Done/**: Completed tasks moved here after processing
- **Errors/**: Tasks that failed processing, quarantined for review
- **Logs/**: System logs and audit trails
- **Reports/**: Generated reports and summaries

## Processing Logic

### 1. Task Ingestion
```python
# Pseudo-code for task ingestion
def process_inbox():
    for file in list_files("AI_Employee_Vault/Inbox/"):
        task_type = determine_task_type(file)
        destination = f"AI_Employee_Vault/Needs_Action/{task_type}/"
        move_file(file, destination)
```

### 2. Task Claiming (Claim-by-Move Rule)
```python
# Pseudo-code for task claiming
def claim_task(instance_type):
    task_folders = ["Needs_Action/email", "Needs_Action/social", "Pending_Approval/email", "Pending_Approval/social"]

    for folder in task_folders:
        for task_file in list_files(f"AI_Employee_Vault/{folder}/"):
            try:
                # Attempt to move task to in-progress with instance type
                destination = f"AI_Employee_Vault/In_Progress/{instance_type}/"
                move_file(task_file, destination)  # This claims the task
                return process_task(f"{destination}/{task_file}")
            except FileMovedError:
                # Task was already claimed by another instance
                continue
```

### 3. Dashboard Updates (Single-Writer Rule)
```python
# Pseudo-code for dashboard updates
def update_dashboard_safely(content_update_func):
    with dashboard_lock():
        current_content = read_dashboard()
        new_content = content_update_func(current_content)
        write_dashboard(new_content)
```

## Example Workflow

### Scenario: Processing an Email Task

1. **Task Arrival**
   - User creates `new_campaign_email.md` in `AI_Employee_Vault/Inbox/`
   - File watcher detects new file and moves it to `AI_Employee_Vault/Needs_Action/email/`

2. **Task Claiming**
   - Cloud instance detects file in `Needs_Action/email/`
   - Cloud instance attempts to move `new_campaign_email.md` to `AI_Employee_Vault/In_Progress/cloud/`
   - Local instance tries to claim the same task but fails (file already moved)
   - Cloud instance successfully claims the task

3. **Task Processing**
   - Cloud instance processes the email task
   - Updates dashboard with "Processing: new_campaign_email.md" using single-writer lock

4. **Approval Required**
   - Task requires approval, moves to `AI_Employee_Vault/Pending_Approval/email/`
   - Dashboard updated to reflect status change

5. **Approval Granted**
   - Human approves the task
   - Task moves to `AI_Employee_Vault/Approved/`

6. **Task Execution**
   - Task moves to `AI_Employee_Vault/In_Progress/cloud/` for execution
   - Email is sent via Business MCP server

7. **Completion**
   - Task moves to `AI_Employee_Vault/Done/`
   - Dashboard updated to reflect completion
   - Success report generated in `AI_Employee_Vault/Reports/`

## Instance Coordination

### Cloud Instance Responsibilities
- Pulls vault changes every 2 minutes via cron
- Processes high-priority tasks
- Handles external API communications
- Manages social media tasks
- Generates reports

### Local Instance Responsibilities
- Pushes changes manually when ready
- Processes local-specific tasks
- Handles sensitive internal operations
- Manages email tasks
- Performs data validation

## Synchronization Logic

### Git Sync Operations
1. **Pull Operation** (every 2 minutes by cloud instance)
   - Fetches latest repository changes
   - Merges changes, handling conflicts automatically for Dashboard.md
   - Updates local vault state

2. **Push Operation** (manual by local instance)
   - Commits all local changes
   - Pushes to remote repository
   - Updates dashboard with sync timestamp

### Conflict Resolution
1. **Dashboard.md**: Automatic merge preserving both cloud and local sections
2. **Task Files**: Claim-by-move ensures only one instance processes each task
3. **Other Files**: Standard Git merge behavior

## State Management

### Task States
- **New**: In `Inbox/`
- **Ready**: In `Needs_Action/*`
- **Claimed**: In `In_Progress/*`
- **Pending**: In `Pending_Approval/*`
- **Approved**: In `Approved/`
- **Processed**: In `Done/`
- **Error**: In `Errors/`

### Dashboard Sections
The dashboard maintains separate sections for:
- Active tasks by instance (cloud/local)
- Recently completed tasks
- Pending approvals
- Error summaries

## Example Code Implementation

### Task Processor with Claim-by-Move
```python
import os
import shutil
from pathlib import Path
from dashboard_manager import DashboardManager

class TaskProcessor:
    def __init__(self, instance_type="cloud"):
        self.instance_type = instance_type
        self.dashboard_manager = DashboardManager()
        self.vault_path = Path("AI_Employee_Vault")

    def find_and_claim_task(self):
        """Find a task and claim it using claim-by-move"""
        task_dirs = [
            "Needs_Action/email",
            "Needs_Action/social",
            "Pending_Approval/email",
            "Pending_Approval/social"
        ]

        for task_dir in task_dirs:
            full_dir = self.vault_path / task_dir
            if not full_dir.exists():
                continue

            for task_file in full_dir.iterdir():
                if task_file.is_file():
                    try:
                        # Attempt to claim the task by moving it
                        in_progress_dir = self.vault_path / "In_Progress" / self.instance_type
                        in_progress_dir.mkdir(parents=True, exist_ok=True)

                        destination = in_progress_dir / task_file.name
                        shutil.move(str(task_file), str(destination))

                        print(f"Claimed task: {task_file.name}")
                        return destination
                    except OSError:
                        # File was already moved by another instance
                        continue

        return None  # No tasks available

    def update_dashboard_with_status(self, task_name, status):
        """Safely update dashboard with single-writer rule"""
        def update_func(content):
            lines = content.split('\n')
            updated_lines = []
            found_section = False

            for line in lines:
                if f"## Tasks in Progress" in line:
                    updated_lines.append(line)
                    updated_lines.append(f"- {status}: {task_name} (by {self.instance_type})")
                    found_section = True
                else:
                    updated_lines.append(line)

            return '\n'.join(updated_lines)

        return self.dashboard_manager.update_dashboard(update_func)

# Usage example:
processor = TaskProcessor("cloud")
while True:
    task = processor.find_and_claim_task()
    if task:
        processor.update_dashboard_with_status(task.name, "Processing")
        # Process the task...
        # Move to appropriate final location
    else:
        print("No tasks to claim")
        break
```

## Safety Mechanisms

### 1. Mutual Exclusion for Dashboard
- File locking prevents concurrent dashboard updates
- Queue mechanism for pending updates

### 2. Task Deduplication
- Claim-by-move ensures each task is processed only once
- Instance tagging in progress directories

### 3. Data Integrity
- Git version control provides audit trail
- Backup creation during conflict resolution
- Regular integrity checks

## Monitoring and Operations

### Daily Operations
- Monitor sync logs for conflicts
- Check dashboard status regularly
- Verify task flow between directories

### Weekly Operations
- Review completed tasks in Done/
- Archive old tasks if needed
- Check repository health

### Monthly Operations
- Review and rotate any security tokens
- Archive old logs
- Verify backup integrity

This system ensures consistent, conflict-free operation of the AI Employee system across multiple instances while maintaining Git-based synchronization.