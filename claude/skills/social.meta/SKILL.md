# social.meta Skill

**Purpose:** This skill allows for posting content to Facebook and Instagram via the Meta Graph API.

**Usage for Claude:**
To post to Facebook:
`python claude/skills/social.meta/scripts/post_meta.py --platform facebook --content "<your_content>"`

To post to Instagram:
`python claude/skills/social.meta/scripts/post_meta.py --platform instagram --content "<your_content>" --image_url "<image_url>"`

**Requirements:**
-   **Environment Variables:**
    -   `FACEBOOK_PAGE_ACCESS_TOKEN`: Your Facebook Page Access Token.
    -   `FACEBOOK_PAGE_ID`: Your Facebook Page ID.
    -   `INSTAGRAM_ACCESS_TOKEN`: Your Instagram Access Token.
    -   `INSTAGRAM_ACCOUNT_ID`: Your Instagram Account ID.
-   **Dependencies:** `requests`
-   **Inputs:**
    -   `--platform`: `facebook` or `instagram`.
    -   `--content`: The text content of the post.
    -   `--image_url`: (Required for Instagram) The URL of the image to post.

**Output:**
-   Returns `Success: <platform> post created.` on success.
-   Returns `Error: <error_details>` if posting fails.
-   Logs post history to `logs/social/log`.
