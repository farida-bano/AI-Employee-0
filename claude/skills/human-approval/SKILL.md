# Human Approval Skill

This skill allows for human intervention and approval in workflows. It monitors a specific file in the `AI_Employee_Vault/Need_Approval` folder for "APPROVED" or "REJECTED" keywords, blocking execution until a decision is made or a timeout occurs.

## Goal
- Monitor `AI-Employee_Vault/Need_Approval` folder for approval requests.
- Block execution until a human writes `APPROVED` or `REJECTED` in the monitored file.
- Rename the file to `.approved`, `.rejected`, or `.timeout` based on the outcome.
- Timeout after a configurable duration (default 1 hour).
- Log all actions in `logs/action.log`.

## Usage

The approval process is initiated by running the `Scripts/request_approval.py` script.

### `request_approval.py`

This script monitors a single file within the `AI_Employee_Vault/Need_Approval` directory. The file should be created manually or by another process in that folder.

```bash
python Scripts/request_approval.py <file_to_monitor> [--timeout <seconds>]
```

- `<file_to_monitor>`: The name of the file (e.g., `my_task_approval.txt`) located in `AI_Employee_Vault/Need_Approval` that needs human review. The script expects this file to exist in that folder.
- `--timeout <seconds>`: Optional. Specifies the maximum duration in seconds the script will wait for approval or rejection. If not provided, it defaults to 3600 seconds (1 hour).

**Example:**

1.  **Create an approval request file:**
    ```bash
    echo "Please review this task for approval." > AI_Employee_Vault/Need_Approval/my_task_approval.txt
    ```
2.  **Run the approval agent:**
    ```bash
    python Scripts/request_approval.py my_task_approval.txt --timeout 1800 # Wait for 30 minutes
    ```

### Workflow

1.  A file (e.g., `my_task_approval.txt`) is placed in the `AI_Employee_Vault/Need_Approval` directory.
2.  The `request_approval.py` script is executed, specifying the name of the file to monitor.
3.  The script will continuously check the content of the specified file.
4.  **For Approval:** A human user should open `AI_Employee_Vault/Need_Approval/my_task_approval.txt` and add the word `APPROVED` (case-insensitive, on its own line or within existing text).
5.  **For Rejection:** A human user should open `AI_Employee_Vault/Need_Approval/my_task_approval.txt` and add the word `REJECTED` (case-insensitive, on its own line or within existing text).
6.  Upon detecting `APPROVED` or `REJECTED`, the script will rename the file to `my_task_approval.txt.approved` or `my_task_approval.txt.rejected` respectively, and then exit.
7.  **Timeout:** If neither `APPROVED` nor `REJECTED` is found within the specified `--timeout` period, the script will rename the file to `my_task_approval.txt.timeout` and then exit.

### Logging

All actions and outcomes of the approval process are logged to `logs/action.log`.
