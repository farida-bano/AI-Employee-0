# linkedin-post Skill

**Purpose:** This skill allows for creating real LinkedIn text posts using browser automation with Playwright. It's useful for automated content sharing or updates.

**Usage for Claude:**
To create a LinkedIn post, use the following command structure:
`python .claude/skills/linkedin-post/scripts/post_linkedin.py --content "<your_post_content>"`

**Requirements:**
-   **Environment Variables:**
    -   `LINKEDIN_EMAIL`: Your LinkedIn login email.
    -   `LINKEDIN_PASSWORD`: Your LinkedIn login password.
-   **Dependencies:** Playwright must be installed (`pip install playwright`) and its browsers must be installed (`playwright install`).
-   **Inputs:**
    -   `--content`: The text content of the LinkedIn post.

**Output:**
-   Returns `Success: LinkedIn post created.` on successful posting.
-   Returns `Error: <error_details>` if posting fails (e.g., login issues, Playwright errors).
