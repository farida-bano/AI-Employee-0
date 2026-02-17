# human-approval Skill

**Purpose:** This skill facilitates human-in-the-loop approval for sensitive actions. It creates an approval request and waits for a human to review and mark it as 'APPROVED' or 'REJECTED'.

**Usage for Claude:**
To request human approval, use the following command structure:
`python .claude/skills/human-approval/scripts/request_approval.py --action_details "<details_of_action>" --approval_id <unique_id>`

**Requirements:**
-   **Inputs:**
    -   `--action_details`: A description of the action requiring approval. This will be written to a file in `AI_Employee_Vault/Need_Approval/`.
    -   `--approval_id`: A unique identifier for this approval request. This will be used as the filename.

**Process:**
1.  A file named `<approval_id>.md` is created in `AI_Employee_Vault/Need_Approval/` with the `action_details`.
2.  The script continuously monitors this file.
3.  A human must manually edit the file to contain either "APPROVED" or "REJECTED" (case-insensitive) as the first line.

**Output:**
-   Returns `Status: APPROVED` if the file is updated with "APPROVED".
-   Returns `Status: REJECTED` if the file is updated with "REJECTED".
-   Returns `Error: <error_details>` if an error occurs during the process.
