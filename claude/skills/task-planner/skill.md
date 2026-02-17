# Task Planner Skill

## Overview
The Task Planner skill reads new markdown files, analyzes their content, generates a step-by-step plan, and manages the lifecycle of these files within the AI Employee Vault.

## Purpose
- Read new `.md` files from the `AI_Employee_Vault/inbox` directory.
- Analyze the content of the `.md` file to create a detailed, step-by-step plan.
- Save the generated plan as `plan.md` in `AI_Employee_Vault/Needs_Action`.
- Ensure idempotency by not reprocessing already handled files.
- Log all actions for auditing and debugging purposes.
- Integrate with file management to move processed files to `AI_Employee_Vault/Done`.
- Designed to be callable by other skills (e.g., Vault Watcher) or scheduler triggers.

## Components
1.  **Input Reader**: Reads the content of the markdown file.
2.  **Plan Generator**: Analyzes the content and generates a structured plan.
3.  **File Mover**: Handles moving files between `Inbox`, `Needs_Action`, and `Done` directories.
4.  **Logger**: Records all skill activities.
5.  **Idempotency Checker**: Ensures files are processed only once.

## Usage
The `task_planner.py` script should be called with the path to the markdown file to be processed.

Example:
`python scripts/task_planner.py /path/to/AI_Employee_Vault/Inbox/new_task.md`

## Output Files
- `claude/skills/task-planner/skill.md` (this file)
- `scripts/task_planner.py`
- `AI_Employee_Vault/Needs_Action/plan.md` (generated plan)
- `AI_Employee_Vault/logs/actions.log` (activity log)
- `AI_Employee_Vault/logs/processed_files.log` (for idempotency tracking)

