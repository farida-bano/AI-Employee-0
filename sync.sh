#!/bin/bash

# Git-based vault synchronization script
# This script handles Git operations for the AI Employee vault system

VAULT_ROOT="AI_Employee_Vault"
LOG_FILE="logs/vault_sync.log"
DASHBOARD_FILE="$VAULT_ROOT/Dashboard.md"

# Function to log messages
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# Function to handle dashboard merge conflicts
handle_dashboard_conflict() {
    log_message "Dashboard conflict detected, handling with single-writer rule..."

    # If we have a conflict in Dashboard.md, use a merge strategy that preserves both sections
    if git diff --name-only --diff-filter=U | grep -q "Dashboard.md"; then
        # Get the current local dashboard content
        LOCAL_DASHBOARD="$VAULT_ROOT/Dashboard.md.working"
        REMOTE_DASHBOARD="$VAULT_ROOT/Dashboard.md.remote"

        # Create backup
        cp "$DASHBOARD_FILE" "$DASHBOARD_FILE.backup.$(date +%s)"

        # Try to get both versions
        git show HEAD:Dashboard.md > "$REMOTE_DASHBOARD" 2>/dev/null || true
        cp "$DASHBOARD_FILE" "$LOCAL_DASHBOARD" 2>/dev/null || true

        # Create a merged dashboard preserving content from both versions
        {
            echo "# AI Employee Dashboard"
            echo ""
            echo "## Local Tasks"
            if [ -f "$LOCAL_DASHBOARD" ]; then
                grep -v "^#\|^$\|##" "$LOCAL_DASHBOARD" || echo "No local tasks"
            else
                echo "No local tasks"
            fi
            echo ""
            echo "## Cloud Tasks"
            if [ -f "$REMOTE_DASHBOARD" ]; then
                grep -v "^#\|^$\|##" "$REMOTE_DASHBOARD" || echo "No cloud tasks"
            else
                echo "No cloud tasks"
            fi
            echo ""
            echo "Last updated: $(date)"
        } > "$DASHBOARD_FILE"

        # Add the resolved dashboard
        git add "$DASHBOARD_FILE"
        rm -f "$LOCAL_DASHBOARD" "$REMOTE_DASHBOARD"

        log_message "Dashboard conflict resolved using merge strategy"
    fi
}

# Function to pull changes from remote repository
pull_changes() {
    log_message "Pulling changes from remote repository..."

    # Fetch the latest changes
    if git fetch origin; then
        log_message "Successfully fetched remote changes"

        # Check if there are any changes to pull
        LOCAL=$(git rev-parse HEAD)
        REMOTE=$(git rev-parse origin/main)

        if [ $LOCAL != $REMOTE ]; then
            log_message "Changes detected, merging..."

            # Try to merge changes
            if git merge origin/main --no-commit --no-ff 2>/dev/null; then
                log_message "Successfully merged remote changes"
                # Commit the merge if needed
                git commit -m "Auto-merge from sync script $(date)"
            else
                # Handle merge conflicts
                log_message "Merge conflicts detected"

                # Handle dashboard conflicts specifically
                handle_dashboard_conflict

                # Try to commit the resolution
                git add .
                if ! git commit -m "Resolve conflicts - $(date)"; then
                    log_message "Some conflicts remain, aborting merge"
                    git merge --abort
                fi
            fi

            log_message "Pull completed successfully"
        else
            log_message "No new changes to pull"
        fi
    else
        log_message "Failed to fetch remote changes"
        return 1
    fi
}

# Function to push changes to remote repository
push_changes() {
    log_message "Pushing local changes to remote repository..."

    # Add all changes in the vault directory (excluding logs and sensitive data filtered by .gitignore)
    git add "$VAULT_ROOT/"*.md "$VAULT_ROOT/"*.txt "$VAULT_ROOT/"*.json "$VAULT_ROOT/"*.py

    # Check if there are any changes to commit
    if ! git diff --cached --quiet; then
        # Create commit with timestamp
        COMMIT_MSG="Vault sync $(date '+%Y-%m-%d %H:%M:%S')"
        if git commit -m "$COMMIT_MSG"; then
            log_message "Changes committed locally: $COMMIT_MSG"

            # Push to remote
            if git push origin main; then
                log_message "Successfully pushed changes to remote"
            else
                log_message "Failed to push changes to remote"
                return 1
            fi
        else
            log_message "Failed to commit changes"
            return 1
        fi
    else
        log_message "No local changes to commit"
    fi
}

# Function to initialize git repo if needed
init_repo() {
    if [ ! -d .git ]; then
        log_message "Initializing new Git repository..."
        git init
        git remote add origin $1
        git add .
        git commit -m "Initial commit - AI Employee vault structure"
        git branch -M main
    fi
}

# Main script logic
case "${1:-status}" in
    "pull")
        pull_changes
        ;;
    "push")
        push_changes
        ;;
    "sync")
        log_message "Starting full sync operation..."
        pull_changes
        push_changes
        log_message "Full sync completed"
        ;;
    "setup")
        if [ -z "$2" ]; then
            echo "Usage: $0 setup <repository-url>"
            exit 1
        fi
        init_repo "$2"
        ;;
    "status")
        log_message "Checking repository status..."
        git status --porcelain
        ;;
    *)
        echo "Usage: $0 {pull|push|sync|setup|status}"
        echo "  pull   - Pull changes from remote"
        echo "  push   - Push local changes to remote"
        echo "  sync   - Pull and push (full sync)"
        echo "  setup  - Initialize repository with remote URL"
        echo "  status - Show repository status"
        exit 1
        ;;
esac