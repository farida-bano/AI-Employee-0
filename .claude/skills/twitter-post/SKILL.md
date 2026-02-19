# twitter-post Skill

**Purpose:** This skill allows for posting tweets to Twitter (X) and maintains a history of posts in the vault.

**Usage for Claude:**
To post a tweet, use the following command structure:
`python .claude/skills/twitter-post/scripts/post_tweet.py --content "<your_tweet_content>"`

**Requirements:**
-   **Environment Variables:**
    -   `TWITTER_API_KEY`: Your Twitter API Key.
    -   `TWITTER_API_SECRET`: Your Twitter API Secret.
    -   `TWITTER_ACCESS_TOKEN`: Your Twitter Access Token.
    -   `TWITTER_ACCESS_TOKEN_SECRET`: Your Twitter Access Token Secret.
-   **Dependencies:** `requests`, `requests-oauthlib`
-   **Inputs:**
    -   `--content`: The text content of the tweet.

**Output:**
-   Returns `Success: Tweet posted.` on successful posting.
-   Returns `Error: <error_details>` if posting fails.
-   Logs post history to `AI_Employee_Vault/reports/twitter_history.log`.
