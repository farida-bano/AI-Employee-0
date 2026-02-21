# AI Employee Vault - Conflict Handling Instructions

## Overview
This document outlines strategies and procedures to handle potential conflicts in the AI Employee vault system when multiple instances (cloud and local) are syncing via Git.

## Types of Conflicts

### 1. Dashboard.md Conflicts
- **Issue**: Multiple instances trying to update the dashboard simultaneously
- **Solution**: Single-writer rule using file locking mechanism

### 2. Task File Conflicts
- **Issue**: Same task being processed by multiple instances
- **Solution**: Claim-by-move rule where moving a task file claims it for processing

### 3. Directory Content Conflicts
- **Issue**: Different instances adding different files to the same directory
- **Solution**: Git merge handles this naturally as long as filenames are unique

## Conflict Prevention Strategies

### Single-Writer Rule for Dashboard.md
1. Before updating Dashboard.md, acquire an exclusive lock using the dashboard_manager.py
2. Only one process can hold the lock at a time
3. Other processes must wait or queue their updates
4. Lock is automatically released after the update is complete

### Claim-by-Move Rule for Tasks
1. When a process identifies a task to work on, it moves the task file to its processing directory
2. Moving the file acts as claiming the task
3. Other instances will not see the moved file, preventing duplicate processing
4. If move fails (file already moved), the task is already claimed

## Handling Merge Conflicts

### Automatic Conflict Resolution
The sync.sh script includes automatic conflict resolution for Dashboard.md:
1. When a merge conflict occurs in Dashboard.md, the system preserves content from both versions
2. Local tasks and cloud tasks are kept in separate sections
3. A backup of the original file is created before conflict resolution

### Manual Conflict Resolution
If automatic resolution fails:

1. Check current conflicts:
   ```bash
   git status
   git diff
   ```

2. Manually resolve Dashboard.md conflicts:
   ```bash
   # Open the file to see conflict markers
   vim AI_Employee_Vault/Dashboard.md
   ```

3. Merge other conflicted files as appropriate

4. Mark conflicts as resolved:
   ```bash
   git add .
   git commit -m "Resolve conflicts manually"
   ```

## Best Practices

### 1. Task Processing Workflow
- Always use dashboard_manager.py claim_by_move function to claim tasks
- Do not directly move files without using the manager
- Always update dashboard through dashboard_manager.py with lock mechanism

### 2. Git Operations
- Run sync operations during low-activity periods when possible
- Monitor logs for conflict warnings
- Use the sync.sh script for all Git operations rather than direct commands

### 3. Monitoring
- Check logs regularly: `tail -f logs/vault_sync.log`
- Monitor dashboard status: `python dashboard_manager.py status`
- Set up alerts for failed sync operations

## Recovery Procedures

### If Dashboard Gets Corrupted
1. Restore from the latest backup:
   ```bash
   # Find backup files created during conflict resolution
   ls -la AI_Employee_Vault/Dashboard.md.backup.*
   cp AI_Employee_Vault/Dashboard.md.backup.<timestamp> AI_Employee_Vault/Dashboard.md
   ```

2. Force push the restored version:
   ```bash
   git add AI_Employee_Vault/Dashboard.md
   git commit -m "Restore dashboard from backup"
   git push origin main --force-with-lease  # Use --force-with-lease for safety
   ```

### If Sync Process Gets Stuck
1. Check for lock files:
   ```bash
   ls -la AI_Employee_Vault/.dashboard.lock AI_Employee_Vault/.dashboard_claim.json
   ```

2. Remove lock files if the process holding them is no longer active:
   ```bash
   rm -f AI_Employee_Vault/.dashboard.lock AI_Employee_Vault/.dashboard_claim.json
   ```

### If Git Repository Gets Corrupted
1. Restore from a known good state:
   ```bash
   # Find a good commit hash
   git log --oneline -10

   # Reset to the good state (with caution!)
   git reset --hard <good-commit-hash>
   git push origin main --force-with-lease
   ```

## Emergency Procedures

### Immediate Conflict Response
1. Stop all AI Employee processes:
   ```bash
   pm2 stop all
   ```

2. Check repository status:
   ```bash
   git status
   ```

3. Resolve conflicts manually if needed

4. Restart processes:
   ```bash
   pm2 start all
   ```

### Data Integrity Check
Run this script periodically to verify data consistency:
```bash
#!/bin/bash
# integrity_check.sh

echo "Checking vault integrity..."

# Check for missing directories
for dir in "Needs_Action" "Pending_Approval" "Approved" "In_Progress" "Done" "Errors" "Inbox"; do
    if [ ! -d "AI_Employee_Vault/$dir" ]; then
        echo "MISSING: AI_Employee_Vault/$dir"
    fi
done

# Check dashboard integrity
if [ ! -f "AI_Employee_Vault/Dashboard.md" ]; then
    echo "CRITICAL: Dashboard.md is missing!"
else
    echo "Dashboard.md exists, checking format..."
    head -10 AI_Employee_Vault/Dashboard.md
fi

echo "Integrity check complete."
```

## Logging and Monitoring

All conflict detection and resolution attempts are logged to `logs/vault_sync.log`:
- Timestamp of each sync attempt
- Details of any conflicts found
- Actions taken to resolve conflicts
- Status of dashboard lock operations

## Testing Conflict Scenarios

Before deploying, test these scenarios:
1. Two processes trying to update Dashboard.md simultaneously
2. Two processes trying to claim the same task
3. Git pull during active processing
4. Network interruption during sync