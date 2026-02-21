# Project Tracking and Updates

This note explains how developers can track updates to files and folders in the AI Employee project, and how this is reflected in Obsidian.

## File and Folder Tracking

### Git for Version Control
- Use Git to track changes to all project files
- Each commit records what files were modified, added, or deleted
- The `.git` folder stores all version history

### Obsidian Integration
- All project files can be referenced in Obsidian notes
- When files are updated, the changes are visible in the Obsidian vault
- Links to files and folders create a graph of relationships

### Update Tracking Methods
1. **Git Commands**:
   - `git status` - Shows modified files
   - `git log` - Shows commit history
   - `git diff` - Shows changes in files

2. **File Watchers**:
   - Scripts like `watchdog.py` monitor file changes
   - Automatic notifications when files are created/modified

3. **Log Files**:
   - Stored in [[AI_Employee_Vault/logs|AI_Employee_Vault/logs/]]
   - Track system operations and file changes
   - Monitor progress and identify issues

## Visualizing Updates in Obsidian

### Graph View
- All linked notes appear as nodes in the graph
- Connections show relationships between different parts of the project
- New files automatically appear when linked from existing notes

### Daily Notes
- Create daily notes to track what files were worked on
- [[AI_Employee_Vault/Briefings|AI_Employee_Vault/Briefings/]] can contain daily updates
- Link to specific files and folders to show activity

### Tagging System
- Use tags like #updated, #new-file, #modified to mark recent changes
- Create queries to see recently updated files
- Color-code different types of updates in the graph view

## Best Practices
- Keep notes updated with links to related files
- Use consistent naming for files and folders
- Document changes in corresponding notes
- Link code files to design documents
- Track dependencies between different parts of the project