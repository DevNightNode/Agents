import os
from typing import List, Dict, Any
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from agents import function_tool

# Initialize Slack client
slack_client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))

@function_tool
def read_channel_history(channel_id: str, limit: int = 100) -> Dict[str, Any]:
    """
    Read the recent message history from a Slack channel.
    
    Args:
        channel_id (str): The Slack channel ID to read from
        limit (int): Maximum number of messages to retrieve (default: 100)
    
    Returns:
        Dict containing channel history with messages and metadata
    """
    try:
        response = slack_client.conversations_history(
            channel=channel_id,
            limit=limit
        )
        return {
            "channel_id": channel_id,
            "messages": response["messages"],
            "is_truncated": response.get("has_more", False)
        }
    except SlackApiError as e:
        return {"error": f"Slack API error: {e.response['error']}"}

@function_tool
def post_message(channel_id: str, text: str, thread_ts: str = None) -> Dict[str, Any]:
    """
    Post a message to a Slack channel.
    
    Args:
        channel_id (str): The Slack channel ID to post to
        text (str): The message text to post
        thread_ts (str, optional): Timestamp of thread to reply in
    
    Returns:
        Dict containing the post result with message details
    """
    try:
        response = slack_client.chat_postMessage(
            channel=channel_id,
            text=text,
            thread_ts=thread_ts
        )
        return {
            "channel_id": channel_id,
            "message_ts": response["ts"],
            "text": text
        }
    except SlackApiError as e:
        return {"error": f"Slack API error: {e.response['error']}"}

@function_tool
def list_channel_members(channel_id: str) -> Dict[str, Any]:
    """
    List all members in a Slack channel.
    
    Args:
        channel_id (str): The Slack channel ID to list members for
    
    Returns:
        Dict containing channel members and metadata
    """
    try:
        response = slack_client.conversations_members(
            channel=channel_id
        )
        return {
            "channel_id": channel_id,
            "member_ids": response["members"]
        }
    except SlackApiError as e:
        return {"error": f"Slack API error: {e.response['error']}"}
