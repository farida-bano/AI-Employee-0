# Silver Scheduler Skill

This skill provides scheduling capabilities for the AI Employee system.

## Goal
- Run `vault-watcher` and `task-planner` in a loop.
- Default interval: 5 minutes.
- Support command-line modes: `daemon`, `once`, `status`.
- Log all actions to `logs/ai_employee.log`.
- Rotate logs at 5MB.
- Prevent duplicate instances with lock files.

## Usage

The scheduler is controlled via the `Scripts/run_ai_employee` script.

### Modes

The script supports three primary modes of operation, specified as the first argument: `daemon`, `once`, and `status`.

#### `daemon` Mode

Runs the `vault-watcher` and `task-planner` continuously in a loop, pausing for a specified interval between runs. This mode also uses a lock file to prevent multiple instances from running concurrently.

```bash
python Scripts/run_ai_employee daemon [--interval <seconds>]
```

- `--interval <seconds>`: Optional. Specifies the delay in seconds between each execution cycle. If not provided, it defaults to 300 seconds (5 minutes).

**Example:**
```bash
python Scripts/run_ai_employee daemon
python Scripts/run_ai_employee daemon --interval 600 # Run every 10 minutes
```

#### `once` Mode

Executes the `vault-watcher` and `task-planner` a single time and then exits.

```bash
python Scripts/run_ai_employee once
```

**Example:**
```bash
python Scripts/run_ai_employee once
```

#### `status` Mode

Displays the current count of files in the `Bronze/Needs_Action` directory (active tasks) and the `Bronze/Inbox` directory (inbox items).

```bash
python Scripts/run_ai_employee status
```

**Example:**
```bash
python Scripts/run_ai_employee status
```

### Logging

All actions and output are logged to `logs/ai_employee.log`. The log file is configured to rotate at 5MB, keeping up to 5 backup files.
