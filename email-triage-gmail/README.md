# Email Triage Gmail Agent

An AI-powered email triage agent that automatically organizes, labels, drafts replies, and forwards important emails using the Gmail API.

## Features

- **List unread emails**: Retrieves all unread emails with subject, sender, and snippet
- **Apply labels**: Automatically categorizes emails with custom labels
- **Draft replies**: Creates draft replies to important emails
- **Forward emails**: Forwards important emails to other recipients

## Tools

### `list_unread()`
Lists all unread emails in the inbox with subject, sender, and snippet.

### `apply_label(message_id: str, label_name: str)`
Applies a label to an email message. Creates the label if it doesn't exist.

### `draft_reply(message_id: str, draft_content: str)`
Creates a draft reply to an email message with the specified content.

### `forward_email(message_id: str, recipient_email: str, forward_content: str = "")`
Forwards an email to another recipient with optional additional content.

## Requirements

- Python 3.8+
- OpenAI API key
- Gmail API credentials

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a Google Cloud project and enable the Gmail API:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the Gmail API
   - Create credentials (OAuth 2.0 Client ID)
   - Download the `credentials.json` file to your project directory

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env to add your OpenAI API key
```

4. Run the agent:
```bash
python main.py
```

## How It Works

The agent uses a LangGraph workflow that:
1. Calls the LLM with the available tools
2. The LLM decides which tool to use and what parameters to pass
3. The agent executes the tool and returns results to the LLM
4. This continues until the task is complete

## Authentication

The first time you run the agent, it will open a browser window to authenticate with your Gmail account. The authentication token will be saved in `token.json` for future use.

## Security

- All credentials are stored locally in `token.json` and `credentials.json`
- The agent only accesses your Gmail account with the permissions you grant
- No email content is stored or transmitted outside your local environment
