#!/bin/bash

# AI Employee System - Automated Setup Script
# This script sets up and runs the AI Employee system

set -e  # Exit on error

PROJECT_DIR="/Users/sarosh/Desktop/AI-Employee"
cd "$PROJECT_DIR"

echo "=========================================="
echo "AI Employee System - Setup & Run"
echo "=========================================="
echo ""

# Step 1: Create virtual environment
echo "📦 Step 1: Creating Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Step 2: Activate virtual environment
echo ""
echo "🔌 Step 2: Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

# Step 3: Install dependencies
echo ""
echo "📥 Step 3: Installing dependencies..."
pip install -q fastapi uvicorn watchdog mcp-server 2>/dev/null || \
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -q fastapi uvicorn watchdog mcp-server
echo "✓ Dependencies installed"

# Step 4: Create required directories
echo ""
echo "📁 Step 4: Creating required directories..."
mkdir -p Bronze/Inbox
mkdir -p Bronze/Needs_Action
mkdir -p Bronze/Done
mkdir -p AI_Employee_Vault/logs
mkdir -p logs
echo "✓ Directories created"

# Step 5: Display next steps
echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo ""
echo "1️⃣  Start the Business MCP Server (in Terminal 1):"
echo "   python3 mcp/business_mcp/server.py"
echo ""
echo "2️⃣  Run the AI Employee Scheduler (in Terminal 2):"
echo "   python3 scripts/run_ai_employee daemon --interval 300"
echo ""
echo "3️⃣  Create a test task (in Terminal 3):"
echo "   cat > Bronze/Inbox/test_task.md << 'EOF'"
echo "   # Test Task"
echo "   Create a new file named \`test_output.txt\` in the root directory of the project and write the string \"Hello from Ralph\" into it."
echo "   EOF"
echo ""
echo "📊 Monitor logs:"
echo "   - logs/ai_employee.log (main activity)"
echo "   - Bronze/System_log.md (system events)"
echo "   - AI_Employee_Vault/logs/business.log (business activities)"
echo ""
echo "For more details, see QUICKSTART.md"
echo ""
