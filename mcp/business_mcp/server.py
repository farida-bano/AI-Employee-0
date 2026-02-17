import os
import subprocess
import datetime # Added for timestamp
from mcp.server.fastmcp import FastMCP

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
def post_linkedin(content: str) -> str:
    """
    Creates a new post on LinkedIn.

    Args:
        content: The text content of the LinkedIn post.

    Returns:
        A confirmation message.
    """
    # Real-world implementation would require using the LinkedIn API.
    # This requires setting up an app on the LinkedIn Developer portal,
    # handling OAuth 2.0 authentication, and using a library like 'requests'.
    # For now, we simulate the action by printing to the console.
    print(f"--- LINKEDIN POST ---")
    print(f"Content: {content}")
    print(f"---------------------")

    # Call the social summary script after a successful LinkedIn post
    try:
        current_time = datetime.datetime.now().isoformat()
        # Use sys.executable to ensure the correct Python interpreter is used
        subprocess.run(
            [sys.executable, LOG_SOCIAL_POST_SCRIPT, "LinkedIn", content, current_time],
            check=True, # Raise CalledProcessError if the script returns a non-zero exit code
            capture_output=True,
            text=True
        )
        print(f"Social post logged by {os.path.basename(LOG_SOCIAL_POST_SCRIPT)}")
    except subprocess.CalledProcessError as e:
        print(f"Error logging social post: {e.stderr}")
    except FileNotFoundError:
        print(f"Error: Social logging script not found at {LOG_SOCIAL_POST_SCRIPT}")
    except Exception as e:
        print(f"An unexpected error occurred while calling social logging script: {e}")

    return "LinkedIn post successfully created (simulated)."

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
