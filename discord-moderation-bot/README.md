# Discord Moderation Bot

A Discord moderation agent built with LangChain.js that automatically detects and handles rule violations in Discord servers.

## Features

- **Message Analysis**: Uses AI to analyze messages for moderation violations
- **Automated Actions**: Deletes inappropriate messages, timeouts, and bans users
- **Logging**: Comprehensive logging of all moderation actions
- **Extensible**: Easy to add new moderation rules and actions

## Tools

### `delete_message`
Deletes a message from a Discord channel.

**Parameters:**
- `messageId` (string): The ID of the message to delete
- `channelId` (string): The ID of the channel where the message is located
- `guildId` (string): The ID of the guild where the message is located

### `timeout_member`
Timeouts a member in a Discord guild for a specified duration.

**Parameters:**
- `memberId` (string): The ID of the member to timeout
- `guildId` (string): The ID of the guild where the member is located
- `duration` (number): Timeout duration in seconds
- `reason` (string): Reason for the timeout

### `ban_member`
Bans a member from a Discord guild.

**Parameters:**
- `memberId` (string): The ID of the member to ban
- `guildId` (string): The ID of the guild where the member is located
- `reason` (string): Reason for the ban

### `log_action`
Logs moderation actions to a database or file.

**Parameters:**
- `action` (string): Type of action performed (e.g., "delete", "timeout", "ban")
- `details` (object): Details about the action including:
  - `messageId` (string, optional): ID of the message if applicable
  - `memberId` (string, optional): ID of the member if applicable
  - `guildId` (string, optional): ID of the guild if applicable
  - `reason` (string, optional): Reason for the action
  - `duration` (number, optional): Duration of timeout if applicable

## Required Environment Variables

Create a `.env` file with the following variables:

```env
DISCORD_BOT_TOKEN=your_discord_bot_token_here
OPENAI_API_KEY=your_openai_api_key_here
```

## How to Run

1. Install dependencies:
```bash
npm install
```

2. Set up your environment variables in `.env` file

3. Start the bot:
```bash
npm start
```

## Implementation Notes

This implementation provides a complete framework for Discord moderation using LangChain.js. The agent can be extended with additional tools and rules as needed. All actions are logged to a file for audit purposes.

The tools currently simulate actions for demonstration purposes. In a production environment, they would interact with the actual Discord API through discord.js and with a database for persistent logging.
