---
name: make-plan-for-tasks
description: Analyzes pending tasks in the 'Needs_Action' directory and creates a plan file. Use when the user says "make a plan for tasks".
---

# Make Plan for Tasks

## Overview

This skill analyzes all pending tasks in the `Bronze/Needs_Action` directory and generates a markdown plan file in the `Bronze/Plans` directory. This plan helps in organizing and strategizing the execution of pending tasks.

## Workflow

When the user asks to "make a plan for tasks", you must follow these steps:

1.  **Read Task Files:**
    *   List all the files present in the `Bronze/Needs_Action/` directory.
    *   If the directory is empty, inform the user that there are no pending tasks and stop.

2.  **Analyze Tasks:**
    *   For each file in the `Needs_Action` directory, read its content to understand the task.
    *   The file name itself (e.g., `task_review_client_document.txt.md`) gives a good summary of the task.

3.  **Create Plan File:**
    *   Generate a timestamp in the format `YYYYMMDDHHMMSS`.
    *   Create a new file named `Plan_<timestamp>.md` in the `Bronze/Plans/` directory.

4.  **Populate the Plan File:**
    *   Structure the plan file with the following sections:
        *   `# Pending Tasks Plan - <Date>`
        *   `## Summary of Pending Tasks`
        *   `## Suggested Order of Execution`
        *   `## Risks and Unclear Items`
        *   `## Strategy`

    *   **Summary of Pending Tasks:**
        *   List each task file from the `Needs_Action` directory. Briefly describe the task based on its filename and content.

    *   **Suggested Order of Execution:**
        *   Propose a logical order to execute the tasks. For now, a simple sequential order is acceptable. You can suggest prioritizing tasks based on keywords like "client" or "urgent" if found in the task files.

    *   **Risks and Unclear Items:**
        *   Review the tasks and identify any potential risks, dependencies, or ambiguous instructions. For example, a task to "review a document" might be risky if the document is missing. Note these down.

    *   **Strategy:**
        *   Write a short paragraph outlining the overall approach to completing the tasks. This could involve grouping similar tasks, or a general statement about the focus of the work.

**Important:** This skill is for planning purposes only. Do not execute the tasks themselves.
