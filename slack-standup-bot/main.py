import os
import sys
from typing import Dict, Any
from agents import Agent, Runner, function_tool, ModelSettings
from tools import read_channel_history, post_message, list_channel_members

# Import the tools
tools = [read_channel_history, post_message, list_channel_members]

# System instructions for the agent
instructions = """
You are a Slack standup bot that collects daily standup updates from a Slack channel, 
summarizes them, and posts a digest. You have access to three tools:
1. read_channel_history - Read recent messages from a Slack channel
2. post_message - Post a message to a Slack channel
3. list_channel_members - List all members in a Slack channel

Your workflow:
1. First, use list_channel_members to get the list of members in the standup channel
2. Then, use read_channel_history to get recent messages from the channel
3. Analyze the messages to extract standup updates (typically starting with "What I did", "What I'm doing", or "Blockers")
4. Create a summary of the standup updates
5. Use post_message to post the summary back to the channel

Always ensure you're working with the correct channel ID and that messages are properly formatted.
"""

# Create the agent
agent = Agent(
    name="slack-standup-bot",
    instructions=instructions,
    model="gpt-4.1",
    tools=tools
)

def main():
    # Get channel ID from environment
    channel_id = os.environ.get("STANDUP_CHANNEL_ID")
    if not channel_id:
        print("Error: STANDUP_CHANNEL_ID environment variable not set")
        sys.exit(1)
    
    # Run the agent with a sample input
    user_input = f"Collect standup updates from channel {channel_id} and create a summary"
    
    try:
        result = Runner.run_sync(agent, user_input, max_turns=10)
        print("Final output:")
        print(result.final_output)
    except Exception as e:
        print(f"Error running agent: {e}")

if __name__ == "__main__":
    main()
