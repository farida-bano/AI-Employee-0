import os
import subprocess
import datetime # Added for timestamp
import sys
from mcp.server.fastmcp import FastMCP
from linkedin_api import Linkedin
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastMCP(
    name="BusinessMCP",
)

# Path to the social summary script (relative to project root)
LOG_SOCIAL_POST_SCRIPT = os.path.join(
    os.path.dirname(__file__), "..", "..", "social-summary", "scripts", "log_social_post.py"
)

@app.tool()
def send_email(to: str, subject: str, body: str) -> str:
    """
    Sends an email to a specified recipient.

    Args:
        to: The recipient's email address.
        subject: The subject of the email.
        body: The content of the email.

    Returns:
        A confirmation message.
    """
    # In a real-world scenario, you would integrate with an email service
    # like SendGrid, AWS SES, or use Python's smtplib.
    # For this example, we will just log the action.
    print(f"--- EMAIL SENT ---")
    print(f"To: {to}")
    print(f"Subject: {subject}")
    print(f"Body: {body}")
    print(f"------------------")
    return "Email successfully sent (simulated)."

@app.tool()
def post_linkedin(content: str, auto_post: bool = False) -> str:
    """
    Creates a new post on LinkedIn.

    Args:
        content: The text content of the LinkedIn post.
        auto_post: If True, attempts to post automatically (requires LinkedIn API setup).
                   If False (default), saves to approval queue.

    Returns:
        A confirmation message.
    """
    try:
        print(f"--- LINKEDIN POST REQUEST ---")
        print(f"Content: {content}")
        print(f"Auto-post: {auto_post}")
        print(f"-----------------------------")

        # Log to business log
        log_file_path = os.path.join(
            os.path.dirname(__file__), "..", "..", "AI_Employee_Vault", "logs", "business.log"
        )
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if auto_post:
            # TODO: Implement real LinkedIn API posting here
            # For now, save to approval queue
            approval_dir = os.path.join(
                os.path.dirname(__file__), "..", "..", "AI_Employee_Vault", "Need_Approval"
            )
            os.makedirs(approval_dir, exist_ok=True)

            approval_file = os.path.join(
                approval_dir,
                f"linkedin_post_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            )

            with open(approval_file, 'w') as f:
                f.write(f"# LinkedIn Post - Pending Approval\n\n")
                f.write(f"**Created:** {timestamp}\n\n")
                f.write(f"**Content:**\n\n{content}\n\n")
                f.write(f"---\n\n")
                f.write(f"To approve: Delete this file and manually post to LinkedIn\n")

            with open(log_file_path, "a") as log_file:
                log_file.write(f"[{timestamp}] 📝 LinkedIn post queued for approval: {content[:100]}...\n")

            print(f"✅ LinkedIn post saved to approval queue: {approval_file}")
            return f"✅ LinkedIn post queued for approval. Check: AI_Employee_Vault/Need_Approval/"

        else:
            # Direct simulation mode (for testing)
            with open(log_file_path, "a") as log_file:
                log_file.write(f"[{timestamp}] 🚀 LinkedIn post created (simulated): {content[:100]}...\n")

            # Call the social summary script
            try:
                current_time = datetime.datetime.now().isoformat()
                subprocess.run(
                    [sys.executable, LOG_SOCIAL_POST_SCRIPT, "LinkedIn", content, current_time],
                    check=True,
                    capture_output=True,
                    text=True
                )
                print(f"Social post logged by {os.path.basename(LOG_SOCIAL_POST_SCRIPT)}")
            except Exception as e:
                print(f"Error logging social post: {e}")

            print("✅ LinkedIn post logged successfully!")
            return f"✅ LinkedIn post created (simulated). Content: {content[:50]}..."

    except Exception as e:
        error_msg = f"LinkedIn post failed: {str(e)}"
        print(f"❌ {error_msg}")
        return error_msg

@app.tool()
def log_activity(message: str) -> str:
    """
    Logs a business activity message to the vault.

    Args:
        message: The message to log.

    Returns:
        A confirmation message.
    """
    log_file_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "AI_Employee_Vault", "logs", "business.log"
    )
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    
    with open(log_file_path, "a") as log_file:
        log_file.write(f"{message}\n")
        
    return f"Activity logged to {log_file_path}"

if __name__ == "__main__":
    import uvicorn
    # The server will be accessible at http://127.0.0.1:8000
    # The OpenAPI spec will be at http://127.0.0.1:8000/openapi.json
    uvicorn.run(app, host="0.0.0.0", port=8000)
