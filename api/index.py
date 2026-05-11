from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import json
from datetime import datetime
from pathlib import Path

app = FastAPI()

# Enable CORS for Vercel frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).parent.parent

@app.get("/")
def read_root():
    return {"status": "AI Employee API is running"}

@app.get("/api/tasks")
def get_tasks():
    """Get all tasks from Bronze folders"""
    tasks = {
        "inbox": [],
        "needs_action": [],
        "done": []
    }

    # Read Inbox
    inbox_path = BASE_DIR / "Bronze" / "Inbox"
    if inbox_path.exists():
        for file in inbox_path.glob("*.md"):
            tasks["inbox"].append({
                "name": file.stem,
                "path": str(file),
                "modified": datetime.fromtimestamp(file.stat().st_mtime).isoformat()
            })

    # Read Needs_Action
    needs_action_path = BASE_DIR / "Bronze" / "Needs_Action"
    if needs_action_path.exists():
        for file in needs_action_path.glob("*.md"):
            content = file.read_text()
            tasks["needs_action"].append({
                "name": file.stem,
                "path": str(file),
                "content": content[:200] + "..." if len(content) > 200 else content,
                "modified": datetime.fromtimestamp(file.stat().st_mtime).isoformat()
            })

    # Read Done
    done_path = BASE_DIR / "Bronze" / "Done"
    if done_path.exists():
        for file in done_path.glob("*.md"):
            tasks["done"].append({
                "name": file.stem,
                "path": str(file),
                "modified": datetime.fromtimestamp(file.stat().st_mtime).isoformat()
            })

    return tasks

@app.get("/api/logs")
def get_logs():
    """Get recent logs"""
    logs = {
        "system": [],
        "errors": [],
        "business": []
    }

    # Read system log
    system_log = BASE_DIR / "logs" / "ai_employee.log"
    if system_log.exists():
        lines = system_log.read_text().splitlines()
        logs["system"] = lines[-50:] if len(lines) > 50 else lines

    # Read error log
    error_log = BASE_DIR / "logs" / "errors.log"
    if error_log.exists():
        lines = error_log.read_text().splitlines()
        logs["errors"] = lines[-50:] if len(lines) > 50 else lines

    # Read business log
    business_log = BASE_DIR / "AI_Employee_Vault" / "logs" / "business.log"
    if business_log.exists():
        lines = business_log.read_text().splitlines()
        logs["business"] = lines[-50:] if len(lines) > 50 else lines

    return logs

@app.get("/api/reports")
def get_reports():
    """Get available reports"""
    reports = []

    reports_path = BASE_DIR / "AI_Employee_Vault" / "Reports"
    if reports_path.exists():
        for file in reports_path.glob("*.md"):
            content = file.read_text()
            reports.append({
                "name": file.stem,
                "path": str(file),
                "content": content,
                "modified": datetime.fromtimestamp(file.stat().st_mtime).isoformat()
            })

    return reports

@app.get("/api/stats")
def get_stats():
    """Get system statistics"""
    stats = {
        "inbox_count": 0,
        "needs_action_count": 0,
        "done_count": 0,
        "error_count": 0,
        "last_updated": datetime.now().isoformat()
    }

    inbox_path = BASE_DIR / "Bronze" / "Inbox"
    if inbox_path.exists():
        stats["inbox_count"] = len(list(inbox_path.glob("*.md")))

    needs_action_path = BASE_DIR / "Bronze" / "Needs_Action"
    if needs_action_path.exists():
        stats["needs_action_count"] = len(list(needs_action_path.glob("*.md")))

    done_path = BASE_DIR / "Bronze" / "Done"
    if done_path.exists():
        stats["done_count"] = len(list(done_path.glob("*.md")))

    errors_path = BASE_DIR / "AI_Employee_Vault" / "Errors"
    if errors_path.exists():
        stats["error_count"] = len(list(errors_path.glob("*")))

    return stats
