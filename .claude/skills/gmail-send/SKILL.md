# gmail-send Skill

**Purpose:** This skill enables sending real emails using SMTP. It's designed for automated communication within workflows, such as sending notifications, reports, or task summaries.

**Usage for Claude:**
To send an email, use the following command structure:
`python .claude/skills/gmail-send/scripts/send_email.py --to <recipient_email> --subject <email_subject> --body <email_body>`

**Requirements:**
-   **Environment Variables:**
    -   `EMAIL_ADDRESS`: The sender's email address (e.g., your Gmail address).
    -   `EMAIL_PASSWORD`: The app-specific password for the `EMAIL_ADDRESS`. (Do NOT use your main account password).
-   **Inputs:**
    -   `--to`: Recipient's email address.
    -   `--subject`: Subject line of the email.
    -   `--body`: Body content of the email.

**Output:**
-   Returns `Success: Email sent to <recipient_email>` on successful delivery.
-   Returns `Error: <error_details>` if sending fails.
