# Skill: Error Recovery

## Description

This skill provides a basic error recovery mechanism for file-based operations within the AI Employee system. When an error occurs during the processing of a file, this skill logs the error, quarantines the problematic file, and signals for a potential retry.

## Functionality

Upon invocation with an error:

1.  **Log Error**: The error details, along with a timestamp and the path to the problematic file, are appended to `logs/errors.log`. A note is included to indicate that a retry for the operation on the file is requested.
2.  **Quarantine File**: The file that caused the error is moved from its original location to `AI_Employee_Vault/Errors/`. The file is renamed with a timestamp to prevent name collisions and provide a history of errors.
3.  **Retry Signal**: The skill signals for a retry of the original operation on the file after a 5-minute delay. The actual retry mechanism needs to be implemented by the calling component (e.g., a scheduler or task processor) that detects the error and invokes this skill.

## Usage

This skill is designed to be called by other system components when an unrecoverable error is encountered during file processing. It should be provided with the path to the problematic file and the details of the error.

Example (conceptual):
`handle_error(file_path="/path/to/problematic_file.txt", error_message="File processing failed due to invalid format.")`

## Output

-   **Log File**: `logs/errors.log` (appended entries)
-   **Quarantine Directory**: `AI_Employee_Vault/Errors/` (moved files)
