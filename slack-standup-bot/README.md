# Slack Standup Bot

A Slack bot that collects daily standup updates from a Slack channel, summarizes them, and posts a digest.

## Features

- Collects standup updates from a designated Slack channel
- Summarizes the updates into a concise digest
- Posts the summary back to the same channel
- Uses OpenAI's GPT-4.1 for natural language processing

## Tools

1. **read_channel_history**
   - Reads recent message history from a Slack channel
   - Parameters:
     - `channel_id` (str): The Slack channel ID to read from
     - `limit` (int): Maximum number of messages to retrieve (default: 100)

2. **post_message**
   - Posts a message to a Slack channel
   - Parameters:
     - `channel_id` (str): The Slack channel ID to post to
     - `text` (str): The message text to post
     - `thread_ts` (str, optional): Timestamp of thread to reply in

3. **list_channel_members**
   - Lists all members in a Slack channel
   - Parameters:
     - `channel_id` (str): The Slack channel ID to list members for

## Required Environment Variables

- `SLACK_BOT_TOKEN`: Slack bot token with appropriate permissions
- `STANDUP_CHANNEL_ID`: The Slack channel ID where standups are collected

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Create a `.env` file based on `.env.example`:
   ```
   SLACK_BOT_TOKEN=xoxb-your-slack-bot-token
   STANDUP_CHANNEL_ID=C012AB3CD
   ```

3. Run the agent:
   ```
   python main.py
   ```

## Usage

The bot will automatically collect standup updates from the specified channel, analyze them, and post a summary back to the same channel. The bot expects standup updates to be in a standard format (e.g., "What I did", "What I'm doing", "Blockers").

## Requirements

- Python 3.8+
- Slack bot token with `channels:history`, `channels:read`, `chat:write`, and `users:read` permissions
