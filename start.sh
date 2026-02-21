#!/bin/bash

# AI Employee Start Script

# Change to the project directory (adjust as needed)
cd /opt/ai-employee || cd /home/ubuntu/ai-employee || cd .

# Activate Python virtual environment
source venv/bin/activate

# Create logs directory if it doesn't exist
mkdir -p logs

# Start the Business MCP Server (required for social and email actions)
echo "Starting Business MCP Server..."
python3 mcp/business_mcp/server.py > logs/mcp_server.log 2>&1 &

# Wait a moment for the server to start
sleep 2

# Start the File Watcher
echo "Starting File Watcher..."
python3 Bronze/file_watcher.py > logs/file_watcher.log 2>&1 &

# Start the AI Employee Scheduler in daemon mode
echo "Starting AI Employee Scheduler..."
python3 scripts/run_ai_employee daemon --interval 300 > logs/ai_employee_scheduler.log 2>&1 &

echo "AI Employee services started successfully!"
echo "Business MCP Server PID: $(pgrep -f 'server.py')"
echo "File Watcher PID: $(pgrep -f 'file_watcher.py')"
echo "Scheduler PID: $(pgrep -f 'run_ai_employee')"