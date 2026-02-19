# personal-tasks Skill

**Purpose:** This skill manages personal tasks within the personal domain of the AI Employee. It provides a complete workflow for personal task management including reading tasks, processing them, updating status, and organizing them across the Inbox/Needs_Action/Done lifecycle.

**Environment Variables:**
- `PERSONAL_VAULT_PATH`: Optional path to the personal vault directory (default: AI_Employee_Vault/personal)
- `PERSONAL_TASK_LOG_PATH`: Optional path for the personal task log (default: AI_Employee_Vault/personal/tasks.md)

**Usage for Claude:**
To process a personal task file, use the following command structure:
`python .claude/skills/personal-tasks/scripts/handle_personal_task.py --task-path <path_to_task_file>`

**Requirements:**
- **Inputs:**
  - `--task-path`: The full path to the personal task file to be processed. The file should contain either plain content or content with YAML frontmatter.

**Task File Format:**
Personal task files can include YAML frontmatter to specify metadata:
```
---
priority: high
category: scheduling
status: pending
---
Content of the personal task goes here. This could be scheduling an appointment, creating a reminder, sending an email, or any other personal task.
```

**Expected Directory Structure:**
- `AI_Employee_Vault/personal/Inbox/` - New personal tasks awaiting processing
- `AI_Employee_Vault/personal/Needs_Action/` - Personal tasks ready to be executed
- `AI_Employee_Vault/personal/Done/` - Completed personal tasks
- `AI_Employee_Vault/personal/Logs/` - Personal task logs

**Output:**
- Returns `Personal task completed successfully and moved to Done: <filename>` on successful completion and file move.
- Returns `Personal task completed but failed to move to Done folder: <result>` if the task processing succeeds but the file move fails.
- Returns `Error: <error_details>` if the task processing fails.
- Logs all activities to `AI_Employee_Vault/personal/Logs/personal_tasks.log`

**Supported Task Types (Execution Logic):**
- Scheduling tasks (when content contains "schedule" or "appointment")
- Note/reminder tasks (when content contains "note" or "reminder")
- Email/contact tasks (when content contains "email" or "contact")
- Todo tasks (when content contains "todo" or "task")
- Generic tasks (for all other content)

**Error Handling:**
- Comprehensive error logging for troubleshooting
- Graceful degradation when environment variables are not set
- Proper file handling with existence checks
- Exception handling at every operation level
