# AI Employee System - Bronze Phase (Enhanced)

This project implements the "Bronze Phase" of an autonomous AI Employee system, focusing on file-based task management, external business actions, automated reporting, and robust error handling.

## 🚀 Core Functionality & Autonomous Loops

The AI Employee operates based on a scheduled loop that continuously monitors and processes tasks.

### 1. 📂 Vault Watcher
Monitors the `Bronze/Inbox` directory for new files. When a new file is detected, it triggers the creation of a corresponding task in `Bronze/Needs_Action`.

### 2. 🧠 Ralph Wiggum Autonomous Loop (Task Processor)
This is the core task execution engine. When a task appears in `Bronze/Needs_Action`:
-   **Analyzes Task**: Reads the task file and generates a simple executable plan.
-   **Creates Plan**: Internally, it formulates a step-by-step plan (currently basic parsing for direct commands).
-   **Executes Steps**: Runs each step of the plan, which can involve calling other scripts or performing file operations.
-   **Safety Measures**:
    -   **Max 5 Iterations**: Limits execution to prevent infinite loops.
    -   **Human Approval**: If a step is deemed risky (e.g., involves deletion or external communication), it requests human approval via the `human-approval` skill.
-   **Error Handling**: Integrates with the `Error Recovery` skill to log errors and quarantine problematic files.
-   **Completion**: Moves the task from `Bronze/Needs_Action` to `Bronze/Done` upon successful completion.

### 3. 📧 Business MCP (Managed Component Platform)
A Python-based server exposing external business actions as tools that the AI Employee can utilize.
-   **Send Email**: `send_email(to, subject, body)` - Simulates sending emails.
-   **Create LinkedIn Post**: `post_linkedin(content)` - Simulates creating LinkedIn posts. Automatically triggers the `Social Summary` skill.
-   **Log Business Activity**: `log_activity(message)` - Logs general business activities to `AI_Employee_Vault/logs/business.log`.

### 4. 📈 CEO Briefing Skill
Generates a weekly briefing report for the CEO.
-   **Output**: `AI_Employee_Vault/Reports/CEO_Weekly.md`
-   **Content**: Includes summaries of completed tasks, emails sent, LinkedIn posts, pending approvals, and placeholders for financial and system health data.
-   **Automation**: Runs automatically via the main scheduler on a weekly basis.

### 5. 🌐 Social Summary Skill
Logs summaries of social media posts.
-   **Trigger**: Automatically called after a `post_linkedin` operation from the Business MCP.
-   **Output**: `AI_Employee_Vault/Reports/Social_Log.md`
-   **Content**: Includes platform, content, and date of the post.

### 6. ⚠️ Error Recovery System
Provides a robust mechanism for handling operational errors.
-   **Functionality**:
    -   **Log Error**: Appends error details, timestamp, and file path to `logs/errors.log`.
    -   **Quarantine File**: Moves the problematic file to `AI_Employee_Vault/Errors/` with a timestamped filename.
    -   **Retry Signal**: Signals for a retry of the original operation after a 5-minute delay (caller responsible for actual retry logic).

## 🛠️ Setup and Installation

1.  **Clone the repository**:
    ```bash
    git clone [repository_url]
    cd AI-Employee
    ```
2.  **Create and activate a Python virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Install Python dependencies**:
    ```bash
    pip install fastapi uvicorn mcp-server
    ```
    *(Note: You might encounter SSL certificate issues during installation. If so, try: `pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org fastapi uvicorn mcp-server`)*

## ▶️ Running the System

The core of the AI Employee system is managed by the `scripts/run_ai_employee` scheduler.

### Start the Business MCP Server (Required for Social and Email actions)

This needs to be running in the background for the AI Employee to use its tools.
```bash
python3 mcp/business_mcp/server.py &
```

### Run the AI Employee Scheduler

The scheduler can be run in different modes:

-   **Daemon Mode (Continuous Operation)**:
    Monitors for new tasks, processes them, and runs scheduled reports (e.g., CEO Briefing) continuously.
    ```bash

    python3 scripts/run_ai_employee daemon --interval 300 # Runs every 5 minutes (300 seconds)
    ```
-   **Once Mode (Single Pass)**:
    Performs a single pass of all tasks and scheduled operations, then exits.
    ```bash
    python3 scripts/run_ai_employee once
    ```
-   **Status Mode (Check Status)**:
    Provides a quick overview of pending tasks and inbox items.
    ```bash
    python3 scripts/run_ai_employee status
    ```

## 📝 How to Use & Extend

1.  **Create a New Task**: Place Markdown files (e.g., `new_idea.md`) into the `Bronze/Inbox` directory. The `Vault Watcher` will automatically create a corresponding task in `Bronze/Needs_Action`.
2.  **Tasks for the Ralph Wiggum Loop**: For the `Ralph Wiggum Autonomous Loop` to execute a task, the task description in `Bronze/Needs_Action/*.md` should contain clear, parsable instructions.
    *   **Example Task (in `Bronze/Needs_Action/example_task.md`):**
        ```markdown
        filename: example_task.md
        status: pending

        ## Task: Create a file and write "Hello from Ralph" into it

        Create a new file named `output.txt` in the root directory of the project and write the string "Hello from Ralph" into it.
        ```
    *   The `Ralph Wiggum Loop` will parse this to perform a `write_file` action. More complex tasks will require more sophisticated parsing logic within `ralph_wiggum_loop.py`.

3.  **Monitor Activity**:
    -   Check `logs/ai_employee.log` for general system activity.
    -   Check `logs/errors.log` for any errors encountered.
    -   Review `AI_Employee_Vault/Reports/CEO_Weekly.md` for weekly summaries.
    -   Review `AI_Employee_Vault/Reports/Social_Log.md` for social media post logs.
    -   Inspect `AI_Employee_Vault/Errors/` for quarantined files.

## 📦 Project Structure (Key Directories)

-   `.claude/skills/`: Contains custom skills (e.g., `error-recovery`, `human-approval`).
-   `AI_Employee_Vault/`: Central storage for logs, reports, and managed files.
    -   `Done/`: Completed tasks.
    -   `Errors/`: Quarantined problematic files.
    -   `Inbox/`: New files awaiting processing.
    -   `logs/`: System and business activity logs.
    -   `Need_Approval/`: Tasks awaiting human intervention.
    -   `Reports/`: Generated reports (e.g., CEO Briefing, Social Log).
-   `Bronze/`: Core components for the Bronze phase.
    -   `Needs_Action/`: Tasks waiting to be processed by the `Ralph Wiggum Loop`.
-   `ceo-briefing/`: CEO Briefing skill definition and scripts.
-   `mcp/business_mcp/`: Business MCP server and tools.
-   `scripts/`: Main system scripts, including the scheduler (`run_ai_employee`) and the `ralph_wiggum_loop`.
-   `social-summary/`: Social Summary skill definition and scripts.
