import os
import requests
from typing import Optional, List, Dict, Any
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()

# Zendesk API configuration
ZENDESK_SUBDOMAIN = os.getenv("ZENDESK_SUBDOMAIN")
ZENDESK_EMAIL = os.getenv("ZENDESK_EMAIL")
ZENDESK_API_TOKEN = os.getenv("ZENDESK_API_TOKEN")
ZENDESK_API_URL = f"https://{ZENDESK_SUBDOMAIN}.zendesk.com/api/v2"

# Create authentication tuple
auth = (f"{ZENDESK_EMAIL}/token", ZENDESK_API_TOKEN)

@tool
def search_help_center(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Search the Zendesk help center for articles matching the query.
    
    Args:
        query: Search query string
        limit: Maximum number of results to return (default: 10)
    
    Returns:
        List of dictionaries containing article information
    """
    url = f"{ZENDESK_API_URL}/help_center/articles/search.json"
    params = {"query": query, "limit": limit}
    
    response = requests.get(url, auth=auth, params=params)
    response.raise_for_status()
    
    articles = response.json().get("results", [])
    return [
        {
            "id": article["id"],
            "title": article["title"],
            "url": article["html_url"],
            "excerpt": article.get("excerpt", ""),
            "created_at": article["created_at"]
        }
        for article in articles
    ]

@tool
def get_ticket(ticket_id: int) -> Dict[str, Any]:
    """
    Retrieve a specific ticket by ID.
    
    Args:
        ticket_id: The Zendesk ticket ID
    
    Returns:
        Dictionary containing ticket information
    """
    url = f"{ZENDESK_API_URL}/tickets/{ticket_id}.json"
    
    response = requests.get(url, auth=auth)
    response.raise_for_status()
    
    ticket = response.json()["ticket"]
    return {
        "id": ticket["id"],
        "subject": ticket["subject"],
        "description": ticket["description"],
        "status": ticket["status"],
        "priority": ticket["priority"],
        "requester": ticket["requester"]["name"],
        "requester_email": ticket["requester"]["email"],
        "created_at": ticket["created_at"],
        "updated_at": ticket["updated_at"],
        "tags": ticket.get("tags", []),
        "comments": [
            {
                "id": comment["id"],
                "author": comment["author_id"],
                "body": comment["body"],
                "created_at": comment["created_at"]
            }
            for comment in ticket.get("comments", [])
        ]
    }

@tool
def reply_to_ticket(ticket_id: int, message: str, is_public: bool = True) -> Dict[str, Any]:
    """
    Reply to a Zendesk ticket with a message.
    
    Args:
        ticket_id: The Zendesk ticket ID
        message: The reply message to send
        is_public: Whether the reply should be visible to the customer (default: True)
    
    Returns:
        Dictionary containing reply information
    """
    url = f"{ZENDESK_API_URL}/tickets/{ticket_id}/comments.json"
    
    payload = {
        "ticket": {
            "id": ticket_id,
            "comment": {
                "body": message,
                "public": is_public
            }
        }
    }
    
    response = requests.put(url, auth=auth, json=payload)
    response.raise_for_status()
    
    comment = response.json()["comment"]
    return {
        "id": comment["id"],
        "ticket_id": ticket_id,
        "body": comment["body"],
        "created_at": comment["created_at"],
        "is_public": comment["public"]
    }

@tool
def escalate_ticket(ticket_id: int, assignee_id: Optional[int] = None, 
                   group_id: Optional[int] = None, priority: Optional[str] = None) -> Dict[str, Any]:
    """
    Escalate a ticket by assigning it to an agent or group, or changing its priority.
    
    Args:
        ticket_id: The Zendesk ticket ID
        assignee_id: The ID of the agent to assign the ticket to (optional)
        group_id: The ID of the group to assign the ticket to (optional)
        priority: The new priority level (one of 'low', 'normal', 'high', 'urgent') (optional)
    
    Returns:
        Dictionary containing escalation information
    """
    url = f"{ZENDESK_API_URL}/tickets/{ticket_id}.json"
    
    ticket_updates = {}
    if assignee_id is not None:
        ticket_updates["assignee_id"] = assignee_id
    if group_id is not None:
        ticket_updates["group_id"] = group_id
    if priority is not None:
        ticket_updates["priority"] = priority
    
    payload = {"ticket": ticket_updates}
    
    response = requests.put(url, auth=auth, json=payload)
    response.raise_for_status()
    
    updated_ticket = response.json()["ticket"]
    return {
        "id": updated_ticket["id"],
        "status": updated_ticket["status"],
        "priority": updated_ticket["priority"],
        "assignee_id": updated_ticket.get("assignee_id"),
        "group_id": updated_ticket.get("group_id"),
        "updated_at": updated_ticket["updated_at"]
    }
