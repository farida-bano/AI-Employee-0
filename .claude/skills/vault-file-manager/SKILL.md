# vault-file-manager Skill

**Purpose:** This skill manages the workflow of task files within the `AI_Employee_Vault/` by moving them between different stages (Inbox, Needs_Action, Done).

**Usage for Claude:**
To move a task file, use the following command structure:
`python .claude/skills/vault-file-manager/scripts/move_task.py --filename <filename_with_extension> --source <source_vault_path> --destination <destination_vault_path>`

**Vault Paths:**
-   `Inbox`: AI_Employee_Vault/Inbox/
-   `Needs_Action`: AI_Employee_Vault/Needs_Action/
-   `Done`: AI_Employee_Vault/Done/

**Requirements:**
-   **Inputs:**
    -   `--filename`: The name of the file to move (e.g., `task_review_document.txt.md`).
    -   `--source`: The current vault path of the file (e.g., `Inbox`, `Needs_Action`).
    -   `--destination`: The target vault path for the file (e.g., `Needs_Action`, `Done`).

**Output:**
-   Returns `Success: Moved <filename> from <source_path> to <destination_path>.` on successful move.
-   Returns `Error: <error_details>` if the file does not exist, or moving fails.
