import os
import sys
import datetime

SOCIAL_LOG_FILE = os.path.join("AI_Employee_Vault", "Reports", "Social_Log.md")

def log_social_post(platform: str, content: str, post_date: str):
    """
    Logs a social media post summary to a Markdown file.

    Args:
        platform: The social media platform (e.g., "LinkedIn", "X").
        content: The content of the post.
        post_date: The date and time of the post (ISO format recommended).
    """
    # Ensure the Reports directory exists
    os.makedirs(os.path.dirname(SOCIAL_LOG_FILE), exist_ok=True)

    log_entry = f"""
---
Platform: {platform}
Date: {post_date}
Content:
  {content}
---
"""
    with open(SOCIAL_LOG_FILE, "a") as f:
        f.write(log_entry)
    
    print(f"Social media post summary logged to {SOCIAL_LOG_FILE}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python log_social_post.py <platform> <content> <date>")
        sys.exit(1)
    
    platform = sys.argv[1]
    content = sys.argv[2]
    post_date = sys.argv[3]
    
    log_social_post(platform, content, post_date)
