# MCP Executor Skill

## Overview
The MCP Executor skill is responsible for executing external actions triggered by AI workflows, ensuring human-in-the-loop approvals are respected, logging all operations, and handling execution gracefully.

## Purpose
- Accept execution requests from AI workflows (e.g., from a watcher or scheduler).
- Integrate and call external skills for specific actions like sending emails (using `gmail-send-skill`) and posting on LinkedIn (using `linkedin-post-skill`).
- Implement a human-in-the-loop approval mechanism by checking a designated approval folder.
- Log all execution steps and outcomes to a centralized log file.
- Provide robust error handling and retry mechanisms for external actions.

## Components
1.  **Request Handler**: Parses incoming execution requests.
2.  **Approval Manager**: Checks for and respects human approvals.
3.  **External Action Integrator**: Calls other skills (e.g., `gmail-send`, `linkedin-post`).
4.  **Logger**: Records all activities and errors.
5.  **Retry Mechanism**: Handles transient errors by retrying actions.

## Dependencies
- `gmail-send-skill`: Assumed to be an available skill for sending emails.
- `linkedin-post-skill`: Assumed to be an available skill for posting on LinkedIn.

## Configuration
- `AI_Employee_Vault/Need_Approval/`: Directory where approval files are expected. An empty file named after the task ID (e.g., `task_123.approved`) would signify approval.

## Usage
The `mcp_executor.py` script should be called with arguments defining the task to be executed, including the type of action (e.g., "send_email", "post_linkedin") and relevant parameters.

Example:
`python scripts/mcp_executor.py --action send_email --recipient "test@example.com" --subject "Hello" --body "This is a test"`
`python scripts/mcp_executor.py --action post_linkedin --message "Check out my new post!"`

## Output Files
- `claude/skills/mcp-executor/SKILL.md` (this file)
- `scripts/mcp_executor.py`
- `AI_Employee_Vault/logs/actions.log` (shared activity log)

