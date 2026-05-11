# AI Employee System - Quick Start Guide

## 📋 Project Overview
This is an autonomous AI Employee system that:
- Monitors task files in `Bronze/Inbox`
- Processes tasks through the Ralph Wiggum Loop
- Generates CEO briefings
- Logs business activities
- Handles errors and approvals

---

## 🚀 Step-by-Step Setup & Run Instructions

### Step 1: Navigate to Project Directory
```bash
cd /Users/sarosh/Desktop/AI-Employee
```

### Step 2: Create Python Virtual Environment
```bash
python3 -m venv venv
```

### Step 3: Activate Virtual Environment
```bash
source venv/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install fastapi uvicorn watchdog mcp-server
```

If you encounter SSL certificate issues, use:
```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org fastapi uvicorn watchdog mcp-server
```

### Step 5: Create Required Directories
```bash
mkdir -p Bronze/Inbox
mkdir -p Bronze/Needs_Action
mkdir -p Bronze/Done
mkdir -p AI_Employee_Vault/logs
mkdir -p logs
```

### Step 6: Start the Business MCP Server (Background)
```bash
python3 mcp/business_mcp/server.py &
```
This server provides email, LinkedIn, and logging tools. It runs on `http://127.0.0.1:8000`

### Step 7: Run the AI Employee Scheduler

Choose one of these modes:

#### Option A: Run Once (Single Pass)
```bash
python3 scripts/run_ai_employee once
```
Processes all pending tasks and generates reports, then exits.

#### Option B: Run in Daemon Mode (Continuous - Recommended)
```bash
python3 scripts/run_ai_employee daemon --interval 300
```
Runs continuously, checking for new tasks every 5 minutes (300 seconds).

#### Option C: Check Status
```bash
python3 scripts/run_ai_employee status
```
Shows pending tasks and inbox items without processing.

---

## 📝 How to Create Tasks

1. Create a markdown file in `Bronze/Inbox/`:
```bash
cat > Bronze/Inbox/my_task.md << 'EOF'
# My Task

Create a new file named `output.txt` in the root directory of the project and write the string "Hello from Ralph" into it.
EOF
```

2. The system will automatically:
   - Detect the new file
   - Create a task in `Bronze/Needs_Action/`
   - Process it through Ralph Wiggum Loop
   - Move it to `Bronze/Done/` on success

---

## 📊 Monitoring & Logs

Check these files to monitor system activity:

- **General Activity**: `logs/ai_employee.log`
- **Business Activity**: `AI_Employee_Vault/logs/business.log`
- **Errors**: `AI_Employee_Vault/logs/errors.log`
- **System Log**: `Bronze/System_log.md`
- **CEO Briefing**: `AI_Employee_Vault/Reports/CEO_Weekly.md`
- **Social Posts**: `AI_Employee_Vault/Reports/Social_Log.md`
- **Quarantined Files**: `AI_Employee_Vault/Errors/`

---

## 🔧 Project Structure

```
AI-Employee/
├── Bronze/                          # Core task management
│   ├── Inbox/                       # New task files go here
│   ├── Needs_Action/                # Tasks waiting to be processed
│   ├── Done/                        # Completed tasks
│   ├── file_watcher.py              # Monitors Inbox for new files
│   └── System_log.md                # Activity log
├── AI_Employee_Vault/               # Central storage
│   ├── logs/                        # System logs
│   ├── Reports/                     # Generated reports
│   ├── Errors/                      # Quarantined problematic files
│   └── personal/                    # Personal task management
├── scripts/
│   ├── run_ai_employee              # Main scheduler (Python script)
│   ├── ralph_wiggum_loop.py         # Task execution engine
│   ├── task_planner.py              # Task planning
│   └── request_approval.py          # Approval requests
├── mcp/
│   └── business_mcp/
│       └── server.py                # Business tools server
├── ceo-briefing/                    # CEO briefing generation
├── social-summary/                  # Social media logging
└── .claude/skills/                  # Custom skills
    ├── error-recovery/              # Error handling
    ├── human-approval/              # Approval workflow
    └── vault-file-manager/          # File management
```

---

## 🎯 Complete Workflow Example

### Terminal 1: Start MCP Server
```bash
cd /Users/sarosh/Desktop/AI-Employee
source venv/bin/activate
python3 mcp/business_mcp/server.py
```

### Terminal 2: Run Scheduler in Daemon Mode
```bash
cd /Users/sarosh/Desktop/AI-Employee
source venv/bin/activate
python3 scripts/run_ai_employee daemon --interval 300
```

### Terminal 3: Create a Task
```bash
cd /Users/sarosh/Desktop/AI-Employee
cat > Bronze/Inbox/test_task.md << 'EOF'
# Test Task

Create a new file named `test_output.txt` in the root directory of the project and write the string "Hello from Ralph" into it.
EOF
```

The system will automatically:
1. Detect the new file in `Bronze/Inbox/`
2. Create `Bronze/Needs_Action/task_review_test_task.md`
3. Process it through Ralph Wiggum Loop
4. Create `test_output.txt` with the content
5. Move the task to `Bronze/Done/`

---

## ⚠️ Troubleshooting

### Issue: "Another instance is already running"
The daemon mode uses a lock file. If it crashes, remove the lock:
```bash
rm ai_employee.lock
```

### Issue: "Script not found" errors
Ensure you're running from the project root directory:
```bash
cd /Users/sarosh/Desktop/AI-Employee
```

### Issue: MCP Server won't start
Check if port 8000 is already in use:
```bash
lsof -i :8000
```

### Issue: Tasks not being processed
1. Check `logs/ai_employee.log` for errors
2. Verify `Bronze/Inbox/` has files
3. Check `Bronze/Needs_Action/` for pending tasks
4. Run `python3 scripts/run_ai_employee status` to see current state

---

## 🛑 Stopping the System

### Stop Daemon Mode
Press `Ctrl+C` in the terminal running the daemon

### Stop MCP Server
Press `Ctrl+C` in the terminal running the server, or:
```bash
pkill -f "python3 mcp/business_mcp/server.py"
```

---

## 📚 Additional Resources

- **Main README**: `README.md`
- **Setup Guide**: `SETUP_FOR_CLAUDE.md`
- **Project Overview**: `haackathon0/AI Employee Project Complete Overview.md`
- **Processing Logic**: `processing_logic.md`
- **Conflict Handling**: `conflict_handling.md`
