# Business MCP Server

This directory contains a Python-based MCP (Managed Component Platform) server for handling external business actions.

## Capabilities

The server exposes the following tools:

1.  **Send Email**: `send_email(to, subject, body)`
    -   Simulates sending an email. In a real application, this would integrate with an email service provider.
    -   **Parameters**:
        -   `to` (str): The recipient's email address.
        -   `subject` (str): The email subject.
        -   `body` (str): The email content.

2.  **Create LinkedIn Post**: `post_linkedin(content)`
    -   Simulates creating a post on LinkedIn.
    -   **Parameters**:
        -   `content` (str): The text for the LinkedIn post.

3.  **Log Business Activity**: `log_activity(message)`
    -   Logs a message to a central business activity log file.
    -   **Parameters**:
        -   `message` (str): The activity message to log.
    -   **Log File Location**: `AI_Employee_Vault/logs/business.log`

## Setup and Installation

Before running the server, ensure you have the necessary dependencies installed. The primary dependencies are `fastapi` and `uvicorn`.

```bash
pip install fastapi uvicorn
```

## Running the Server

To start the MCP server, run the `server.py` script:

```bash
python mcp/business_mcp/server.py
```

The server will start and be accessible at `http://127.0.0.1:8000`.

The OpenAPI (Swagger) documentation for the available API routes will be available at `http://127.0.0.1:8000/docs`.
