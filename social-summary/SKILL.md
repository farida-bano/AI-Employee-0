# Skill: Social Summary

## Description

This skill is responsible for logging a summary of social media posts to a dedicated log file. It is primarily triggered after a LinkedIn post is successfully made by the Business MCP.

## Functionality

Upon being called after a social media post (e.g., LinkedIn):

-   **Save Summary**: A summary of the post is saved to `AI_Employee_Vault/Reports/Social_Log.md`.
-   **Included Information**: Each entry in the log includes:
    -   `platform`: The social media platform where the post was made (e.g., "LinkedIn").
    -   `content`: The textual content of the post.
    -   `date`: The date and time when the post was made.

## Output

-   **Log File**: `AI_Employee_Vault/Reports/Social_Log.md` (appended entries)

## Integration

This skill is designed to be integrated with other social media posting functionalities, such as the `post_linkedin` tool in the Business MCP server, which will call this skill after a successful post.
